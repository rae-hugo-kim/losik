"""Fable (claude-fable): eight paired 16-bar genre skeletons — parallel-mode pairs.

Pair principle: the two sketches of a genre share tempo, drum pattern, bass rhythm
cell, chord rhythm, voicing register and break instrument. Only the *mode* changes:
one sketch sits in a minor key, its partner in the parallel major on the same tonic,
with chord qualities and the few diatonic roots that follow from that. The question
each pair asks is how much of a genre's "feel" survives when only the harmony's mode
is swapped under an identical rhythm section.

Drums + bass + chords only (deep house adds a 1+5 pad). Bars 1-8 loop, 9-12 subtract
one layer, 13-16 return with a crash. No leads, no Logic actions.
"""
import os

from pipeline import BAR, PPQ, E, S, SW, SK_DIR, bt, hum_t, hum_v, seed
from pipeline import build_smf, write_smf
from sketches import PC

N_BARS = 16
END = N_BARS * BAR
MARKERS = [(1, 'A'), (9, 'break'), (13, 'A2')]
BREAK = range(9, 13)

# GM drum notes
K, SN, CL, CH, OH, CR = 36, 38, 39, 42, 46, 49

SKETCHES = [
    dict(sid='copper-tram-minor', title='Copper Tram Minor', bpm=124, genre='house',
         notes='G minor; four-on-the-floor, offbeat open hats, octave-leap eighth bass, bright grand stabs; break drops the stabs.'),
    dict(sid='copper-tram-major', title='Copper Tram Major', bpm=124, genre='house',
         notes='G major; identical rhythm section to Copper Tram Minor, chords and VI/VII roots swapped to the parallel major.'),
    dict(sid='harbor-fog-minor', title='Harbor Fog Minor', bpm=120, genre='deep house',
         notes='D minor; soft kick, accented 16th hats, long sub bass, rootless EP ninths held then re-touched, 1+5 pad; break drops kick/snare.'),
    dict(sid='harbor-fog-major', title='Harbor Fog Major', bpm=120, genre='deep house',
         notes='D major; identical rhythm section and pad rhythm to Harbor Fog Minor, harmony swapped to the parallel major.'),
    dict(sid='attic-radio-minor', title='Attic Radio Minor', bpm=121, genre='lo-fi house',
         notes='A minor; five swung hats per bar, lagging bass, low muffled EP shells on the offbeats; break drops the bass.'),
    dict(sid='attic-radio-major', title='Attic Radio Major', bpm=121, genre='lo-fi house',
         notes='A major; identical drums, lag and stab rhythm to Attic Radio Minor, harmony swapped to the parallel major.'),
    dict(sid='late-bus-minor', title='Late Bus Minor', bpm=80, genre='lo-fi hip hop',
         notes='C minor; boom-bap kick with ghosts, swung hats, finger bass glued to the kick, pedalled grand ninths; break drops all drums.'),
    dict(sid='late-bus-major', title='Late Bus Major', bpm=80, genre='lo-fi hip hop',
         notes='C major; identical drums, bass cell and pedal rhythm to Late Bus Minor, harmony swapped to the parallel major.'),
]

# sid -> (keysig_sf, minor, 4-bar loop of (root, quality))
HARMONY = {
    'copper-tram-minor': (-2, True, [('G', 'm7'), ('C', 'm7'), ('Eb', 'M7'), ('F', '7')]),
    'copper-tram-major': (1, False, [('G', 'M7'), ('C', 'M7'), ('E', 'm7'), ('D', '7')]),
    'harbor-fog-minor': (-1, True, [('D', 'm9'), ('G', 'm9'), ('Bb', 'M9'), ('A', '7b9')]),
    'harbor-fog-major': (2, False, [('D', 'M9'), ('G', 'M9'), ('B', 'm9'), ('A', '9')]),
    'attic-radio-minor': (0, True, [('A', 'm9'), ('F', 'M9'), ('D', 'm9'), ('E', '7b9')]),
    'attic-radio-major': (3, False, [('A', 'M9'), ('F#', 'm9'), ('D', 'M9'), ('E', '9')]),
    'late-bus-minor': (-3, True, [('C', 'm9'), ('Ab', 'M9'), ('F', 'm9'), ('G', '7b9')]),
    'late-bus-major': (0, False, [('C', 'M9'), ('A', 'm9'), ('F', 'M9'), ('G', '9')]),
}
QUAL = {
    'm7': [0, 3, 7, 10], 'M7': [0, 4, 7, 11], '7': [0, 4, 7, 10],
    'm9': [0, 3, 7, 10, 14], 'M9': [0, 4, 7, 11, 14], '9': [0, 4, 7, 10, 14], '7b9': [0, 4, 7, 10, 13],
}
GENRE_SEED = {'house': 61224, 'deep house': 61220, 'lo-fi house': 61221, 'lo-fi hip hop': 61280}


def voice(pc, q, lo, hi, rootless=False):
    """Chord tones from a root placed in [lo, lo+11]; anything above hi folds down an octave."""
    iv = QUAL[q][1:] if rootless else QUAL[q]
    r = lo + (pc - lo) % 12
    return sorted(n - 12 if n > hi else n for n in (r + i for i in iv))


def low(pc, lo):
    return lo + (pc - lo) % 12


def chord_at(loop, bar):
    name, q = loop[(bar - 1) % 4]
    return PC[name], q


def put(nt, i, t, dur, pitch, vel):
    t = max(0, t)
    if t < END:
        nt[i].append((t, max(1, min(dur, END - t)), pitch, vel))


def pedal(cc, i, t_on, t_off):
    """CC64 re-pedal: lift just before, press just after the chord onset."""
    cc[i].append((max(0, t_on - 24), 64, 0))
    cc[i].append((t_on + 30, 64, 127))
    cc[i].append((t_off, 64, 0))


def drum_return(nt, bar):
    """Crash on the A2 downbeat; two-sixteenth snare pickup at the end of the break."""
    if bar == 12:
        put(nt, 0, bt(bar, 3.5), S, SN, 86)
        put(nt, 0, bt(bar, 3.75), S, SN, 104)
    if bar == 13:
        put(nt, 0, bt(bar), BAR, CR, 106)


# ----------------------------------------------------------------- house
def house(nt, cc, loop):
    for bar in range(1, N_BARS + 1):
        for b in range(4):
            put(nt, 0, hum_t(bt(bar, b), 4), S, K, hum_v(114, 5))
            if b in (1, 3):
                t = hum_t(bt(bar, b), 4)
                put(nt, 0, t, S, SN, hum_v(100, 6))
                put(nt, 0, t, S, CL, hum_v(84, 6))
            put(nt, 0, hum_t(bt(bar, b), 5), 60, CH, hum_v(58, 6))
            put(nt, 0, hum_t(bt(bar, b + .5), 6), E - 50, OH, hum_v(92, 8))
        drum_return(nt, bar)
    for bar in range(1, N_BARS + 1):
        pc, q = chord_at(loop, bar)
        root = low(pc, 33)
        for k, (off, vel) in enumerate(zip([0, 0, 12, 0, 7, 0, 12, 0], [102, 84, 92, 84, 98, 84, 92, 80])):
            put(nt, 1, hum_t(bt(bar, k / 2), 4), E - 36, root + off, hum_v(vel, 5))
    for bar in range(1, N_BARS + 1):
        if bar in BREAK:
            continue
        pc, q = chord_at(loop, bar)
        notes = voice(pc, q, 60, 79)
        hits = [(.5, 96), (1.5, 88), (3, 94)] if bar % 2 else [(.5, 96), (1.5, 88), (2.5, 90), (3.5, 86)]
        for beat, vel in hits:
            t = hum_t(bt(bar, beat), 6)
            v = hum_v(vel, 6)
            for n in notes:
                put(nt, 2, t, S - 24, n, v)
    return {0: 25, 1: 38, 2: 0}


# ------------------------------------------------------------ deep house
def deep_house(nt, cc, loop):
    for bar in range(1, N_BARS + 1):
        full = bar not in BREAK
        for k in range(16):
            beat = k / 4
            if full and k % 4 == 0:
                put(nt, 0, hum_t(bt(bar, beat), 5), S, K, hum_v(92, 5))
            if full and k in (4, 12):
                t = hum_t(bt(bar, beat), 5)
                put(nt, 0, t, S, SN, hum_v(78, 6))
                put(nt, 0, t, S, CL, hum_v(56, 6))
            if k == 14 and bar % 2 == 0:
                put(nt, 0, hum_t(bt(bar, beat), 6), E - 60, OH, hum_v(70, 6))
                continue
            vel = 74 if k % 4 == 2 else (46 if k % 2 else 56)
            put(nt, 0, hum_t(bt(bar, beat), 6), 50, CH, hum_v(vel, 6))
        drum_return(nt, bar)
    for bar in range(1, N_BARS + 1):
        pc, q = chord_at(loop, bar)
        root = low(pc, 28)
        tail = 0 if bar % 4 == 0 else -5
        for beat, dur, off, vel in [(0, 1.75, 0, 98), (2.5, 1, 0, 84), (3.5, .5, tail, 80)]:
            put(nt, 1, hum_t(bt(bar, beat), 4), int(dur * PPQ) - 30, root + off, hum_v(vel, 4))
    for bar in range(1, N_BARS + 1):
        pc, q = chord_at(loop, bar)
        notes = voice(pc, q, 57, 78, rootless=True)
        t0 = hum_t(bt(bar), 5)
        v0 = hum_v(72, 5)
        for n in notes:
            put(nt, 2, t0, 2 * PPQ - 40, n, v0)
        t1 = hum_t(bt(bar, 2.5), 5)
        v1 = hum_v(60, 5)
        for n in notes:
            put(nt, 2, t1, int(1.25 * PPQ) - 40, n, v1)
        pedal(cc, 2, t0, bt(bar + 1) - 30 if bar < N_BARS else END - 10)
        pr = low(pc, 48)
        for n in (pr, pr + 7):
            put(nt, 3, bt(bar), BAR - 20, n, 56)
    return {0: 25, 1: 38, 2: 4, 3: 89}


# ----------------------------------------------------------- lo-fi house
LAG = 9  # lo-fi house bass sits this far behind the grid before humanize


def lofi_house(nt, cc, loop):
    for bar in range(1, N_BARS + 1):
        for b in range(4):
            put(nt, 0, hum_t(bt(bar, b), 9), S, K, hum_v(96, 8))
            if b in (1, 3):
                t = hum_t(bt(bar, b), 9)
                put(nt, 0, t, S, SN, hum_v(82, 10))
                put(nt, 0, t, S, CL, hum_v(62, 8))
        for beat in (.5, 1.5, 2, 2.5, 3.5):
            off = beat % 1 == .5
            t = hum_t(bt(bar, beat) + (SW if off else 0), 10)
            if beat == 1.5 and bar % 4 == 0:
                put(nt, 0, t, E - 60, OH, hum_v(66, 10))
            else:
                put(nt, 0, t, 50, CH, hum_v(72 if off else 52, 12))
        drum_return(nt, bar)
    for bar in range(1, N_BARS + 1):
        if bar in BREAK:
            continue
        pc, q = chord_at(loop, bar)
        root = low(pc, 31)
        for beat, dur, off, vel in [(0, .75, 0, 96), (1.5, .5, 0, 80), (2, .75, 0, 92), (3.5, .5, 12, 78)]:
            put(nt, 1, hum_t(bt(bar, beat) + LAG, 6), int(dur * PPQ) - 40, root + off, hum_v(vel, 8))
    for bar in range(1, N_BARS + 1):
        pc, q = chord_at(loop, bar)
        notes = voice(pc, q, 48, 66, rootless=True)
        for beat, dur, vel in [(.5, S, 58), (1.5, S + 60, 64), (3.5, S, 54)]:
            t = hum_t(bt(bar, beat) + SW, 10)
            v = hum_v(vel, 10)
            for n in notes:
                put(nt, 2, t, dur, n, v)
    return {0: 25, 1: 38, 2: 4}


# --------------------------------------------------------- lo-fi hip hop
def lofi_hiphop(nt, cc, loop):
    kicks = {1: [(0, 104), (1.75, 86), (2.5, 94)], 0: [(0, 104), (2.5, 94), (3.75, 82)]}
    ghosts = {1: [2.75, 3.5], 0: [1.5, 3.25]}
    for bar in range(1, N_BARS + 1):
        if bar in BREAK:
            drum_return(nt, bar)
            continue
        odd = bar % 2
        for beat, vel in kicks[odd]:
            put(nt, 0, hum_t(bt(bar, beat), 8), S, K, hum_v(vel, 6))
        for beat in (1, 3):
            put(nt, 0, hum_t(bt(bar, beat), 7), S, SN, hum_v(102, 6))
        for beat in ghosts[odd]:
            put(nt, 0, hum_t(bt(bar, beat), 10), 60, SN, hum_v(40, 8))
        for k in range(8):
            beat = k / 2
            t = hum_t(bt(bar, beat) + (SW if k % 2 else 0), 10)
            if k == 7 and bar % 4 == 0:
                put(nt, 0, t, E - 40, OH, hum_v(62, 8))
            else:
                put(nt, 0, t, 60, CH, hum_v(56 if k % 2 else 70, 10))
        drum_return(nt, bar)
    cells = {1: [(0, 1.5, 0, 96), (1.75, .5, 0, 80), (2.5, 1.25, -5, 88)],
             0: [(0, 2.25, 0, 96), (2.5, 1, 0, 84), (3.75, .25, 7, 76)]}
    for bar in range(1, N_BARS + 1):
        pc, q = chord_at(loop, bar)
        root = low(pc, 33)
        for beat, dur, off, vel in cells[bar % 2]:
            put(nt, 1, hum_t(bt(bar, beat), 8), int(dur * PPQ) - 40, root + off, hum_v(vel, 6))
    for bar in range(1, N_BARS + 1):
        pc, q = chord_at(loop, bar)
        notes = voice(pc, q, 55, 76, rootless=True)
        t0 = hum_t(bt(bar), 8)
        v0 = hum_v(70, 6)
        for n in notes:
            put(nt, 2, t0 + (n - notes[0]) * 2, int(3.6 * PPQ), n, v0)   # slight roll upward
        if bar % 2 == 0:
            t1 = hum_t(bt(bar, 2.5), 8)
            v1 = hum_v(52, 6)
            for n in notes:
                put(nt, 2, t1, int(1.2 * PPQ), n, v1)
        pedal(cc, 2, t0, bt(bar + 1) - 30 if bar < N_BARS else END - 10)
    return {0: 0, 1: 33, 2: 0}


GENRES = {'house': house, 'deep house': deep_house, 'lo-fi house': lofi_house, 'lo-fi hip hop': lofi_hiphop}


def tracks_for(genre):
    base = [('Drums', 9), ('Bass', 0), ('Keys', 1)]
    return base + [('Pad', 2)] if genre == 'deep house' else base


def compose(sid):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    spec = next((s for s in SKETCHES if s['sid'] == sid), None)
    if spec is None:
        raise ValueError('unknown sketch ' + sid)
    keysig_sf, minor, loop = HARMONY[sid]
    seed(GENRE_SEED[spec['genre']])
    nt = {i: [] for i in range(4)}
    cc = {i: [] for i in range(4)}
    pcs = GENRES[spec['genre']](nt, cc, loop)
    return nt, cc, pcs, N_BARS, spec['bpm'], spec['title'], keysig_sf, minor


if __name__ == '__main__':
    for spec in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, sf, minor = compose(spec['sid'])
        smf = build_smf(title, bpm, sf, minor, n_bars, tracks_for(spec['genre']), pcs, nt, cc, MARKERS)
        print(write_smf(os.path.join(SK_DIR, spec['sid'] + '-v1.mid'), smf))
