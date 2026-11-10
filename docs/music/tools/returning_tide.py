"""Returning Tide: original 112-bar instrumental, using the established Logic SMF pipeline."""
from collections import defaultdict
from pathlib import Path
import json
import pipeline as p

TITLE = 'Returning Tide Astra v1'
BPM = 100
BARS = 112
SECTIONS = [(1, 8, 'Intro A'), (9, 8, 'Intro B'), (17, 16, 'Verse 1'),
            (33, 8, 'Pre 1'), (41, 8, 'Chorus 1'), (49, 16, 'Verse 2'),
            (65, 8, 'Pre 2'), (73, 8, 'Chorus 2'), (81, 8, 'Bridge'),
            (89, 16, 'Final Chorus'), (105, 8, 'Outro')]
TRACKS = [('SoCal - Breathing Drums', 9), ('Simple Foundation - Bass', 0),
          ('Acoustic Guitar - Tide Motif', 1), ('Studio Grand - Harmony', 2),
          ('Authentic Strings - Horizon', 3), ('Deluxe Classic - Song Melody', 4),
          ('Studio Grand - Upper Light', 5), ('Hard Rock - Wide Fifths', 6)]
PCS = dict(enumerate([0, 33, 25, 0, 50, 4, 0, 26]))
# Bass and upper voicings; D major with a relative-minor verse.
CHORDS = {'D': (38, [62, 66, 69, 73]), 'Ac': (37, [61, 64, 69, 71]),
          'Bm': (35, [62, 66, 69, 71]), 'G': (43, [59, 62, 66, 69]),
          'A': (33, [61, 64, 67, 69]), 'Em': (40, [59, 62, 66, 67]),
          'Fs': (42, [61, 64, 66, 69]), 'Df': (42, [62, 66, 69, 74])}
INTRO = ['D', 'Ac', 'Bm', 'G']
VERSE = ['Bm', 'G', 'D', 'A']
PRE = ['Em', 'Fs', 'G', 'A']
CHORUS = ['G', 'Df', 'Em', 'A', 'G', 'D', 'Em', 'A']
# Hand-composed two-bar question, two-bar answer. Eighth-note pickup and fourth leap.
MOTIF = [[(0, 66, .75), (1, 66, .4), (1.5, 69, .8), (2.5, 73, .9)],
         [(.5, 71, .8), (1.5, 69, .4), (2, 66, 1.5)],
         [(0, 66, .75), (1, 66, .4), (1.5, 69, .8), (2.5, 74, .9)],
         [(.5, 71, .9), (1.5, 69, .4), (2, 67, 1.4)]]
VERSE_MELODY = [[(.5, 62, .8), (1.5, 66, .4), (2, 66, .8), (3, 64, .6)],
                [(0, 62, 1.3), (2, 59, .8), (3, 62, .6)],
                [(.5, 61, .4), (1, 62, .8), (2, 66, 1.4)],
                [(0, 64, 1.4), (2, 61, .7)],
                [(.5, 66, .8), (1.5, 69, .4), (2, 71, 1.3)],
                [(0, 69, 1.3), (2, 67, .8), (3, 66, .6)],
                [(0, 66, .8), (1, 64, .4), (1.5, 62, 1.3)],
                [(0, 61, 1.6), (3, 64, .5)]]
HOOK = [[(0, 74, 1.4), (1.5, 71, .4), (2, 69, 1.4)],
        [(.5, 69, .8), (1.5, 66, .4), (2, 69, 1.3)],
        [(0, 71, .8), (1, 74, .8), (2, 76, 1.4)],
        [(0, 73, 2.4), (3, 71, .5)],
        [(0, 74, 1.4), (1.5, 76, .4), (2, 78, 1.4)],
        [(0, 76, .8), (1, 74, 1.7)],
        [(.5, 71, .8), (1.5, 69, .4), (2, 67, 1.4)],
        [(0, 69, 2.8)]]


def compose():
    p.seed(908)
    notes, controls = defaultdict(list), defaultdict(list)

    def note(track, bar, beat, pitch, dur, vel, human=False):
        tick = p.bt(bar, beat)
        if human:
            tick = p.hum_t(tick, 8)
            vel = p.hum_v(vel, 9)
        notes[track].append((tick, max(1, round(dur * p.PPQ)), pitch, max(1, min(127, vel))))

    for start, length, section in SECTIONS:
        for offset in range(length):
            bar = start + offset
            verse = section.startswith('Verse')
            pre = section.startswith('Pre')
            chorus = 'Chorus' in section
            final = section == 'Final Chorus'
            peak = final and offset >= 8
            intro = section.startswith('Intro')
            outro = section == 'Outro'
            bridge = section == 'Bridge'
            progression = VERSE if verse else PRE if pre else CHORUS if chorus else INTRO
            if bridge:
                progression = ['Bm', 'Bm', 'G', 'G', 'Em', 'Fs', 'G', 'A']
            chord = progression[offset % len(progression)]
            root, voice = CHORDS[chord]
            strength = 1.08 if peak else 1.0 if final else .91 if chorus else .76 if pre else .64
            if outro:
                strength = .60 - offset * .045

            # Drum texture expands in density, not just velocity; bridge removes the kit.
            if not bridge and not (outro and offset >= 4):
                soft = (intro and bar <= 8) or outro
                snare = 37 if soft else 38
                base = int(78 * strength)
                kicks = [0, 2.5] if soft or verse else [0, 1.5, 2, 3.5] if chorus else [0, 2, 2.75]
                for beat in kicks:
                    note(0, bar, beat, 36, .13, base + 5, True)
                for beat in [1, 3]:
                    note(0, bar, beat, snare, .13, base + 9, True)
                for h in range(8):
                    pitch = 46 if chorus and h == 7 else 42
                    note(0, bar, h / 2, pitch, .10, int((52 if h % 2 == 0 else 37) * strength), True)
                if chorus:
                    note(0, bar, 2.75, 38, .1, 32, True)
                if peak:
                    for beat in [0, 2]:
                        note(0, bar, beat, 51, .3, 51, True)
                if offset == 0 and (chorus or pre):
                    note(0, bar, 0, 49, 2.0, 76 if chorus else 48, True)
                if offset == length - 1 and (pre or chorus):
                    for j, pitch in enumerate([38, 38, 48, 45]):
                        note(0, bar, 3 + j * .25, pitch, .12, 48 + j * 9, True)

            if bar >= 5 and not bridge and not (outro and offset >= 4):
                bass_notes = [(0, 3.3)] if not chorus else [(0, 1.25), (1.5, .35), (2, 1.2), (3.5, .3)]
                for beat, duration in bass_notes:
                    note(1, bar, beat, root, duration, int(64 * strength), True)

            # Guitar motif yields to the song melody after the introduction.
            if intro or outro:
                pattern = MOTIF[offset % 4]
                if outro and offset >= 6:
                    pattern = [(0, 66 if offset == 6 else 62, 3.6)]
                for beat, pitch, duration in pattern:
                    note(2, bar, beat, pitch, duration, int(92 * strength), True)
            elif verse and offset % 4 == 3:
                for beat, pitch, duration in [(2.5, 66, .4), (3, 69, .6)]:
                    note(2, bar, beat, pitch, duration, 43, True)
            elif chorus:
                for beat, pitch, duration in MOTIF[offset % 4][-1:]:
                    note(2, bar, beat, pitch, duration, 58 if peak else 44, True)
            elif bridge and offset < 4:
                note(2, bar, 0, [66, 69, 74, 71][offset], 2.8, 43, True)

            # Sustained, re-pedalled piano harmony; selected eighth-note motion in prechoruses.
            if bar >= 9 and not (outro and offset >= 4):
                controls[3].extend([(p.bt(bar), 64, 0), (p.bt(bar, .08), 64, 100),
                                    (p.bt(bar, 3.88), 64, 0)])
                if pre:
                    for j, ix in enumerate([0, 2, 1, 3, 2, 1, 3, 2]):
                        note(3, bar, j / 2, voice[ix], .8, 43 + j % 3 * 4, True)
                else:
                    beats = [0, 2] if chorus else [0]
                    for beat in beats:
                        for j, pitch in enumerate(voice[:3]):
                            note(3, bar, beat + j * .025, pitch, 1.7 if chorus else 3.5,
                                 int((60 if not bridge else 38) * strength), True)

            # Strings begin as a quiet horizon, absent from the first verse.
            strings = (intro and bar >= 11) or pre or chorus or (section == 'Verse 2' and offset >= 8)
            if strings:
                for pitch in [voice[1], voice[-1]]:
                    note(4, bar, 0, pitch, 3.9, int((61 if peak else 45) * strength))

            if verse or chorus:
                phrase = (HOOK if chorus else VERSE_MELODY)[offset % 8]
                if peak and offset % 8 == 4:
                    phrase = [(0, 78, 1.4), (1.5, 79, .4), (2, 81, 1.4)]
                if peak and offset % 8 == 5:
                    phrase = [(0, 78, .8), (1, 76, .8), (2, 74, 1.4)]
                if final and offset == 15:
                    phrase = [(0, 73, 1.3), (1.5, 71, .4), (2, 69, 1.4)]
                for beat, pitch, duration in phrase:
                    note(5, bar, beat, pitch, duration, 83 if peak else 75 if chorus else 65, True)
            elif pre:
                pitch = [67, 69, 71, 73][offset % 4]
                for beat, duration in [(0, 1.4), (2, 1.2)]:
                    note(5, bar, beat, pitch, duration, 64 + offset * 2, True)

            # Upper voice is sparse and answers gaps rather than doubling the lead.
            if intro and bar >= 13:
                note(6, bar, .25, [81, 76, 78, 79][offset % 4], 3.2, 46, True)
            if chorus and (section != 'Chorus 1') and offset % 2 == 1:
                note(6, bar, 3, [81, 78, 79, 76][(offset // 2) % 4], .8, 51 if peak else 39, True)
            if bridge and offset >= 4:
                note(6, bar, 1, [76, 78, 79, 81][offset - 4], 2.6, 37 + offset, True)
            if outro and offset < 2:
                note(6, bar, 0, 78 if offset == 0 else 76, 3.4, 35 - offset * 5)

            # Distorted fifths reserved for choruses; avoid a full synth/chord wall.
            if chorus:
                guitar_root = (38 if chord == 'Df' else root) + 12
                for beat in ([0, 2] if peak else [0]):
                    for pitch in [guitar_root, guitar_root + 7]:
                        note(7, bar, beat, pitch, 1.75 if peak else 3.4, 45 if peak else 32, True)

        if section.startswith('Pre') or section == 'Bridge':
            last = start + length - 1
            for j in range(8):
                note(0, last, 2 + j * .25, 49, .2, 30 + j * 7, True)

    # A short ensemble breath before each early chorus makes the downbeat land.
    for last in (40, 72):
        cutoff, boundary = p.bt(last, 2.5), p.bt(last + 1)
        for track, events in notes.items():
            notes[track] = [(tick, min(dur, cutoff - tick) if tick < cutoff else dur, pitch, vel)
                            for tick, dur, pitch, vel in events
                            if not cutoff <= tick < boundary - 8]
        controls[3].append((cutoff, 64, 0))

    # Tail remains uncluttered and truly resolves to D.
    for pitch in [50, 62, 66]:
        note(3, 112, 0, pitch, 3.8, 26)
    for track in range(len(TRACKS)):
        controls[track].append((p.bt(113), 64, 0))
    smf = p.build_smf(TITLE, BPM, 2, False, BARS, TRACKS, PCS, notes, controls,
                      [(bar, name) for bar, _, name in SECTIONS])
    return smf, notes


if __name__ == '__main__':
    dest = Path(__file__).resolve().parents[1] / 'sketches' / 'returning-tide-astra-v1.mid'
    dest.parent.mkdir(parents=True, exist_ok=True)
    smf, notes = compose()
    assert all(0 <= pitch <= 127 and 0 < vel <= 127 and dur > 0
               for track in notes.values() for tick, dur, pitch, vel in track)
    assert max(tick + dur for track in notes.values() for tick, dur, _, _ in track) <= p.bt(113)
    print(p.write_smf(dest, smf))
    print(json.dumps({'title': TITLE, 'bpm': BPM, 'bars': BARS, 'seconds': BARS * 4 * 60 / BPM,
                      'sections': SECTIONS, 'notes_per_track': {TRACKS[i][0]: len(n) for i, n in notes.items()}}, indent=2))
