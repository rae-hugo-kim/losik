"""Boundary tests for real AIFF readiness before Logic's destructive limiter."""
import struct
import tempfile
import unittest
from pathlib import Path

from pipeline import _aiff_ready


def fixture(frames=32, bits=24, compression=None):
    rate=b'\x40\x0e\xbb\x80'+b'\0'*6  # 48000 in AIFF extended precision.
    comm=struct.pack('>HIH',2,frames,bits)+rate
    kind=b'AIFC' if compression else b'AIFF'
    if compression:
        comm+=compression+b'\0\0'
    samples=b'\x10\x20\x30\x40'[:bits//8]*(frames*2)
    ssnd=b'\0'*8+samples
    body=kind+b'COMM'+struct.pack('>I',len(comm))+comm+b'SSND'+struct.pack('>I',len(ssnd))+ssnd
    return b'FORM'+struct.pack('>I',len(body))+body


class AiffReadinessTests(unittest.TestCase):
    def test_complete_pcm24_is_ready_and_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'complete.aif'; data=fixture(); path.write_bytes(data)
            self.assertTrue(_aiff_ready(path))
            self.assertEqual(path.read_bytes(),data)

    def test_stable_but_truncated_data_is_not_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'partial.aif'; data=fixture(); path.write_bytes(data[:-24])
            self.assertFalse(_aiff_ready(path))

    def test_frame_count_must_match_samples(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'wrongframes.aif'; data=bytearray(fixture())
            data[22:26]=struct.pack('>I',64)
            path.write_bytes(data)
            self.assertFalse(_aiff_ready(path))

    def test_float_intermediate_cannot_enter_pcm24_limiter(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'float.aif'; path.write_bytes(fixture(bits=32,compression=b'fl32'))
            with self.assertRaisesRegex(ValueError,'PCM24'):
                _aiff_ready(path)

    def test_zero_frame_placeholder_is_not_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'empty.aif'; path.write_bytes(fixture(frames=0))
            self.assertFalse(_aiff_ready(path))


if __name__=='__main__':
    unittest.main()
