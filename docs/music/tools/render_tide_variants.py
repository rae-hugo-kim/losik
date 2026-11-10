"""Serial Logic production and bounded WAV mastering for the four Tide variants."""
from pathlib import Path
import hashlib
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import time
import pipeline as p
import returning_tide as base
from tide_variants import IDS, SKETCHES

BOUNCES = Path('/Volumes/Netac 2TB/music/bounces')
PROJECTS = Path('/Volumes/Netac 2TB/music/projects')


def close_owned_project():
    titles = [w for w in p.windows() if w.endswith('- 트랙')]
    allowed = ['Returning Tide Astra v1', 'Paper Lanterns Astra v1', 'Blue Window Astra v1',
               'Northbound Lights Astra v1', 'After the Rain Astra v1']
    for title in titles:
        assert any(title in (x + ' - 트랙', x + '.logicx - 트랙') for x in allowed), ('Unexpected project', title)
        rc, out, err = p.osa(f'''tell application "System Events" to tell process "{p.APP}"
set frontmost to true
perform action "AXRaise" of window "{title}"
click menu bar item "파일" of menu bar 1
delay 0.3
click menu item "저장" of menu 1 of menu bar item "파일" of menu bar 1
delay 2
keystroke "w" using command down
delay 2
repeat with w in windows
try
if (name of buttons of w) contains "저장하지 않음" then click button "저장" of w
end try
end repeat
end tell''', timeout=60)
        assert rc == 0, (out, err)
    assert p.wait_window('- 트랙', present=False, timeout=30), p.windows()


def control_bar():
    rc, out, err = p.osa(f'''on walk(el, depth)
tell application "System Events"
if depth > 5 then return ""
set s to ""
try
set s to (role of el as text) & "|" & (description of el as text)
try
set s to s & "|" & (value of el as text)
end try
set s to s & linefeed
end try
try
repeat with c in every UI element of el
set s to s & my walk(c, depth + 1)
end repeat
end try
return s
end tell
end walk
tell application "System Events" to tell process "{p.APP}"
set out to ""
repeat with w in windows
if (name of w) ends with "- 트랙" then
repeat with e in every UI element of w
try
if description of e is "컨트롤 막대" then set out to out & my walk(e, 0)
end try
end repeat
end if
end repeat
return out
end tell''', timeout=60)
    assert rc == 0, err
    return out


def wave_data(file):
    assert file.read(12)[8:] == b'WAVE'
    rate = channels = bits = None
    while True:
        header = file.read(8)
        assert len(header) == 8
        kind, size = struct.unpack('<4sI', header)
        if kind == b'fmt ':
            payload = file.read(size)
            _, channels, rate, _, align, bits = struct.unpack_from('<HHIIHH', payload)
            assert align == channels * bits // 8
            file.seek(size & 1, 1)
        elif kind == b'data':
            return file.tell(), size, rate, channels, bits
        else:
            file.seek(size + (size & 1), 1)


def fade_release(path):
    with path.open('r+b') as file:
        begin, size, rate, channels, bits = wave_data(file)
        assert (channels, bits) == (2, 24)
        assert os.fstat(file.fileno()).st_size >= begin + size
        frames = rate // 10
        offset = begin + size - frames * 6
        file.seek(offset)
        tail = bytearray(file.read(frames * 6))
        for frame in range(frames):
            gain = (frames - 1 - frame) / (frames - 1)
            for channel in range(2):
                at = frame * 6 + channel * 3
                value = int.from_bytes(tail[at:at + 3], 'little', signed=True)
                tail[at:at + 3] = round(value * gain).to_bytes(3, 'little', signed=True)
        file.seek(offset)
        assert file.write(tail) == len(tail)
        file.flush()
        os.fsync(file.fileno())


def measure(path):
    with path.open('rb') as file:
        begin, size, rate, channels, bits = wave_data(file)
        assert (rate, channels, bits) == (48000, 2, 24)
        assert os.fstat(file.fileno()).st_size == begin + size
        frames = size // 6
        assert frames == 12902400, ('Wrong duration', frames / rate)
        bucket_frames = rate // 4
        energies, peaks, clipped = [], [0, 0], 0
        zero_blocks = []
        while raw := file.read(bucket_frames * 6):
            bucket_start = len(energies) * bucket_frames
            if rate <= bucket_start < frames - rate and not any(raw):
                zero_blocks.append(bucket_start / rate)
            energy = 0
            for at in range(0, len(raw), 3):
                value = int.from_bytes(raw[at:at + 3], 'little', signed=True)
                channel = (at // 3) % 2
                peaks[channel] = max(peaks[channel], abs(value))
                clipped += abs(value) >= 8388607
                energy += (value / 8388608) ** 2
            energies.append(energy / (len(raw) // 3))
        file.seek(begin + size - 6)
        assert file.read(6) == b'\x00' * 6
    assert not zero_blocks, ('Unexpected all-zero 250ms audio blocks', zero_blocks)
    def level(start, end):
        values = energies[round(start * 4):round(end * 4)]
        return round(10 * math.log10(sum(values) / len(values) + 1e-15), 2)
    levels = {name: level((bar - 1) * 2.4, (bar - 1 + length) * 2.4) for bar, length, name in base.SECTIONS}
    impact = {str(bar): round(level((bar - 1) * 2.4, (bar - 1) * 2.4 + 1)
                             - level((bar - 1) * 2.4 - 1, (bar - 1) * 2.4), 2) for bar in (41, 73, 89)}
    hasher = hashlib.sha256()
    with path.open('rb') as file:
        while chunk := file.read(1024 * 1024):
            hasher.update(chunk)
    digest = hasher.hexdigest()
    result = dict(path=str(path), bytes=path.stat().st_size, sha256=digest, sample_rate=rate,
                  channels=channels, bits=bits, frames=frames, seconds=frames / rate,
                  peak_dbfs=[round(20 * math.log10(n / 8388608 + 1e-15), 3) for n in peaks],
                  full_scale_samples=clipped, section_rms_dbfs=levels, chorus_impact_db=impact,
                  final_first_half_dbfs=level(88 * 2.4, 96 * 2.4), climax_dbfs=level(96 * 2.4, 104 * 2.4),
                  last_second_dbfs=level(267.8, 268.8), final_frame=[0, 0], release_fade_ms=100,
                  all_zero_internal_blocks=zero_blocks)
    assert clipped == 0 and max(result['peak_dbfs']) <= -.1
    return result


def render(slug):
    assert slug in IDS
    data = json.loads((SKETCHES / (slug + '.json')).read_text())
    title = data['title'] + ' Astra v1'
    mid = SKETCHES / (slug + '.mid')
    destination = PROJECTS / (title + '.logicx')
    aiff, wav = BOUNCES / (slug + '.aif'), BOUNCES / (slug + '.wav')
    assert mid.exists() and not destination.exists() and not aiff.exists() and not wav.exists()
    assert not (SKETCHES / (title + '.logicx')).exists()
    close_owned_project()
    print(slug, 'importing MIDI', flush=True)
    assert p.open_mid(str(mid), timeout=240), p.windows()
    metro = p.metronome_off('무제 - 트랙')
    print('metronome', metro, flush=True)
    controls = control_bar()
    assert 'AXSlider|템포|100.0' in controls and 'AXPopUpButton|박자표|4/4' in controls
    assert 'D 메이저' in controls
    p.open_mixer()
    strips = p.mixer_strips()
    print('patches', strips, flush=True)
    assert strips.count('[Studio Grand]') == 2
    for name in ('SoCal', 'Simple Foundation', 'Acoustic Guitar', 'Authentic Strings', 'Deluxe Classic', 'Hard Rock'):
        assert '[' + name + ']' in strips
    assert 'GM 기기' not in strips
    ok, msg = p.save_project_as(title)
    assert ok, msg
    print('project saved', title, flush=True)
    ok, msg = p.start_bounce_aiff(title, slug)
    assert ok, msg
    print('bounce started', flush=True)
    assert p.wait_file_stable(str(aiff), min_size=77000000, timeout=360), str(aiff)
    info = subprocess.run(['afinfo', str(aiff)], capture_output=True, text=True, check=True).stdout
    assert '268.800000' in info and '24-bit' in info and '48000' in info, info
    close_owned_project()
    source = SKETCHES / (title + '.logicx')
    if source.exists():
        assert not destination.exists()
        shutil.move(str(source), str(destination))
    assert (destination / 'Alternatives/000/ProjectData').is_file()
    print('preserved', destination, flush=True)
    limited = p.limit_aiff(str(aiff))
    print('limiter samples', limited, flush=True)
    ok, error = p.aiff_to_wav(str(aiff), str(wav))
    assert ok, error
    fade_release(wav)
    metrics = measure(wav)
    metrics.update(title=title, project=str(destination), metronome=metro,
                   observed_patches=strips, control_bar=controls, limiter_samples=limited)
    path = SKETCHES / (slug + '-verification.json')
    path.write_text(json.dumps(metrics, indent=2) + '\n')
    print(json.dumps(metrics, indent=2), flush=True)
    subprocess.run(['afplay', '-t', '5', str(wav)], check=True, timeout=30)
    print('COMPLETE', slug, flush=True)
    return metrics


if __name__ == '__main__':
    for slug in sys.argv[1:]:
        render(slug)
