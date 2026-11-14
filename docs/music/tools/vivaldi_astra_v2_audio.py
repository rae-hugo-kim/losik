"""Read-only PCM proof for the Vivaldi Astra v2 bounces.

`measure()` verifies one stereo PCM24 RIFF/WAVE file (44.1 or 48 kHz) in a
single sequential, bounded read: the header chunks are walked first with small
seeks, then the file is streamed once from byte 0 to EOF, feeding SHA-256 and
the frame-aligned audio analysis together. No float lists, no mmap, no second
pass over the PCM. The source file is only ever opened with mode 'rb'.

Checks (failure codes in brackets):
  * strict RIFF/WAVE layout, chunk bounds vs. physical size, PCM24 stereo
    [riff_*, chunk_*, fmt_*, data_*]
  * length within [expected - 0.1 s, expected + 12 s]; +12 s allows Logic's
    release tail, -0.1 s never accepts a missing final bar [length]
  * peak of both channels <= -0.1 dBFS [ceiling]
  * both channels carry meaningful signal: peak >= -40 dBFS and RMS >= -70 dBFS
    [channel_silent]
  * every section RMS > -70 dBFS [section_silent], plus boundary deltas
    (RMS of 0.5 s after a section start minus 0.5 s before it)
  * every run of >= 100 ms of exact all-zero stereo frames is reported, merged
    across read-chunk boundaries; a run is unexpected when it overlaps an
    active MIDI interval after ignoring the first 10 ms of that interval
    [unexpected_zero_run]. The 10 ms onset tolerance covers sampler start
    latency / sample-start offsets in the rendered instrument, which can leave
    true digital zero for a few ms after a note-on that follows silence; it
    never excuses a dropout inside a sounding note.

Run (from the repository root):
  python3 docs/music/tools/vivaldi_astra_v2_audio.py \
      --output docs/music/vivaldi_astra_v2_audio.json [--sids vs-spring1-astra ...]
  python3 -m unittest discover -s docs/music/tools -p 'test_vivaldi_astra_v2_audio.py'
"""
import argparse
import audioop
import hashlib
import json
import math
import os
import re
import struct
import sys
from pathlib import Path

FRAME_BYTES = 6
CHUNK_FRAMES = 65536
CHUNK_BYTES = CHUNK_FRAMES * FRAME_BYTES
FULL_SCALE = 8388608.0
CEILING_DBFS = -0.1
# Largest integer sample magnitude that still satisfies peak <= -0.1 dBFS.
CEILING_SAMPLE = int(FULL_SCALE * 10 ** (CEILING_DBFS / 20))
MIN_CHANNEL_PEAK_DBFS = -40.0
MIN_CHANNEL_RMS_DBFS = -70.0
MIN_SECTION_RMS_DBFS = -70.0
LENGTH_WINDOW = (-0.1, 12.0)
MIN_ZERO_RUN_SECONDS = 0.1
ONSET_TOLERANCE_SECONDS = 0.010
BOUNDARY_WINDOW_SECONDS = 0.5
RATES = (44100, 48000)
PCM_GUID = bytes.fromhex('0100000000001000800000aa00389b71')
_ZERO_BYTES = re.compile(b'\x00{6,}')


class AudioCheckError(Exception):
    """A file failed the audio contract; `failures` lists 'code: detail' strings."""

    def __init__(self, path, failures, evidence=None):
        self.path = str(path)
        self.failures = list(failures)
        self.evidence = evidence
        super().__init__(f'{self.path}: ' + '; '.join(self.failures))


def _dbfs(amplitude):
    # Finite floor keeps the report strict-JSON for digital silence.
    return round(20 * math.log10(max(amplitude / FULL_SCALE, 1e-15)), 3)


def _read_exact(file, size, path, what):
    raw = file.read(size)
    if len(raw) != size:
        raise AudioCheckError(path, [f'{what}: expected {size} bytes, read {len(raw)}'])
    return raw


def _parse_header(file, physical, path):
    """Walk every chunk against the physical size; return (data_offset, data_bytes, rate, tag)."""
    head = _read_exact(file, 12, path, 'riff_header')
    if head[:4] != b'RIFF' or head[8:] != b'WAVE':
        raise AudioCheckError(path, [f'riff_header: not RIFF/WAVE ({head[:4]!r}/{head[8:]!r})'])
    failures = []
    declared = struct.unpack_from('<I', head, 4)[0] + 8
    if declared != physical:
        failures.append(f'riff_length: RIFF declares {declared} bytes, file has {physical}')
    position, fmt, data = 12, None, None
    while position < physical:
        if position + 8 > physical:
            failures.append(f'chunk_header_truncated: {physical - position} trailing bytes at offset {position}')
            break
        file.seek(position)
        kind, size = struct.unpack('<4sI', _read_exact(file, 8, path, 'chunk_header'))
        body = position + 8
        end = body + size + (size & 1)
        if kind == b'data':
            if fmt is None:
                failures.append(f'data_before_fmt: data chunk at offset {position}')
            if data is not None:
                failures.append(f'data_duplicate: second data chunk at offset {position}')
            if body + size > physical:
                failures.append(f'data_truncated: data declares {size} bytes at offset {body}, '
                                f'only {physical - body} physically present')
            if size == 0 or size % FRAME_BYTES:
                failures.append(f'data_alignment: {size} bytes is not a positive multiple of {FRAME_BYTES}')
            data = (body, size)
        elif kind == b'fmt ':
            if fmt is not None:
                failures.append(f'fmt_duplicate: second fmt chunk at offset {position}')
            if size < 16 or body + size > physical:
                failures.append(f'fmt_invalid: size {size} at offset {position}')
                break
            fields = struct.unpack('<HHIIHH', _read_exact(file, 16, path, 'fmt'))
            tag, channels, rate, byte_rate, align, bits = fields
            if tag not in (1, 0xFFFE):
                failures.append(f'fmt_tag: {tag:#06x} is not PCM/extensible')
            if channels != 2 or bits != 24 or align != FRAME_BYTES:
                failures.append(f'fmt_layout: channels={channels} bits={bits} block_align={align}, '
                                f'expected stereo PCM24 block_align 6')
            if rate not in RATES:
                failures.append(f'fmt_rate: {rate} Hz not in {RATES}')
            if byte_rate != rate * FRAME_BYTES:
                failures.append(f'fmt_byte_rate: {byte_rate} != {rate} * {FRAME_BYTES}')
            if tag == 0xFFFE:
                if size < 40:
                    failures.append(f'fmt_extensible: size {size} < 40')
                else:
                    extra, valid, mask = struct.unpack('<HHI', _read_exact(file, 8, path, 'fmt_ext'))
                    guid = _read_exact(file, 16, path, 'fmt_guid')
                    if extra < 22 or valid != 24 or mask != 3 or guid != PCM_GUID:
                        failures.append(f'fmt_extensible: cbSize={extra} valid_bits={valid} '
                                        f'mask={mask:#x} subformat={guid.hex()}')
            fmt = (tag, rate)
        if end > physical and kind != b'data':
            failures.append(f'chunk_truncated: {kind!r} declares {size} bytes at offset {position}')
            break
        if end > physical:
            break
        position = end
    if fmt is None:
        failures.append('fmt_missing: no fmt chunk')
    if data is None:
        failures.append('data_missing: no data chunk')
    if failures:
        raise AudioCheckError(path, failures)
    return data[0], data[1], fmt[1], fmt[0]


def _validate_intervals(active_intervals):
    intervals = []
    for item in active_intervals:
        start, end = float(item[0]), float(item[1])
        if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end):
            raise ValueError(f'invalid active interval {item!r}')
        if intervals and start < intervals[-1][1]:
            raise ValueError(f'active intervals must be sorted and merged: {item!r} after {intervals[-1]!r}')
        intervals.append((start, end))
    return intervals


def _validate_sections(sections, expected):
    out, names = [], set()
    for section in sections:
        name, start, end = section['name'], float(section['start']), float(section['end'])
        if name in names:
            raise ValueError(f'duplicate section name {name!r}')
        if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end <= expected + 1e-9):
            raise ValueError(f'invalid section {section!r} for expected length {expected}')
        names.add(name)
        out.append((name, start, end))
    if not out:
        raise ValueError('sections must not be empty')
    return out


def _windows(sections, rate, frames):
    """Frame windows for section RMS and boundary deltas: name -> [first, last, energy, samples]."""
    windows, failures = {}, []
    half = round(BOUNDARY_WINDOW_SECONDS * rate)
    for index, (name, start, end) in enumerate(sections):
        first, last = round(start * rate), min(frames, round(end * rate))
        if first >= last:
            failures.append(f'section_out_of_range: {name} [{start}, {end}) s beyond {frames} frames')
            continue
        windows[('section', name)] = [first, last, 0.0, 0]
        if index:
            windows[('after', name)] = [first, min(frames, first + half), 0.0, 0]
            windows[('before', name)] = [max(0, first - half), first, 0.0, 0]
    return windows, failures


def _window_rms(window):
    first, last, energy, samples = window
    return _dbfs(math.sqrt(energy / samples)) if samples else None


def measure(path, expected_seconds, sections, active_intervals):
    """Verify one bounce and return its JSON-serialisable evidence.

    sections: [{name, start, end}] in seconds; active_intervals: sorted, merged
    [(start, end)] seconds of actual MIDI note durations. Raises ValueError for
    invalid caller inputs and AudioCheckError (with evidence when available)
    when the file violates the audio contract.
    """
    path = Path(path)
    expected = float(expected_seconds)
    if not (math.isfinite(expected) and expected > 0):
        raise ValueError(f'invalid expected_seconds {expected_seconds!r}')
    intervals = _validate_intervals(active_intervals)
    section_list = _validate_sections(sections, expected)
    if not path.is_file():
        raise AudioCheckError(path, ['missing_file: no regular file at path'])
    with path.open('rb') as file:
        before = os.fstat(file.fileno())
        physical = before.st_size
        begin, size, rate, tag = _parse_header(file, physical, path)
        frames = size // FRAME_BYTES
        windows, failures = _windows(section_list, rate, frames)
        hasher = hashlib.sha256()
        peaks, energy = [0, 0], [0.0, 0.0]
        min_run = round(MIN_ZERO_RUN_SECONDS * rate)
        runs, pending = [], None
        file.seek(0)
        hasher.update(_read_exact(file, begin, path, 'pre_data'))
        frame = 0
        while frame < frames:
            count = min(CHUNK_FRAMES, frames - frame)
            raw = _read_exact(file, count * FRAME_BYTES, path, f'data_read at frame {frame}')
            hasher.update(raw)
            stop = frame + count
            for channel in (0, 1):
                mono = audioop.tomono(raw, 3, float(channel == 0), float(channel == 1))
                peaks[channel] = max(peaks[channel], audioop.max(mono, 3))
                rms = audioop.rms(mono, 3)
                energy[channel] += float(rms) * rms * count
            for window in windows.values():
                a, b = max(window[0], frame), min(window[1], stop)
                if a < b:
                    rms = audioop.rms(raw[(a - frame) * FRAME_BYTES:(b - frame) * FRAME_BYTES], 3)
                    window[2] += float(rms) * rms * (b - a) * 2
                    window[3] += (b - a) * 2
            # Chunks are frame-aligned, so whole all-zero frames inside a zero-byte
            # run are [ceil(start/6), floor(end/6)); runs touching the previous
            # chunk's end are merged so a dropout split by the read size is whole.
            for match in _ZERO_BYTES.finditer(raw):
                a = frame + (match.start() + FRAME_BYTES - 1) // FRAME_BYTES
                b = frame + match.end() // FRAME_BYTES
                if a >= b:
                    continue
                if pending and pending[1] == a:
                    pending[1] = b
                    continue
                if pending and pending[1] - pending[0] >= min_run:
                    runs.append(tuple(pending))
                pending = [a, b]
            frame = stop
        if pending and pending[1] - pending[0] >= min_run:
            runs.append(tuple(pending))
        position = begin + size
        while position < physical:
            raw = _read_exact(file, min(CHUNK_BYTES, physical - position), path, 'post_data')
            hasher.update(raw)
            position += len(raw)
        if file.read(1):
            failures.append('file_changed: file grew during the read')
        after = os.fstat(file.fileno())
        if (after.st_size, after.st_mtime_ns) != (before.st_size, before.st_mtime_ns):
            failures.append('file_changed: size/mtime changed during the read')

    seconds = frames / rate
    delta = seconds - expected
    if not LENGTH_WINDOW[0] - 1e-9 <= delta <= LENGTH_WINDOW[1] + 1e-9:
        failures.append(f'length: {seconds:.6f} s vs expected {expected:.6f} s '
                        f'(delta {delta:+.6f}, allowed {LENGTH_WINDOW[0]:+}..{LENGTH_WINDOW[1]:+})')
    peak_dbfs = [_dbfs(p) for p in peaks]
    channel_rms = [_dbfs(math.sqrt(e / frames)) for e in energy]
    for channel, name in enumerate(('left', 'right')):
        if peaks[channel] > CEILING_SAMPLE:
            failures.append(f'ceiling: {name} peak {peak_dbfs[channel]} dBFS '
                            f'({peaks[channel]}) > {CEILING_DBFS} dBFS ({CEILING_SAMPLE})')
        if peak_dbfs[channel] < MIN_CHANNEL_PEAK_DBFS or channel_rms[channel] < MIN_CHANNEL_RMS_DBFS:
            failures.append(f'channel_silent: {name} peak {peak_dbfs[channel]} dBFS, '
                            f'RMS {channel_rms[channel]} dBFS (need peak >= {MIN_CHANNEL_PEAK_DBFS}, '
                            f'RMS >= {MIN_CHANNEL_RMS_DBFS})')
    levels, section_frames, boundaries = {}, {}, {}
    for name, _, _ in section_list:
        window = windows.get(('section', name))
        if window is None:
            continue
        levels[name] = _window_rms(window)
        section_frames[name] = window[:2]
        if levels[name] <= MIN_SECTION_RMS_DBFS:
            failures.append(f'section_silent: {name} RMS {levels[name]} dBFS <= {MIN_SECTION_RMS_DBFS}')
        if ('after', name) in windows:
            after_rms = _window_rms(windows[('after', name)])
            before_rms = _window_rms(windows[('before', name)])
            if after_rms is not None and before_rms is not None:
                boundaries[name] = round(after_rms - before_rms, 3)
    zero_runs, unexpected = [], []
    pointer = 0
    for first, last in runs:
        a, b = first / rate, last / rate
        run = dict(start_frame=first, end_frame=last, start=round(a, 6), end=round(b, 6),
                   seconds=round(b - a, 6))
        zero_runs.append(run)
        while pointer < len(intervals) and intervals[pointer][1] <= a:
            pointer += 1
        index = pointer
        while index < len(intervals) and intervals[index][0] < b:
            start, end = intervals[index]
            overlap = min(b, end) - max(a, start + ONSET_TOLERANCE_SECONDS)
            if overlap > 0:
                unexpected.append(dict(run, interval=[round(start, 6), round(end, 6)],
                                       overlap_seconds=round(overlap, 6)))
            index += 1
    for run in unexpected:
        failures.append(f"unexpected_zero_run: {run['start']}-{run['end']} s overlaps active "
                        f"{run['interval'][0]}-{run['interval'][1]} s by {run['overlap_seconds']} s")
    result = dict(
        path=str(path), sha256=hasher.hexdigest(), bytes=physical, format_tag=tag,
        data_offset=begin, data_bytes=size, sample_rate=rate, channels=2, bits=24,
        frames=frames, seconds=round(seconds, 6), expected_seconds=round(expected, 6),
        length_delta_seconds=round(delta, 6), length_window_seconds=list(LENGTH_WINDOW),
        peak_samples=peaks, peak_dbfs=peak_dbfs, ceiling_dbfs=CEILING_DBFS,
        channel_rms_dbfs=channel_rms, section_rms_dbfs=levels, section_frames=section_frames,
        boundary_delta_db=boundaries, boundary_window_seconds=BOUNDARY_WINDOW_SECONDS,
        active_interval_count=len(intervals),
        active_seconds=round(sum(end - start for start, end in intervals), 6),
        min_zero_run_seconds=MIN_ZERO_RUN_SECONDS, onset_tolerance_seconds=ONSET_TOLERANCE_SECONDS,
        zero_runs=zero_runs, unexpected_zero_runs=unexpected)
    if failures:
        raise AudioCheckError(path, failures, result)
    return result


def sketch_inputs(composer, sketch):
    """(expected_seconds, sections, active_intervals) derived from the composer's own data."""
    seconds_per_tick = 60.0 / sketch['bpm'] / composer.PPQ
    bar = composer.ticks(sketch)
    end_tick = sketch['bars'] * bar
    marks = composer.sections(sketch)
    sections = []
    for index, (start_bar, name) in enumerate(marks):
        stop_bar = marks[index + 1][0] if index + 1 < len(marks) else sketch['bars'] + 1
        sections.append(dict(name=name, start=(start_bar - 1) * bar * seconds_per_tick,
                             end=(stop_bar - 1) * bar * seconds_per_tick))
    nt = composer.compose(sketch['sid'])[0]
    merged = []
    for start, end in sorted((t, t + d) for notes in nt.values() for t, d, _, _ in notes):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    intervals = [(a * seconds_per_tick, b * seconds_per_tick) for a, b in merged]
    return end_tick * seconds_per_tick, sections, intervals


def main(argv=None):
    tools = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description='Verify Vivaldi Astra v2 bounces (read-only).')
    parser.add_argument('--output', type=Path, default=tools.parent / 'vivaldi_astra_v2_audio.json')
    parser.add_argument('--sids', nargs='+', help='subset of composer sids (default: all)')
    args = parser.parse_args(argv)
    sys.path.insert(0, str(tools))
    import vivaldi_astra_v2 as composer
    from pipeline import BOUNCE_DIR, PROJ_DIR
    known = {s['sid']: s for s in composer.SKETCHES}
    wanted = args.sids or list(known)
    missing = [sid for sid in wanted if sid not in known]
    if missing:
        parser.error(f'unknown sids: {missing}; known: {sorted(known)}')
    results, errors = [], []
    for sid in wanted:
        sketch = known[sid]
        wav = Path(BOUNCE_DIR) / f'{sid}-v2.wav'
        project = Path(PROJ_DIR) / f"{sketch['title']} v2.logicx"
        expected, sections, intervals = sketch_inputs(composer, sketch)
        entry = dict(sid=sid, title=sketch['title'], meter=list(sketch['meter']), bpm=sketch['bpm'],
                     bars=sketch['bars'], project=str(project))
        failures = [] if project.is_dir() else [f'project_missing: {project}']
        try:
            entry.update(measure(wav, expected, sections, intervals))
        except AudioCheckError as error:
            failures.extend(error.failures)
            entry.update(error.evidence or dict(path=str(wav)))
        if failures:
            entry['failures'] = failures
            errors.append(dict(sid=sid, path=str(wav), failures=failures))
        results.append(entry)
        status = 'PASS' if not failures else 'FAIL ' + '; '.join(failures)
        print(f'{sid} {wav} {status}', flush=True)
    report = dict(model=composer.MODEL, sids=wanted, passed=not errors, results=results, errors=errors)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(args.output.name + '.tmp')
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(args.output)
    print(f'wrote {args.output} {"PASS" if not errors else f"FAIL {len(errors)}/{len(wanted)}"}')
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
