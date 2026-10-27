"""Astra (gpt): eight independent, paired 16-bar genre skeletons.

Each pair holds its tempo, harmony and instrumentation constant so one rhythmic
change is audible. Only drums, bass and chordal keys are used; no Logic actions.
"""
import os

from pipeline import BAR, PPQ, E, S, SW, SK_DIR, bt, hum_t, hum_v, seed
from pipeline import build_smf, write_smf
from sketches import PC, mk_chord2


TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1)]
MARKERS = [(1, 'A'), (9, 'break'), (13, 'A2')]
N_BARS = 16
END = N_BARS * BAR

SKETCHES = [
    dict(sid='citrus-root-grid', title='Citrus Root Grid', bpm=124, genre='house',
         notes='E major; root-only eighth bass; compare bass pitch contour with Citrus Fifth Grid.'),
    dict(sid='citrus-fifth-grid', title='Citrus Fifth Grid', bpm=124, genre='house',
         notes='E major; root/fifth eighth bass; all other parts match Citrus Root Grid.'),
    dict(sid='indigo-held-room', title='Indigo Held Room', bpm=120, genre='deep house',
         notes='B minor; one held EP ninth chord per bar; compare chord rhythm with Indigo Soft Steps.'),
    dict(sid='indigo-soft-steps', title='Indigo Soft Steps', bpm=120, genre='deep house',
         notes='B minor; two soft EP stabs per bar; all other parts match Indigo Held Room.'),
    dict(sid='paper-lantern-eight', title='Paper Lantern Eight', bpm=121, genre='lo-fi house',
         notes='C minor; eight swung hats per bar; compare hat density with Paper Lantern Five.'),
    dict(sid='paper-lantern-five', title='Paper Lantern Five', bpm=121, genre='lo-fi house',
         notes='C minor; five of the same eight swung hats; all other parts match Paper Lantern Eight.'),
    dict(sid='porch-pocket-anchor', title='Porch Pocket Anchor', bpm=82, genre='lo-fi hip hop',
         notes='Eb major; kick and bass anchored to beats one and three with a pickup; compare placement.'),
    dict(sid='porch-pocket-skip', title='Porch Pocket Skip', bpm=82, genre='lo-fi hip hop',
         notes='Eb major; same three kick/bass attacks shifted into syncopation; other parts match Anchor.'),
]

# Four original loops; both members of a pair deliberately share their harmony.
# name, quality, add ninth; all voicings come from the existing chord helper.
LOOPS = {
    'house': [('E', 'M', False), ('F#', 'm', False),
              ('A', 'M', False), ('B', 'M', False)],
    'deep house': [('B', 'm7', True), ('G', 'M7', True),
                   ('E', 'm7', True), ('F#', 'm7', False)],
    'lo-fi house': [('C', 'm7', True), ('Ab', 'M7', True),
                    ('F', 'm7', True), ('Bb', '7', True)],
    'lo-fi hip hop': [('Eb', 'M7', True), ('C', 'm7', True),
                      ('Ab', 'M7', True), ('Bb', '7', True)],
}
KEYS = {'house': (4, False), 'deep house': (2, True),
        'lo-fi house': (-3, True), 'lo-fi hip hop': (-3, False)}
PAIR_SEEDS = {'house': 102124, 'deep house': 102120,
              'lo-fi house': 102121, 'lo-fi hip hop': 102182}


def compose(sid):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    spec = next((item for item in SKETCHES if item['sid'] == sid), None)
    if spec is None:
        raise ValueError('Unknown sketch: ' + sid)
    genre = spec['genre']
    hiphop = genre == 'lo-fi hip hop'
    loose = genre.startswith('lo-fi')
    jitter = 10 if loose else 6
    nt = {i: [] for i in range(len(TRACKS))}
    cc = {i: [] for i in range(len(TRACKS))}
    pcs = {0: 0 if hiphop else 25, 1: 33 if hiphop else 38,
           2: 0 if genre == 'house' else 4}
    cc[2].append((0, 64, 0))

    def note(track, tick, duration, pitch, velocity):
        tick = max(0, tick)
        duration = min(duration, END - 1 - tick)
        if duration > 0:
            nt[track].append((tick, duration, pitch, velocity))

    def drum(tick, pitch, velocity, duration=72):
        note(0, tick, duration, pitch, hum_v(velocity, 8))

    def chord(tick, duration, pitches, velocity):
        # Pedal catches the chord, releases before the next voicing, and never
        # crosses the loop boundary. Short stabs keep a short pedal window too.
        start = hum_t(tick, jitter)
        finish = min(start + duration, END - 1)
        cc[2].extend([(start, 64, 0), (start + 12, 64, 127),
                      (finish, 64, 0)])
        for pitch in pitches:
            note(2, start, finish - start - 18, pitch, hum_v(velocity, 8))

    for bar in range(1, N_BARS + 1):
        broken = 9 <= bar <= 12
        name, quality, ninth = LOOPS[genre][(bar - 1) % 4]
        harmony = mk_chord2(PC[name], quality)
        pitches = harmony['stab'] + ([harmony['n9']] if ninth else [])
        root = harmony['bass']
        origin = bt(bar)

        # Separate deterministic streams keep unchanged instruments identical
        # between pair members, even when the changed part uses fewer events.
        seed(PAIR_SEEDS[genre] + bar * 100)
        if hiphop:
            kick_beats = ((0, 2, 2.5) if sid.endswith('anchor')
                          else (0, .75, 2.75))
        else:
            kick_beats = (0, 1, 2, 3)
        kick_ticks = [hum_t(bt(bar, beat), jitter) for beat in kick_beats]
        if not (broken and genre == 'lo-fi house'):
            strength = {'house': 108, 'deep house': 84,
                        'lo-fi house': 88, 'lo-fi hip hop': 96}[genre]
            for index, tick in enumerate(kick_ticks):
                drum(tick, 36, strength - (5 if index % 2 else 0), 100)

        seed(PAIR_SEEDS[genre] + bar * 100 + 1)
        for beat in (1, 3):
            tick = hum_t(bt(bar, beat), jitter)
            strength = 99 if genre == 'house' else 78
            drum(tick, 38, strength, 100)
            if not hiphop:
                # Same onset as snare, never an exposed clap.
                drum(tick, 39, strength - 25, 90)
        if hiphop:
            for beat in (1.75, 3.75):
                drum(hum_t(bt(bar, beat), jitter), 38, 38, 48)

        seed(PAIR_SEEDS[genre] + bar * 100 + 2)
        if genre == 'house':
            if not broken:
                for beat in range(4):
                    drum(hum_t(bt(bar, beat), jitter), 42, 57, 60)
                    drum(hum_t(bt(bar, beat + .5), jitter), 46, 79, 150)
        elif genre == 'deep house':
            for step in range(16):
                drum(hum_t(origin + step * S, jitter), 42,
                     (50, 37, 62, 40)[step % 4], 45)
        else:
            retained = {0, 1, 3, 4, 7}
            for step in range(8):
                tick = hum_t(origin + step * E + (SW if step % 2 else 0), jitter)
                velocity = hum_v(57 if step % 2 == 0 else 43, 8)
                # Consume the same random values for omitted hats so surviving
                # notes remain identical, isolating density rather than feel.
                if genre == 'lo-fi house' and sid.endswith('five') and step not in retained:
                    continue
                if hiphop and broken:
                    continue
                note(0, tick, 52, 42, velocity)
        if bar == 13:
            note(0, origin, PPQ, 49, 100)

        seed(PAIR_SEEDS[genre] + bar * 100 + 3)
        if genre == 'house':
            for step in range(8):
                pitch = root + (7 if sid == 'citrus-fifth-grid' and step in (3, 7) else 0)
                note(1, hum_t(origin + step * E, 6), 166, pitch,
                     hum_v(77 if step % 2 == 0 else 66, 8))
        elif genre == 'deep house':
            if not broken:
                note(1, hum_t(origin, 6), BAR - 80, root, hum_v(63, 8))
        elif genre == 'lo-fi house':
            for beat, duration in ((.5, 600), (2.5, 540)):
                # A deliberate +8 tick pocket plus +/-2 jitter stays <=10 late.
                note(1, hum_t(bt(bar, beat) + 8, 2), duration, root, hum_v(64, 8))
        else:
            for tick in kick_ticks:
                note(1, tick, 200, root, hum_v(68, 8))

        seed(PAIR_SEEDS[genre] + bar * 100 + 4)
        if genre == 'house':
            for beat in (.75, 2.25, 3.5):
                chord(bt(bar, beat), 125, pitches, 80)
        elif genre == 'deep house':
            if sid == 'indigo-held-room':
                chord(origin, BAR - 70, pitches, 57)
            else:
                for beat in (.5, 2.5):
                    chord(bt(bar, beat), 300, pitches, 57)
        elif genre == 'lo-fi house':
            # Low register and velocity imply a muffled source without assuming
            # any synth-specific filter controller is honored by the GM patch.
            for beat in (.75, 2.5):
                chord(bt(bar, beat), 205, [p - 12 for p in pitches], 49)
        else:
            chord(origin, BAR - 85, pitches, 61)

    cc[2].append((END - 1, 64, 0))
    keysig_sf, minor = KEYS[genre]
    return nt, cc, pcs, N_BARS, spec['bpm'], spec['title'], keysig_sf, minor


if __name__ == '__main__':
    for sketch in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor = compose(sketch['sid'])
        smf = build_smf(title, bpm, keysig_sf, minor, n_bars, TRACKS,
                        pcs, nt, cc, markers=MARKERS)
        print(write_smf(os.path.join(SK_DIR, sketch['sid'] + '-v1.mid'), smf))
