"""Build Astra Air Harmonica from pinned CC0 VCSL acoustic recordings.

Run with Apple Python 3.9; no synthesis engine or Logic actions.
Native EXS export downloads five checksum-pinned, stdlib-only exstools4 modules
into an automatically removed temporary directory; rebuilding requires network.
SoundFont layout follows E-mu SoundFont 2.04 specification sections 5-8:
https://www.synthfont.com/sfspec24.pdf
The bank uses the compatible 2.01 subset with embedded signed 16-bit PCM.
The native EXS references the original 24-bit WAV files without conversion.
"""
import argparse
import audioop
import hashlib
import io
import json
import math
import struct
import sys
import urllib.request
import wave
from array import array
from pathlib import Path


REVISION = 'c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e'
BASE = 'https://raw.githubusercontent.com/sgossner/VCSL/' + REVISION + '/'
SOURCE = BASE + 'Aerophones/Free%20Aerophones/Harmonica-Hohner-Special20-C/Sustains/'
ASSETS = Path('/Volumes/Netac 2TB/music/samples/astra-harmonica')
BANK = Path.home() / 'Music/Audio Music Apps/Sampler Instruments/Astra Air Harmonica.sf2'
NAME = 'Astra Air Harmonica'
KEY_RANGE = (57, 81)
RELEASE = round(1200 * math.log2(0.1))
# VCSL uses C3 for sounding MIDI 60, not scientific C3/MIDI 48.
# Normal G3 is absent upstream: its adjacent real recordings cover that range.
SOURCES = (
    ('Soft', 'C3', 60, '153bcdac7034efd36de628d213c84e82b874b139867d17a0c96a674cf04e3869'),
    ('Soft', 'E3', 64, 'dfcbf52023602d4b094d9ecb8f357c4b682ce082d6bac5491baeac9c8ff2cc5e'),
    ('Soft', 'G3', 67, 'ccdb93e6620aee149252533fc57e4438d4ed282aa6047e9a69ad5303bf9b0eac'),
    ('Soft', 'C4', 72, '6512cb328be4e85ad3dd2977e62b14a19d051845533eb7e9ecac12ddfd1a28e1'),
    ('Soft', 'E4', 76, '15c8d89bd57186d6b41c7ce8e162974caf26eb09ec703c20f6a53a41d8867cce'),
    ('Soft', 'G4', 79, '7657ee0e276593728619442b3211da7dd6ecb1d6ebbcd3ca07427bd348df31a1'),
    ('Normal', 'C3', 60, 'bca5969e869166a45740fc5438808eab521479d992ba681d6f92b373d388a317'),
    ('Normal', 'E3', 64, 'c3d18cffbf25e04beddbf324facd0e9364c9a9b8e2abd4ecb4b6c952b1e4e2b8'),
    ('Normal', 'C4', 72, 'ffb181bf9db1e30eb1b4824a9e923c6c81bd0c411143996639fe829131a47744'),
    ('Normal', 'E4', 76, '48675fa7d387f25b6f32e797521746bb88f319858a04b56a250c759cb895adb6'),
    ('Normal', 'G4', 79, 'dccdd63466082c9a9ed6ec6cc6990b10cf36865a9cc59eb294edd1476fff409b'),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def chunk(identifier, payload):
    return identifier + struct.pack('<I', len(payload)) + payload + b'\0' * (len(payload) & 1)


def riff_list(kind, parts):
    return chunk(b'LIST', kind + b''.join(parts))


def text(value):
    data = value.encode('ascii') + b'\0'
    return data + b'\0' * (len(data) & 1)


def name20(value):
    data = value.encode('ascii')
    require(len(data) < 20, 'SoundFont name exceeds 19 bytes')
    return data.ljust(20, b'\0')


def generator(op, value):
    return struct.pack('<HH', op, value & 0xffff)


def pitch_measurement(pcm16, rate):
    """Find first convincing full-rate period; harmonica overtones defeat decimation."""
    values = array('h', pcm16[int(.5 * rate) * 2:int(.6 * rate) * 2])
    if sys.byteorder != 'little':
        values.byteswap()
    energy = sum(value * value for value in values) / len(values)
    require(energy > 0, 'Silent pitch-analysis window')
    errors = {}
    for lag in range(int(rate / 1000), int(rate / 180) + 2):
        count = len(values) - lag
        errors[lag] = sum((values[i] - values[i + lag]) ** 2 for i in range(count)) / (count * 2 * energy)
    candidates = [lag for lag in range(min(errors) + 1, max(errors))
                  if errors[lag] < .06 and errors[lag] < errors[lag - 1]
                  and errors[lag] < errors[lag + 1]]
    require(bool(candidates), 'No convincing harmonica fundamental in 180-1000 Hz')
    lag = candidates[0]
    left, middle, right = errors[lag - 1], errors[lag], errors[lag + 1]
    refined = lag + .5 * (left - right) / (left - 2 * middle + right)
    frequency = rate / refined
    return {'frequency_hz': round(frequency, 3),
            'midi_note': round(69 + 12 * math.log2(frequency / 440), 4),
            'normalized_period_error': round(middle, 6),
            'method': 'Full-rate normalized squared-difference period, 0.5-0.6 s; parabolic refinement'}


def zone_range(layer, root):
    roots = [entry[2] for entry in SOURCES if entry[0] == layer]
    index = roots.index(root)
    low = KEY_RANGE[0] if index == 0 else (roots[index - 1] + root) // 2 + 1
    high = KEY_RANGE[1] if index == len(roots) - 1 else (root + roots[index + 1]) // 2
    return low, high


def prepare_samples(assets):
    samples = []
    for layer, note, root, expected_hash in SOURCES:
        filename = 'Hohner-Special20_' + layer + '_' + note + '.wav'
        url = SOURCE + layer + '/' + filename
        path = assets / layer / filename
        if path.exists():
            original = path.read_bytes()
        else:
            with urllib.request.urlopen(url, timeout=60) as response:
                original = response.read()
        require(hashlib.sha256(original).hexdigest() == expected_hash, 'Source checksum mismatch: ' + filename)
        with wave.open(io.BytesIO(original)) as source:
            require(source.getnchannels() == 1 and source.getsampwidth() in (2, 3), 'Expected mono 16/24-bit source')
            rate, width, frames = source.getframerate(), source.getsampwidth(), source.getnframes()
            pcm = source.readframes(frames)
        require(len(pcm) == frames * width, 'Truncated source PCM')
        pcm16 = audioop.lin2lin(pcm, width, 2) if width != 2 else pcm
        pitch = pitch_measurement(pcm16, rate)
        require(abs(pitch['midi_note'] - root) < .15, 'Recorded pitch does not match root: ' + filename)
        low, high = zone_range(layer, root)
        fastest = 2 ** ((high - root) / 12)
        require(frames / rate / fastest >= 3.1, 'Sample too short at upper mapped key')
        # Check real recorded sustain, not merely trailing file silence, at the
        # worst transposition after a three-second note plus the release time.
        end_window = int(3.1 * fastest * rate)
        rms_end = audioop.rms(pcm16[(end_window - int(.1 * rate)) * 2:end_window * 2], 2)
        sustain_db = 20 * math.log10(max(rms_end, 1) / 32768)
        require(sustain_db > -45, 'Insufficient natural sustain at upper mapped key: ' + filename)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(original)
        samples.append({'name': layer + '_' + note, 'source_file': str(path),
                        'source_url': url, 'source_sha256': expected_hash,
                        'source_format': {'channels': 1, 'bits': width * 8, 'sample_rate': rate},
                        'source_filename_note': note, 'root_midi': root,
                        'key_range': [low, high], 'velocity_range': [1, 88] if layer == 'Soft' else [89, 127],
                        'duration_seconds': round(frames / rate, 6),
                        'shortest_mapped_duration_seconds': round(frames / rate / fastest, 6),
                        'worst_key_3_1s_sustain_dbfs': round(sustain_db, 2),
                        'peak_dbfs': round(20 * math.log10(audioop.max(pcm16, 2) / 32768), 2),
                        'pitch_verification': pitch, 'pcm16': pcm16})
    return samples


def make_soundfont(samples):
    data, headers, bags, generators = bytearray(), [], [], []
    for sample_id, sample in enumerate(samples):
        start = len(data) // 2
        data.extend(sample['pcm16'])
        end = len(data) // 2
        data.extend(b'\0' * 92)  # Required 46 zero sample points, excluded from dwEnd.
        headers.append(struct.pack('<20sIIIIIBbHH', name20(sample['name']),
                                   start, end, start + 8, end - 8,
                                   sample['source_format']['sample_rate'], sample['root_midi'], 0, 0, 1))
        bags.append(struct.pack('<HH', len(generators), 0))
        low, high = sample['key_range']
        vlow, vhigh = sample['velocity_range']
        # Ranges first; terminal sampleID last. The recorded attack stays intact.
        generators.extend([generator(43, low | (high << 8)), generator(44, vlow | (vhigh << 8)),
                           generator(33, -12000), generator(34, round(1200 * math.log2(.003))),
                           generator(35, -12000), generator(36, -12000), generator(37, 0),
                           generator(38, RELEASE), generator(48, 30), generator(54, 0),
                           generator(56, 100), generator(58, sample['root_midi']), generator(53, sample_id)])
    bags.append(struct.pack('<HH', len(generators), 0))
    generators.append(generator(0, 0))
    headers.append(struct.pack('<20sIIIIIBbHH', name20('EOS'), 0, 0, 0, 0, 0, 0, 0, 0, 0))
    info = riff_list(b'INFO', [chunk(b'ifil', struct.pack('<HH', 2, 1)),
                             chunk(b'isng', text('EMU8000')), chunk(b'INAM', text(NAME)),
                             chunk(b'IENG', text('VCSL / Versilian Studios; Astra mapping')),
                             chunk(b'ICOP', text('CC0 1.0 Universal; source recordings by Versilian Studios LLC')),
                             chunk(b'ICMT', text('Real Hohner Special20 C; Soft/Normal; MIDI57-81; unlooped; 100ms release; no gain boost')),
                             chunk(b'ISFT', text('build_air_harmonica.py'))])
    sdta = riff_list(b'sdta', [chunk(b'smpl', bytes(data))])
    pdta = riff_list(b'pdta', [
        chunk(b'phdr', struct.pack('<20sHHHIII', name20(NAME), 0, 0, 0, 0, 0, 0)
              + struct.pack('<20sHHHIII', name20('EOP'), 0, 0, 1, 0, 0, 0)),
        chunk(b'pbag', struct.pack('<HHHH', 0, 0, 1, 0)),
        chunk(b'pmod', b'\0' * 10), chunk(b'pgen', generator(41, 0) + generator(0, 0)),
        chunk(b'inst', struct.pack('<20sH', name20(NAME), 0)
              + struct.pack('<20sH', name20('EOI'), len(samples))),
        chunk(b'ibag', b''.join(bags)), chunk(b'imod', b'\0' * 10),
        chunk(b'igen', b''.join(generators)), chunk(b'shdr', b''.join(headers))])
    return chunk(b'RIFF', b'sfbk' + info + sdta + pdta)


def read_chunks(data, start, end):
    result = {}
    while start < end:
        require(start + 8 <= end, 'Truncated RIFF chunk header')
        tag, size = struct.unpack_from('<4sI', data, start)
        stop = start + 8 + size
        require(stop <= end, 'RIFF chunk exceeds container')
        key = bytes(data[start + 8:start + 12]) if tag == b'LIST' else tag
        require(key not in result, 'Duplicate RIFF chunk')
        result[key] = data[start + 12:stop] if tag == b'LIST' else data[start + 8:stop]
        start = stop + (size & 1)
    require(start == end, 'Invalid RIFF padding')
    return result


def validate_soundfont(bank):
    """Reparse emitted bytes, validate hydra references, guards and playable coverage."""
    require(bank[:4] == b'RIFF' and bank[8:12] == b'sfbk', 'Not a SoundFont RIFF')
    require(struct.unpack_from('<I', bank, 4)[0] + 8 == len(bank), 'RIFF length mismatch')
    lists = read_chunks(memoryview(bank), 12, len(bank))
    require(list(lists) == [b'INFO', b'sdta', b'pdta'], 'Wrong SoundFont list order')
    tables = read_chunks(lists[b'pdta'], 0, len(lists[b'pdta']))
    formats = {b'phdr': '<20sHHHIII', b'pbag': '<HH', b'pmod': '<HHhHH', b'pgen': '<HH',
               b'inst': '<20sH', b'ibag': '<HH', b'imod': '<HHhHH', b'igen': '<HH', b'shdr': '<20sIIIIIBbHH'}
    require(list(tables) == list(formats), 'Missing or misordered hydra table')
    records = {}
    for tag, fmt in formats.items():
        require(len(tables[tag]) % struct.calcsize(fmt) == 0, 'Invalid hydra record size')
        records[tag] = list(struct.iter_unpack(fmt, tables[tag]))
    require(records[b'phdr'][0][1:4] == (0, 0, 0), 'Expected preset 0, bank 0')
    require(records[b'phdr'][-1][3] == len(records[b'pbag']) - 1, 'Invalid EOP index')
    require(records[b'inst'][-1][1] == len(records[b'ibag']) - 1, 'Invalid EOI index')
    require(records[b'pgen'] == [(41, 0), (0, 0)], 'Invalid preset instrument link')
    for bag_tag, gen_tag, mod_tag in [(b'pbag', b'pgen', b'pmod'), (b'ibag', b'igen', b'imod')]:
        bags = records[bag_tag]
        require(bags == sorted(bags), 'Nonmonotonic bag indices')
        require(bags[-1] == (len(records[gen_tag]) - 1, len(records[mod_tag]) - 1), 'Bad terminal bag')
    sdta = read_chunks(lists[b'sdta'], 0, len(lists[b'sdta']))
    pcm = sdta[b'smpl']
    headers = records[b'shdr'][:-1]
    zones = []
    for index, (gen_index, _) in enumerate(records[b'ibag'][:-1]):
        stop = records[b'ibag'][index + 1][0]
        gens = records[b'igen'][gen_index:stop]
        require([gens[0][0], gens[1][0], gens[-1][0]] == [43, 44, 53], 'Invalid zone generator order')
        values = dict(gens)
        require(len(values) == len(gens), 'Duplicate zone generator')
        sample_id = values[53]
        require(sample_id < len(headers), 'Invalid sample reference')
        _, start, end, loop_start, loop_end, rate, root, _, link, kind = headers[sample_id]
        require(start < loop_start - 7 and loop_start < loop_end - 31 and loop_end < end - 7, 'Invalid sample points')
        require((end + 46) * 2 <= len(pcm) and bytes(pcm[end * 2:(end + 46) * 2]) == b'\0' * 92, 'Missing sample guard')
        require(rate == 44100 and kind == 1 and link == 0, 'Unexpected sample format')
        require(values[54] == 0 and values[58] == root and values[38] == RELEASE & 0xffff, 'Invalid articulation')
        key_low, key_high = values[43] & 255, values[43] >> 8
        vel_low, vel_high = values[44] & 255, values[44] >> 8
        require(key_low <= root <= key_high and 1 <= vel_low <= vel_high <= 127, 'Invalid zone ranges')
        zones.append((key_low, key_high, vel_low, vel_high))
    for key in range(128):
        for velocity in range(1, 128):
            count = sum(lo <= key <= hi and vlo <= velocity <= vhi for lo, hi, vlo, vhi in zones)
            require(count == int(KEY_RANGE[0] <= key <= KEY_RANGE[1]), 'Missing or overlapping playable zone')
    return {'riff_and_hydra': 'valid', 'preset_count': len(records[b'phdr']) - 1,
            'sample_count': len(headers), 'zone_count': len(zones),
            'coverage': 'Exactly one zone per note/velocity on MIDI 57-81; silence outside',
            'sample_guards': '46 zero sample points after every embedded sample'}


def write_native_exs(samples, destination):
    """Use a pinned, source-reviewed EXS writer; never guess proprietary fields.

    The five stdlib-only upstream modules are temporary build dependencies, not
    redistributed project code. Their revision and hashes pin reproducibility.
    """
    import importlib
    import tempfile

    revision = 'd886a5994b7a46de1fc49aec4eb37e8d83b72d55'
    base = 'https://raw.githubusercontent.com/jonkubis/exstools4/' + revision + '/'
    hashes = {
        'exsclasses': 'ae1de7f1f28bb0df99bb429be36e774a7bdde6d30e3740fef1736232a4d5a848',
        'exsparams': 'f82a43dda696800ad19776b4dd8cdff5f2c107643e5da445a397f9df45b17d26',
        'exsblock': 'bd3f414b320e40c9729253b965d31f4351583fa41762f2f23c3692581dc0087e',
        'exsfile': 'ca593f015d733784c448b9fff7e79413ef0999eeca4f52b91ca50052876043f7',
        'samplesearch': '2b3f02868d2c3ff890b8917a7fe8dbc6be8e12573bc446b81e59de5f240d75aa',
    }
    with tempfile.TemporaryDirectory(prefix='astra-exs-writer-') as dependency_dir:
        for module, checksum in hashes.items():
            with urllib.request.urlopen(base + module + '.py', timeout=60) as response:
                code = response.read()
            require(hashlib.sha256(code).hexdigest() == checksum, 'EXS writer checksum mismatch')
            (Path(dependency_dir) / (module + '.py')).write_bytes(code)
        sys.path.insert(0, dependency_dir)
        try:
            classes = importlib.import_module('exsclasses')
            writer = importlib.import_module('exsfile')
            parameters = importlib.import_module('exsparams')
            search = importlib.import_module('samplesearch')
            instrument = classes.EXSInstrument()
            instrument.name = NAME
            instrument.pathname = str(destination)
            instrument.params = dict(parameters.default_params)
            instrument.params.update({
                parameters.PARAM_MASTER_VOLUME: -3,
                parameters.PARAM_FILTER1_TOGGLE: 0,
                parameters.PARAM_FILTER2_TOGGLE: 0,
                parameters.PARAM_ENV1_ATK_HI_VEL: parameters.env_ms_to_value(3),
                parameters.PARAM_ENV1_ATK_LO_VEL: parameters.env_ms_to_value(3),
                parameters.PARAM_ENV1_DECAY: 0,
                parameters.PARAM_ENV1_SUSTAIN: 127,
                parameters.PARAM_ENV1_RELEASE: parameters.env_ms_to_value(100),
            })
            for index, sample in enumerate(samples):
                source = search.get_sample_info(sample['source_file'])
                instrument.samples.append(source)
                zone = classes.EXSZone()
                zone.Name, zone.id, zone.FileName = sample['name'], index, index
                zone.KeyNote = sample['root_midi']
                zone.FirstNote, zone.LastNote = sample['key_range']
                zone.LowestVelocity, zone.HighestVelocity = sample['velocity_range']
                zone.velrangeenable = True
                zone.StartFrame, zone.EndFrame = 0, source.frameCount
                zone.SustainLoopStart, zone.SustainLoopEnd = 0, source.frameCount
                zone.SustainLoop, zone.OneShot, zone.Pitched = False, False, True
                instrument.zones.append(zone)
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix('.exs.part')
            writer.write_exsfile(instrument, str(temporary))
            parsed = writer.read_exsfile(str(temporary))
            require(parsed is not None and parsed.name == NAME, 'Native EXS failed readback')
            require(len(parsed.zones) == len(samples) == len(parsed.samples), 'Native EXS sample count mismatch')
            for index, (zone, source, expected) in enumerate(zip(parsed.zones, parsed.samples, samples)):
                require(zone.FileName == index and zone.KeyNote == expected['root_midi'], 'Native EXS root/link mismatch')
                require([zone.FirstNote, zone.LastNote] == expected['key_range'], 'Native EXS key range mismatch')
                require([zone.LowestVelocity, zone.HighestVelocity] == expected['velocity_range'], 'Native EXS velocity mismatch')
                require(not zone.SustainLoop and not zone.OneShot and zone.Pitched, 'Native EXS playback flags mismatch')
                require(zone.StartFrame == 0 and zone.EndFrame == source.frameCount, 'Native EXS sample boundaries mismatch')
                require(Path(source.folder, source.filename) == Path(expected['source_file']), 'Native EXS sample path mismatch')
                require(source.bitdepth == 24 and source.channels == 1 and source.sampleRate == 44100, 'Native EXS source format mismatch')
            require(search.resolve_sample_locations(parsed), 'Native EXS missing sample file')
            require(parsed.params[parameters.PARAM_ENV1_RELEASE] == parameters.env_ms_to_value(100), 'Native EXS release mismatch')
            require(parsed.params[parameters.PARAM_MASTER_VOLUME] == -3, 'Native EXS gain mismatch')
            temporary.replace(destination)
        finally:
            sys.path.remove(dependency_dir)
            for module in hashes:
                sys.modules.pop(module, None)
    result = {
        'file': str(destination), 'format': 'Native Logic EXS24; references original mono 44.1 kHz 24-bit WAV',
        'bytes': destination.stat().st_size, 'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
        'writer': 'https://github.com/jonkubis/exstools4', 'writer_revision': revision,
        'writer_source_sha256': hashes,
        'attack_ms': parameters.env_value_to_ms(parameters.env_ms_to_value(3)),
        'release_ms': parameters.env_value_to_ms(parameters.env_ms_to_value(100)),
        'checks': 'Upstream writer/parser round-trip: all 11 sample paths, roots, key/velocity ranges, full-frame boundaries, unlooped pitched playback, gain and release verified',
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, default=ASSETS)
    parser.add_argument('--bank', type=Path, default=BANK)
    parser.add_argument('--exs', type=Path, help='Native EXS destination; defaults next to the SoundFont')
    args = parser.parse_args()
    samples = prepare_samples(args.assets)
    bank = make_soundfont(samples)
    checks = validate_soundfont(bank)
    args.bank.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.bank.with_suffix('.sf2.part')
    temporary.write_bytes(bank)
    require(hashlib.sha256(temporary.read_bytes()).digest() == hashlib.sha256(bank).digest(), 'Bank write verification failed')
    temporary.replace(args.bank)
    native = write_native_exs(samples, args.exs or args.bank.with_suffix('.exs'))
    for sample in samples:
        del sample['pcm16']
    provenance = {
        'name': NAME, 'bank_file': str(args.bank), 'bank_format': 'SoundFont 2.01 RIFF sfbk; mono signed 16-bit little-endian PCM',
        'bank_sha256': hashlib.sha256(bank).hexdigest(), 'bank_bytes': len(bank),
        'native_exs': native,
        'preset': {'index': 0, 'program_zero_based': 0, 'bank': 0, 'name': NAME},
        'key_range_midi': list(KEY_RANGE), 'recommended_melody_range_midi': [60, 79],
        'layers': {'Soft': [1, 88], 'Normal': [89, 127]},
        'processing': {'gain_db': -3, 'normalization': False, 'loops': False,
                       'sample_rate_conversion': False, 'sample_bit_conversion': 'audioop.lin2lin: signed PCM 24-bit to 16-bit; discard least-significant byte',
                       'attack_seconds': .003, 'release_seconds': 2 ** (RELEASE / 1200),
                       'recorded_attack_and_breath': 'Preserved; samples are not trimmed, synthesized or looped'},
        'source': {'library': 'Versilian Community Sample Library (VCSL)', 'author': 'Versilian Studios LLC / Sam Gossner',
                   'instrument': 'Hohner Special20 C diatonic harmonica', 'revision': REVISION,
                   'repository': 'https://github.com/sgossner/VCSL',
                   'license': 'CC0-1.0', 'license_url': BASE + 'LICENSE', 'license_statement_url': BASE + 'README.md',
                   'license_statement': "This collection is under a Creative Commons 0 license. Essentially it's Public Domain- you can do whatever you want with these sounds (even make commercial software), no royalties, no credit, no special terms."},
        'mapping_notes': ['Filename C3 sounds at MIDI 60 (scientific C4); roots independently measured from PCM, no smpl metadata present.',
                          'Normal G3 does not exist upstream; nearest Normal E3/C4 recordings cover MIDI63-68/69-74.',
                          'High whistle-register samples intentionally omitted; bank focuses on the requested midregister.'],
        'format_reference': 'https://www.synthfont.com/sfspec24.pdf',
        'construction_checks': checks, 'samples': samples,
    }
    provenance_path = args.assets / 'provenance.json'
    provenance_path.write_text(json.dumps(provenance, indent=2) + '\n')
    print(json.dumps({'bank': str(args.bank), 'bytes': len(bank), 'sha256': provenance['bank_sha256'],
                      'preset': provenance['preset'], 'checks': checks, 'native_exs': native,
                      'provenance': str(provenance_path)}, indent=2))


if __name__ == '__main__':
    main()
