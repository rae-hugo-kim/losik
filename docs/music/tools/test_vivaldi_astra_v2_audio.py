"""Synthetic-fixture tests for vivaldi_astra_v2_audio.measure (no external files, no composer).

Run: python3 -m unittest discover -s docs/music/tools -p 'test_vivaldi_astra_v2_audio.py'
"""
import hashlib
import math
import os
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vivaldi_astra_v2_audio as audio  # noqa: E402

PERIOD = 100  # frames; 480 Hz at 48 kHz, 441 Hz at 44.1 kHz


def _period(left_amp, right_amp):
    frames = bytearray()
    for i in range(PERIOD):
        phase = 2 * math.pi * i / PERIOD
        for amp in (left_amp, right_amp):
            frames += int(round(amp * 8388607 * math.sin(phase))).to_bytes(3, 'little', signed=True)
    return bytes(frames)


def pcm(frames, left_amp=0.5, right_amp=0.4):
    whole, rest = divmod(frames, PERIOD)
    block = _period(left_amp, right_amp)
    return block * whole + block[:rest * 6]


def zero(data, first, last):
    return data[:first * 6] + bytes((last - first) * 6) + data[last * 6:]


def wav(data, rate=48000, extensible=False, bits=24, channels=2):
    align = channels * bits // 8
    if extensible:
        fmt = struct.pack('<HHIIHHHHI', 0xFFFE, channels, rate, rate * align, align, bits, 22, bits, 3)
        fmt += audio.PCM_GUID
    else:
        fmt = struct.pack('<HHIIHH', 1, channels, rate, rate * align, align, bits)
    junk = b'JUNK' + struct.pack('<I', 28) + bytes(28)
    body = (b'WAVE' + junk + b'fmt ' + struct.pack('<I', len(fmt)) + fmt +
            b'data' + struct.pack('<I', len(data)) + data)
    return b'RIFF' + struct.pack('<I', len(body)) + body


class MeasureTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='vivaldi-v2-audio-test-')
        self.addCleanup(self.directory.cleanup)

    def write(self, content, name='fixture.wav'):
        path = Path(self.directory.name) / name
        path.write_bytes(content)
        return path

    def failures(self, path, expected, sections, intervals):
        with self.assertRaises(audio.AudioCheckError) as caught:
            audio.measure(path, expected, sections, intervals)
        self.assertEqual(caught.exception.path, str(path))
        return caught.exception.failures

    def test_valid_pcm_reports_and_leaves_source_unchanged(self):
        content = wav(pcm(3 * 48000))
        path = self.write(content)
        stat = os.stat(path)
        sections = [dict(name='intro', start=0, end=1), dict(name='theme', start=1, end=3)]
        result = audio.measure(path, 3.0, sections, [(0.0, 3.0)])
        self.assertEqual(result['sha256'], hashlib.sha256(content).hexdigest())
        self.assertEqual((result['frames'], result['sample_rate'], result['bytes']), (144000, 48000, len(content)))
        self.assertEqual(result['zero_runs'], [])
        self.assertAlmostEqual(result['peak_dbfs'][0], 20 * math.log10(0.5), places=2)
        self.assertEqual(set(result['section_rms_dbfs']), {'intro', 'theme'})
        self.assertIn('theme', result['boundary_delta_db'])
        self.assertLess(abs(result['boundary_delta_db']['theme']), 0.1)
        self.assertEqual(path.read_bytes(), content)
        self.assertEqual(os.stat(path).st_mtime_ns, stat.st_mtime_ns)

    def test_valid_extensible_44k1(self):
        path = self.write(wav(pcm(2 * 44100), rate=44100, extensible=True))
        result = audio.measure(path, 2.0, [dict(name='all', start=0, end=2)], [(0.1, 1.9)])
        self.assertEqual((result['sample_rate'], result['format_tag']), (44100, 0xFFFE))

    def test_truncated_data_chunk(self):
        content = wav(pcm(2 * 48000))
        path = self.write(content[:-600])
        failures = self.failures(path, 2.0, [dict(name='all', start=0, end=2)], [])
        self.assertTrue(any(f.startswith('data_truncated:') for f in failures), failures)
        self.assertTrue(any(f.startswith('riff_length:') for f in failures), failures)

    def test_single_channel_silent(self):
        path = self.write(wav(pcm(2 * 48000, right_amp=0.0)))
        failures = self.failures(path, 2.0, [dict(name='all', start=0, end=2)], [])
        self.assertEqual([f.split(':')[0] for f in failures], ['channel_silent'], failures)
        self.assertIn('right', failures[0])

    def test_zero_run_crossing_read_chunk_is_merged(self):
        frames = audio.CHUNK_FRAMES + 48000
        first, last = audio.CHUNK_FRAMES - 3000, audio.CHUNK_FRAMES + 3000
        # Each half alone is 62.5 ms (< 100 ms); only the merged run qualifies.
        self.assertLess(3000, round(audio.MIN_ZERO_RUN_SECONDS * 48000))
        path = self.write(wav(zero(pcm(frames), first, last)))
        seconds = frames / 48000
        sections = [dict(name='all', start=0, end=seconds)]
        result = audio.measure(path, seconds, sections, [(0.0, 0.5)])
        self.assertEqual([(r['start_frame'], r['end_frame']) for r in result['zero_runs']], [(first, last)])
        self.assertEqual(result['unexpected_zero_runs'], [])
        failures = self.failures(path, seconds, sections, [(0.0, seconds)])
        self.assertEqual([f.split(':')[0] for f in failures], ['unexpected_zero_run'], failures)

    def test_onset_tolerance_is_ten_ms(self):
        path = self.write(wav(zero(pcm(3 * 48000), 48000, 57600)))  # zeros 1.0-1.2 s
        sections = [dict(name='all', start=0, end=3)]
        tolerated = audio.measure(path, 3.0, sections, [(1.195, 2.0)])
        self.assertEqual(len(tolerated['zero_runs']), 1)
        self.assertEqual(tolerated['unexpected_zero_runs'], [])
        failures = self.failures(path, 3.0, sections, [(0.0, 0.5), (1.15, 2.0)])
        self.assertEqual(len(failures), 1)
        self.assertIn('1.15-2.0', failures[0])

    def test_ceiling_violation(self):
        path = self.write(wav(pcm(2 * 48000, left_amp=1.0)))
        failures = self.failures(path, 2.0, [dict(name='all', start=0, end=2)], [])
        self.assertEqual([f.split(':')[0] for f in failures], ['ceiling'], failures)

    def test_length_window(self):
        path = self.write(wav(pcm(3 * 48000)))
        sections = [dict(name='all', start=0, end=3)]
        short = self.failures(path, 3.2, sections, [])
        self.assertEqual([f.split(':')[0] for f in short], ['length'], short)
        audio.measure(path, 3.05, [dict(name='all', start=0, end=3.05)], [])
        long_tail = self.write(wav(pcm(12 * 48000 + 33600)), 'long.wav')  # 12.7 s
        tail = self.failures(long_tail, 0.5, [dict(name='all', start=0, end=0.5)], [])
        self.assertEqual([f.split(':')[0] for f in tail], ['length'], tail)

    def test_wrong_layout_and_missing_file(self):
        path = self.write(wav(bytes(48000 * 4), bits=16))
        failures = self.failures(path, 1.0, [dict(name='all', start=0, end=1)], [])
        self.assertTrue(any(f.startswith('fmt_layout:') for f in failures), failures)
        missing = Path(self.directory.name) / 'absent.wav'
        self.assertEqual(self.failures(missing, 1.0, [dict(name='all', start=0, end=1)], []),
                         ['missing_file: no regular file at path'])

    def test_rejects_unmerged_intervals(self):
        path = self.write(wav(pcm(48000)))
        with self.assertRaises(ValueError):
            audio.measure(path, 1.0, [dict(name='all', start=0, end=1)], [(0.0, 0.6), (0.5, 0.9)])


if __name__ == '__main__':
    unittest.main()
