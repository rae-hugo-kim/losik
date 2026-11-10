"""Four hand-written melody palettes in the established Returning Tide song form."""
from collections import defaultdict
from pathlib import Path
import hashlib
import json
import sys
import pipeline as p
import returning_tide as base

SKETCHES = Path(__file__).resolve().parents[1] / 'sketches'
IDS = ['paper-lanterns-astra-v1', 'blue-window-astra-v1',
       'northbound-lights-astra-v1', 'after-the-rain-astra-v1']
LENGTHS = {'motif': 4, 'verse': 8, 'pre': 4, 'hook': 8, 'climax': 8,
           'upper_intro': 4, 'upper_chorus': 4, 'upper_bridge': 4, 'ending': 2}


def validate(data):
    assert data['id'] in IDS
    for key, count in LENGTHS.items():
        bars = data['melodies'][key]
        assert len(bars) == count, (key, len(bars))
        for bar in bars:
            for beat, pitch, duration in bar:
                assert 0 <= beat < 4 and 0 < duration <= 4 - beat, (key, bar)
                assert isinstance(pitch, int) and pitch % 12 in (1, 2, 4, 6, 7, 9, 11), (key, pitch)
                assert 48 <= pitch <= 83
    for key, count in [('intro', 4), ('verse', 8), ('pre', 4), ('chorus', 8), ('bridge', 8), ('outro', 4)]:
        assert len(data['progressions'][key]) == count
        assert all(chord in base.CHORDS for chord in data['progressions'][key])
    assert max(n for bar in data['melodies']['climax'] for _, n, _ in bar) > max(
        n for bar in data['melodies']['hook'] for _, n, _ in bar)
    for beat, index, duration in data['piano_pattern']:
        assert 0 <= beat < 4 and 0 <= index < 4 and 0 < duration <= 4 - beat


def compose(data):
    validate(data)
    _, reference = base.compose()
    notes, controls = defaultdict(list), defaultdict(list)
    notes[0] = reference[0].copy()
    p.seed(1908 + IDS.index(data['id']))
    melodies, progressions = data['melodies'], data['progressions']

    def note(track, bar, beat, pitch, duration, velocity, human=True):
        tick = p.bt(bar, beat)
        if human:
            tick = max(p.bt(bar), p.hum_t(tick, 8))
            velocity = p.hum_v(velocity, 9)
        duration = min(round(duration * p.PPQ), p.bt(bar + 1) - tick)
        assert duration > 0
        notes[track].append((tick, duration, pitch, max(1, min(127, velocity))))

    def phrase(track, bar, events, velocity):
        for beat, pitch, duration in events:
            note(track, bar, beat, pitch, duration, velocity)

    for start, length, section in base.SECTIONS:
        for offset in range(length):
            bar = start + offset
            verse, pre = section.startswith('Verse'), section.startswith('Pre')
            chorus, final = 'Chorus' in section, section == 'Final Chorus'
            peak, intro = final and offset >= 8, section.startswith('Intro')
            outro, bridge = section == 'Outro', section == 'Bridge'
            key = 'verse' if verse else 'pre' if pre else 'chorus' if chorus else 'bridge' if bridge else 'outro' if outro else 'intro'
            progression = progressions[key]
            chord = progression[offset % len(progression)]
            root, voice = base.CHORDS[chord]
            strength = 1.08 if peak else 1.0 if final else .91 if chorus else .76 if pre else .64
            if outro:
                strength = .60 - offset * .045

            if bar >= 5 and not bridge and not (outro and offset >= 4):
                rhythm = [(0, 3.3)] if not chorus else [(0, 1.25), (1.5, .35), (2, 1.2), (3.5, .3)]
                for beat, duration in rhythm:
                    note(1, bar, beat, root, duration, int(64 * strength))

            if intro or outro:
                events = melodies['ending'][offset - 6] if outro and offset >= 6 else melodies['motif'][offset % 4]
                phrase(2, bar, events, int(92 * strength))
            elif verse and offset % 4 == 3:
                events = melodies['motif'][offset % 4][-1:]
                for _, pitch, _ in events:
                    note(2, bar, 3, pitch, .7, 43)
            elif chorus:
                phrase(2, bar, melodies['motif'][offset % 4][-1:], 58 if peak else 44)
            elif bridge and offset < 4:
                note(2, bar, 0, melodies['motif'][offset][0][1], 2.8, 43)

            if bar >= 9 and not (outro and offset >= 4):
                controls[3].extend([(p.bt(bar), 64, 0), (p.bt(bar, .08), 64, 100), (p.bt(bar, 3.88), 64, 0)])
                if pre:
                    for j, (beat, index, duration) in enumerate(data['piano_pattern']):
                        note(3, bar, beat, voice[index], duration, 43 + j % 3 * 4)
                else:
                    for beat in ([0, 2] if chorus else [0]):
                        for j, pitch in enumerate(voice[:3]):
                            note(3, bar, beat + j * .025, pitch, 1.7 if chorus else 3.5,
                                 int((60 if not bridge else 38) * strength))

            if (intro and bar >= 11) or pre or chorus or (section == 'Verse 2' and offset >= 8):
                for pitch in [voice[1], voice[-1]]:
                    note(4, bar, 0, pitch, 3.9, int((61 if peak else 45) * strength), False)

            if verse or pre or chorus:
                melodic_key = 'verse' if verse else 'pre' if pre else 'climax' if peak else 'hook'
                events = melodies[melodic_key][offset % len(melodies[melodic_key])]
                velocity = 83 if peak else 75 if chorus else 64 + offset * 2 if pre else 65
                phrase(5, bar, events, velocity)

            if intro and bar >= 13:
                phrase(6, bar, melodies['upper_intro'][offset % 4], 46)
            if chorus and section != 'Chorus 1' and offset % 2 == 1:
                phrase(6, bar, melodies['upper_chorus'][(offset // 2) % 4], 51 if peak else 39)
            if bridge and offset >= 4:
                phrase(6, bar, melodies['upper_bridge'][offset - 4], 37 + offset)
            if outro and offset < 2:
                phrase(6, bar, melodies['upper_intro'][offset][-1:], 35 - offset * 5)

            if chorus:
                guitar_root = (38 if chord == 'Df' else 33 if chord == 'Ac' else root) + 12
                for beat in ([0, 2] if peak else [0]):
                    for pitch in [guitar_root, guitar_root + 7]:
                        note(7, bar, beat, pitch, 1.75 if peak else 3.4, 45 if peak else 32)

    for last in (40, 72):
        cutoff, boundary = p.bt(last, 2.5), p.bt(last + 1)
        for track, events in notes.items():
            if track == 0:
                continue
            notes[track] = [(tick, min(duration, cutoff - tick) if tick < cutoff else duration, pitch, velocity)
                            for tick, duration, pitch, velocity in events if not cutoff <= tick < boundary]
        controls[3].append((cutoff, 64, 0))
    for pitch in [50, 62, 66]:
        note(3, 112, 0, pitch, 2.5, 26, False)
    for track in range(8):
        controls[track].append((p.bt(113), 64, 0))
    tracks = [(name.replace('Tide Motif', 'Theme'), channel) for name, channel in base.TRACKS]
    smf = p.build_smf(data['title'] + ' Astra v1', base.BPM, 2, False, base.BARS, tracks,
                      base.PCS, notes, controls, [(bar, name) for bar, _, name in base.SECTIONS])
    assert all(0 <= pitch <= 127 and 0 < velocity <= 127 and duration > 0 and tick + duration <= p.bt(113)
               for events in notes.values() for tick, duration, pitch, velocity in events)
    return smf, notes


def generate(slug):
    data = json.loads((SKETCHES / (slug + '.json')).read_text())
    smf, notes = compose(data)
    for track, events in notes.items():
        if track == 0:
            continue
        ends = {}
        for tick, duration, pitch, _ in sorted(events):
            assert ends.get(pitch, 0) <= tick, ('Overlapping pitched note', slug, track, pitch, tick)
            ends[pitch] = tick + duration
    print(p.write_smf(SKETCHES / (slug + '.mid'), smf), flush=True)
    return {'id': slug, 'title': data['title'] + ' Astra v1', 'identity': data['identity'],
            'bpm': 100, 'bars': 112, 'seconds': 268.8, 'sha256_midi': hashlib.sha256(smf).hexdigest(),
            'notes_per_track': {str(track): len(events) for track, events in notes.items()}}


if __name__ == '__main__':
    wanted = sys.argv[1:] or IDS
    records = [generate(slug) for slug in wanted]
    if wanted == IDS:
        palettes = [json.loads((SKETCHES / (slug + '.json')).read_text()) for slug in wanted]
        for key in ('motif', 'verse', 'hook', 'climax'):
            assert len({json.dumps(x['melodies'][key]) for x in palettes}) == 4, key
            rhythm = {json.dumps([[(b, d) for b, _, d in bar] for bar in x['melodies'][key]]) for x in palettes}
            assert len(rhythm) == 4, ('identical rhythm', key)
        assert len({json.dumps(x['progressions']['chorus']) for x in palettes}) == 4
        assert len({record['sha256_midi'] for record in records}) == 4
        (SKETCHES / 'tide-variants-manifest.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps(records, indent=2))
