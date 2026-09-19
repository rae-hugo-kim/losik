"""Offline 48 kHz stereo PCM24 mastering and manifest-aware v2 verification.

Manifest section and active-interval times are seconds, with half-open bounds.
A release is a 100 ms fade ending at zero, not 100 ms of digital silence.
Only master() writes audio; measure() returns evidence without saving JSON.
"""
from pathlib import Path
import audioop
import hashlib
import math
import mmap
import os
import re
import struct
import subprocess
import sys
import tempfile

from render_tide_variants import wave_data, fade_release


FS = 8388607.0
CEIL = 10 ** (-0.1 / 20)
KNEE = 0.9 * CEIL
FRAME_BYTES = 6
CHUNK_BYTES = 65536 * FRAME_BYTES
# Search the high byte of each sample in C; decode only possible knee hits.
_KNEE_CANDIDATES = re.compile(bytes((91, int(KNEE * FS) >> 16, 45,
                                    (16777216 - int(KNEE * FS)) >> 16, 93)))
_FULL_SCALE = re.compile(b'\xff\xff\x7f|\x01\x00\x80|\x00\x00\x80')
_ZERO_RUN = re.compile(b'\x00{6,}')


def _header(file):
    """Check physical RIFF/chunk lengths before using the shared data locator."""
    assert sys.byteorder == 'little', 'audioop requires a little-endian host'
    physical = os.fstat(file.fileno()).st_size
    file.seek(0)
    header = file.read(12)
    assert len(header) == 12 and header[:4] == b'RIFF' and header[8:] == b'WAVE', 'Not RIFF/WAVE'
    assert struct.unpack_from('<I', header, 4)[0] + 8 == physical, 'RIFF length mismatch'
    position, fmt, data = 12, None, None
    while position < physical:
        assert position + 8 <= physical, 'Truncated chunk header'
        file.seek(position)
        kind, size = struct.unpack('<4sI', file.read(8))
        end = position + 8 + size
        assert end + (size & 1) <= physical, ('Truncated chunk', kind, size)
        if kind == b'fmt ':
            assert fmt is None and size >= 16, 'Invalid/duplicate fmt chunk'
            fmt = struct.unpack('<HHIIHH', file.read(16))
            assert fmt[0] in (1, 65534) and fmt[1:] == (2, 48000, 288000, 6, 24), (
                'Expected PCM24 stereo 48kHz', fmt)
            if fmt[0] == 65534:
                assert size >= 40, 'Truncated WAVE_FORMAT_EXTENSIBLE'
                extra, valid_bits, mask = struct.unpack('<HHI', file.read(8))
                subtype = file.read(16)
                assert 22 <= extra <= size - 18, 'Invalid extensible format length'
                assert valid_bits == 24 and mask == 3, ('Expected stereo PCM24 layout', valid_bits, mask)
                assert subtype == bytes.fromhex('0100000000001000800000aa00389b71'), (
                    'Expected extensible PCM subtype', subtype.hex())
        elif kind == b'data':
            assert fmt is not None and data is None, 'Missing fmt/duplicate data chunk'
            assert size % FRAME_BYTES == 0 and size >= 4800 * FRAME_BYTES, 'Invalid data frame count'
            data = (position + 8, size)
        position = end + (size & 1)
    assert position == physical and data is not None, 'Missing data or invalid physical length'
    file.seek(0)
    begin, size, rate, channels, bits = wave_data(file)
    assert (begin, size) == data
    return begin, size, rate, channels, bits, physical


def _dbfs(amplitude):
    # A finite -300 dB floor keeps evidence strict-JSON-compatible for silence.
    return round(20 * math.log10(max(amplitude / 8388608.0, 1e-15)), 3)


def _rms(mapped, begin, first, last):
    """Bounded C RMS, weighted by samples; 32-bit expansion limits rounding."""
    energy, count = 0.0, 0
    for at in range(begin + first * FRAME_BYTES, begin + last * FRAME_BYTES, CHUNK_BYTES):
        raw = mapped[at:min(at + CHUNK_BYTES, begin + last * FRAME_BYTES)]
        samples = len(raw) // 3
        rms = audioop.rms(audioop.lin2lin(raw, 3, 4), 4) / 256.0
        energy += rms * rms * samples
        count += samples
    assert count, 'Empty RMS interval'
    return _dbfs(math.sqrt(energy / count))


def master(aiff: Path, wav: Path) -> dict:
    """Convert without replacing wav, soft-limit affected samples, fade 100 ms.

    AIFF is never opened for writing. A same-directory temporary WAV is linked
    into place only when complete; an existing destination is never replaced.
    """
    aiff, wav = Path(aiff), Path(wav)
    assert aiff.is_file(), ('Missing source AIFF', str(aiff))
    assert not os.path.lexists(wav), ('Refusing to overwrite WAV', str(wav))
    hits, changed = 0, 0
    with tempfile.TemporaryDirectory(prefix='.v2-master-', dir=str(wav.parent)) as directory:
        temporary = Path(directory) / 'master.wav'
        subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI24', str(aiff), str(temporary)],
                       check=True, capture_output=True, text=True)
        with temporary.open('r+b') as file:
            begin, size, rate, channels, bits, physical = _header(file)
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_WRITE) as mapped:
                for at in range(begin, begin + size, CHUNK_BYTES):
                    raw = mapped[at:min(at + CHUNK_BYTES, begin + size)]
                    if audioop.max(raw, 3) <= KNEE * FS:
                        continue
                    for match in _KNEE_CANDIDATES.finditer(raw[2::3]):
                        offset = match.start() * 3
                        sample = int.from_bytes(raw[offset:offset + 3], 'little', signed=True)
                        x = sample / FS
                        if abs(x) <= KNEE:
                            continue
                        limited = math.copysign(KNEE + (CEIL - KNEE) *
                                               math.tanh((abs(x) - KNEE) / (CEIL - KNEE)), x)
                        value = max(-8388608, min(8388607, int(limited * FS)))
                        hits += 1
                        if value != sample:
                            mapped[at + offset:at + offset + 3] = value.to_bytes(3, 'little', signed=True)
                            changed += 1
                mapped.flush()
            os.fsync(file.fileno())
        fade_release(temporary)
        # link() is exclusive even if a destination appears after the assertion.
        os.link(str(temporary), str(wav))
    return dict(path=str(wav), source_aiff=str(aiff), bytes=physical,
                data_offset=begin, data_bytes=size, frames=size // FRAME_BYTES,
                seconds=size / FRAME_BYTES / rate, sample_rate=rate, channels=channels,
                bits=bits, limiter_samples=hits, changed_samples=changed,
                limiter_ceiling_dbfs=-0.1, release_fade_ms=100)


def measure(wav: Path, manifest: dict) -> dict:
    """Verify PCM layout, length, peaks, zero endpoint and all >=100 ms rests.

    Zero runs use complete all-zero stereo frames, including leading/trailing
    runs. Any positive overlap with an active interval is an unexpected dropout.
    Assertion errors include the evidence dictionary for audio-contract failures.
    Section RMS combines both channels without cancellation; silent RMS is -300.
    """
    wav = Path(wav)
    expected = float(manifest['duration_seconds'])
    assert math.isfinite(expected) and expected > 0, 'Invalid manifest duration'
    intervals = []
    for start, end in manifest['active_intervals']:
        start, end = float(start), float(end)
        assert math.isfinite(start) and math.isfinite(end) and 0 <= start < end <= expected + 1e-9
        assert not intervals or start >= intervals[-1][1], 'Active intervals must be sorted and merged'
        intervals.append((start, end))
    with wav.open('rb') as file:
        begin, size, rate, channels, bits, physical = _header(file)
        frames = size // FRAME_BYTES
        seconds = frames / rate
        assert abs(seconds - expected) <= 0.10 + 1e-9, ('Duration mismatch', seconds, expected)
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mapped:
            peaks, clipped = [0, 0], 0
            for at in range(begin, begin + size, CHUNK_BYTES):
                raw = mapped[at:min(at + CHUNK_BYTES, begin + size)]
                for channel in range(2):
                    mono = audioop.tomono(raw, 3, int(channel == 0), int(channel == 1))
                    peaks[channel] = max(peaks[channel], audioop.max(mono, 3))
                if audioop.max(raw, 3) >= FS:
                    # Lookahead permits adjacent sample patterns; alignment rejects
                    # byte sequences which cross an actual sample boundary.
                    clipped += sum(match.start() % 3 == 0 for match in
                                   re.finditer(b'(?=' + _FULL_SCALE.pattern + b')', raw))
            zero_runs, unexpected = [], []
            interval_index = 0
            for match in _ZERO_RUN.finditer(mapped, begin, begin + size):
                first = (match.start() - begin + FRAME_BYTES - 1) // FRAME_BYTES
                last = (match.end() - begin) // FRAME_BYTES
                if last - first < rate // 10:
                    continue
                run = dict(start_frame=first, end_frame=last, frames=last - first,
                           start=first / rate, end=last / rate, seconds=(last - first) / rate)
                zero_runs.append(run)
                while interval_index < len(intervals) and intervals[interval_index][1] <= run['start']:
                    interval_index += 1
                if interval_index < len(intervals) and intervals[interval_index][0] < run['end']:
                    unexpected.append(run)
            levels, section_frames = {}, {}
            for section in manifest['sections']:
                name = section['name']
                start, end = float(section['start']), float(section['end'])
                assert name not in levels, ('Duplicate section name', name)
                assert math.isfinite(start) and math.isfinite(end) and 0 <= start < end <= expected + 1e-9
                first, last = round(start * rate), min(frames, round(end * rate))
                assert 0 <= first < last <= frames, ('Empty/out-of-range section', name)
                levels[name] = _rms(mapped, begin, first, last)
                section_frames[name] = [first, last]
            assert levels, 'Missing manifest sections'
            final = [int.from_bytes(mapped[begin + size - 6:begin + size - 3], 'little', signed=True),
                     int.from_bytes(mapped[begin + size - 3:begin + size], 'little', signed=True)]
            hasher = hashlib.sha256()
            for at in range(0, physical, CHUNK_BYTES):
                hasher.update(mapped[at:min(at + CHUNK_BYTES, physical)])
            result = dict(path=str(wav), seconds=seconds, bytes=physical, sha256=hasher.hexdigest(),
                          sample_rate=rate, channels=channels, bits=bits, data_offset=begin,
                          data_bytes=size, frames=frames, peak_dbfs=[_dbfs(n) for n in peaks],
                          peak_samples=peaks, full_scale_samples=clipped, section_rms_dbfs=levels,
                          section_frames=section_frames, zero_runs=zero_runs,
                          unexpected_zero_runs=unexpected, final_frame=final,
                          release_tail_frames=rate // 10,
                          last_100ms_rms_dbfs=_rms(mapped, begin, frames - rate // 10, frames))
    assert not clipped and max(peaks) / 8388608.0 <= CEIL, ('Peak/full-scale violation', result)
    assert final == [0, 0], ('Nonzero final frame', result)
    assert not unexpected, ('Unexpected digital dropouts', result)
    return result
