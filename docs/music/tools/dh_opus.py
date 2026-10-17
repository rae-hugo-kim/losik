"""Opus (claude): deep house set slots 3, 6, 9, ..., 30 — ten DJ tracks.

Follows docs/music/DEEP_HOUSE_SET_BRIEF.md: soft kick 78-96, closed hats 40-64 at
eighth or sparse-sixteenth density, one open hat per 2-4 bars, rim or soft snare
70-85 (clap only under the snare), sub bass inside E1-A2 moving only by root /
fifth below / octave below, two-chord minor harmony in C3-C5 at velocity 50-70,
optional root+fifth pad 35-50. Structure: 1-16 intro (kick+hats -> bass at 9 ->
chord hint at 12), 17-32 A, 33-40 break, 41-56 A2 (crash bar 41 beat 1),
57-end outro (chords and pad out, drums + bass only).

Composed last, after astra (dh_astra.py) and fable (dh_fable.py). Each loop's
second chord is a new (interval from tonic, quality) signature checked against
the 20 earlier set tracks and the brief's overlap-avoid list (SIGS_TAKEN below),
and each break is a type neither earlier model used: kick on the one only,
drums-only, four-step additive rebuild, broken 2-step kick, three-step strip,
bass-out with a two-bar chord-only gap, sub+pad only, kick+sub only, rim+keys
only, hats+piano+pad. Slot 30 (closer) runs 72 bars so the outro is 16 bars and
the drums thin out step by step down to a single kick on the one of bar 72.
"""
import os

from pipeline import BAR, PPQ, SW, SK_DIR, bt, hum_t, hum_v, seed
from pipeline import build_smf, write_smf
from sketches import PC

TRACKS = [('Drums', 9), ('Bass', 0), ('Keys', 1), ('Pad', 2)]
MARKERS = [(1, 'intro'), (17, 'A'), (33, 'break'), (41, 'A2'), (57, 'outro')]
S16 = PPQ // 4
KEYS_LAST = 56          # chords and pad stop before the outro (bar 57)

KICK, RIM, SNARE, CLAP, HAT, OHAT, CRASH = 36, 37, 38, 39, 42, 46, 49
BACK = {'rim': ((RIM, 0),), 'snare': ((SNARE, 0),), 'snare+clap': ((SNARE, 0), (CLAP, -18))}

# (interval of the loop's moving chord above the tonic, quality) to avoid. The astra/fable
# entries are from the FIRST (discarded, mis-attributed) sets; the shipped astra/fable sets
# were composed after this file and their own set-checks verify no overlap against opus.
SIGS_TAKEN = {
    (0, 'm11'), (7, 'm7'), (10, '6/9'), (2, 'm7'), (3, 'maj9'), (0, 'm9'), (1, 'maj9'),
    (2, 'm7b5'), (5, '6/9'), (0, '6/9'),                                   # astra
    (0, 'mmaj9'), (9, 'm7b5'), (7, '7sus4'), (3, 'm7'), (8, 'm9'), (10, 'm9'),
    (11, 'dim7'), (2, '7sus4'), (0, '9sus4'), (0, 'm11-quartal'),           # fable
    (5, 'm9'), (5, '9'), (8, 'maj9'),                                      # brief
}


def m(name):
    """'F#2' -> MIDI number with C4 = 60."""
    letter, rest = name[0], name[1:]
    acc = 0
    while rest and rest[0] in '#b':
        acc += 1 if rest[0] == '#' else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + PC[letter] + acc


def ch(voicing, bass, pad=None):
    return dict(v=[m(n) for n in voicing.split()], bass=m(bass), pad=m(pad) if pad else None)


# loop: [(chord, bars)]; the cycle repeats from bar 1.
# keys: (bar_in_cycle, beat, length_beats, velocity); chord = the one in force half a
#   beat after the attack.
# bass: one list per bar of a repeating cell, (beat, length_beats, degree, velocity);
#   degree r=root, f=fifth below, o=octave below (falls back to root under E1).
#   Lengths may run past the bar line (long subs).
# hats: (sixteenth step, velocity); oh=(every_n_bars, step, velocity).
# drops: (from_bar, to_bar, {parts}) — breaks and the closer's outro thinning;
#   parts: kick, kick_one (kick on beat 1 only), kick_broken (beats 1 and and-of-2),
#   back, hats, bass, keys, pad.
SKETCHES = [
    dict(slot=3, sid='dh03-cistern-hum', title='Cistern Hum', bpm=118, key='E minor', energy=1,
         sf=1, n_bars=64, pcs=(25, 38, 4, None), kick=83, back=('rim', 72, 9), swing=False,
         hats=[(2, 46), (6, 50), (14, 50)], oh=(4, 10, 50),
         loop=[(ch('B3 D4 F#4 G4', 'E2'), 2), (ch('A3 D4 E4 G4', 'E2'), 2)],
         sig=(5, '9sus4'),
         keys=[(0, 1.5, 5.0, 56), (2, 1.5, 5.0, 54)],
         bass=[[(0, 1.75, 'r', 62)], [(2.5, .45, 'f', 56)]],
         drops=[(33, 40, {'kick_one', 'bass'})], pad=None,
         break_txt='킥 1박만(마디당 1개) + 베이스 아웃, 햇·림·건반 유지',
         loop_txt='Em9 ↔ A9sus4/E (iv sus, E 페달, B→A·F♯→E 두 성부만 하행), 2마디씩, EP 2박 뒷박에서 들어와 5박 홀드',
         bass_txt='E2 페달: 1박 1.75박 / 다음 마디 3박 뒷박 짧은 5도 아래(B1)',
         feature='세 번째 오프너입니다. 마디당 햇 3개(1·2·4박 뒷박, 3박 뒷박은 비움), 림, 브레이크는 킥이 마디 1박에만 남고 서브가 빠집니다',
         notes='Third opener. Em9 <-> A9sus4 over an E pedal (iv sus, only two voices step down); '
               'EP enters late on the and-of-2 and holds five beats; three hats per bar with the '
               'and-of-3 left empty; break keeps one kick per bar and drops the sub.'),
    dict(slot=6, sid='dh06-chalk-river', title='Chalk River', bpm=119, key='B minor', energy=2,
         sf=2, n_bars=64, pcs=(25, 38, 16, None), kick=87, back=('snare', 74, 9), swing=False,
         hats=[(2, 54), (6, 54), (8, 42), (10, 54), (14, 54), (15, 40)], oh=(2, 14, 52),
         loop=[(ch('D3 F#3 A3 C#4', 'B1'), 2), (ch('D3 F3 A3 B3', 'G1'), 2)],
         sig=(8, '9'),
         keys=[(k, b, d, v) for k in range(4) for b, d, v in ((0, .9, 58), (3.0, .45, 52))],
         bass=[[(1.0, .75, 'r', 62), (3.0, .75, 'r', 60)],
               [(1.0, .75, 'r', 62), (3.0, .4, 'f', 56), (3.5, .4, 'r', 58)]],
         drops=[(33, 40, {'bass', 'keys'})], pad=None,
         break_txt='드럼만(킥·스네어·햇), 베이스·오르간 아웃',
         loop_txt='Bm9 ↔ G9 (i–♭VI9 도미넌트, D·A 공통음, F♯→F·C♯→B 하행), 2마디씩, 톤휠 오르간 매 마디 1박 짧게 + 4박 8분',
         bass_txt='2·4박 정박 4분 길이(스네어와 같이), 2마디째 4박은 5도 아래(B1 구간만 F♯1, G1 구간은 근음) + 4박 뒷박 근음',
         feature='6/16 햇(뒷박 + 3박 정박 + 4박 마지막 16분 고스트), 약한 스네어, 오픈햇 2마디에 1개, 브레이크는 드럼만 남깁니다',
         notes='Bm9 <-> G9 (i - bVI dominant ninth, D and A held while F# -> F and C# -> B); '
               'tonewheel organ chops on the one and on beat 4 every bar; sub sits on beats 2 '
               'and 4 with the snare; break is drums only (no sub, no organ).'),
    dict(slot=9, sid='dh09-wet-asphalt', title='Wet Asphalt', bpm=120, key='C# minor', energy=2,
         sf=4, n_bars=64, pcs=(25, 33, 4, 89), kick=88, back=('rim', 76, 9), swing=True,
         hats=[(0, 40), (2, 52), (3, 40), (6, 52), (10, 52), (11, 40), (14, 52)], oh=(4, 6, 52),
         loop=[(ch('E3 B3 D#4 F#4', 'C#2', 'C#2'), 2), (ch('F#3 B3 D4 G#4', 'G#1', 'G#2'), 2)],
         sig=(7, 'm7b5'),
         keys=[(0, 1.0, 2.0, 58), (1, 3.5, .4, 52), (2, 1.0, 2.0, 56), (3, 3.5, .4, 52)],
         bass=[[(1.75, 1.5, 'r', 62), (3.75, .2, 'f', 54)], [(0, .4, 'r', 58), (1.75, 1.5, 'r', 62)]],
         drops=[(33, 34, {'kick', 'back', 'hats', 'bass'}), (35, 36, {'kick', 'back', 'bass'}),
                (37, 38, {'kick', 'back'}), (39, 40, {'back'})], pad=(33, 56),
         break_txt='4단 가산 재구성: 33–34 건반+패드 → 35–36 +햇 → 37–38 +베이스 → 39–40 +킥',
         loop_txt='C♯m11 ↔ G♯m7♭5 (i–v ø, D 내추럴 그늘), 2마디씩, EP 2박 정박 2박 홀드 + 2마디째 4박 뒷박 짧게 다음 코드 당김',
         bass_txt='2박 마지막 16분에서 1.5박 + 4박 마지막 16분 5도 아래(C♯2 구간만 G♯1) / 1박 짧게 + 2박 마지막 16분 1.5박(핑거 베이스)',
         feature='스윙 7/16 햇(1박 정박 고스트 + 뒷박 + 1·3박 마지막 16분), 림, 패드는 브레이크부터, 브레이크는 2마디씩 한 요소씩 더해 쌓습니다',
         notes='C#m11 <-> G#m7b5 (i - v half-diminished, the D natural darkens it); EP holds two '
               'beats from beat 2 and anticipates the next chord with a short and-of-4 touch; '
               'finger bass pushes from the a-of-2; break rebuilds in four 2-bar steps '
               '(keys+pad, +hats, +bass, +kick).'),
    dict(slot=12, sid='dh12-tarnished-blue', title='Tarnished Blue', bpm=121, key='G# minor',
         energy=2.5, sf=5, n_bars=64, pcs=(25, 38, 4, 89), kick=90, back=('snare', 76, 9),
         swing=False, hats=[(2, 56), (4, 42), (6, 56), (9, 40), (10, 56), (14, 56)], oh=(3, 10, 54),
         loop=[(ch('B3 D#4 F#4 A#4', 'G#1', 'G#2'), 2), (ch('A3 D#4 F#4 G#4', 'B1', 'B2'), 2)],
         sig=(3, '13'),
         keys=[(0, 2.0, 1.0, 58), (0, 3.5, 1.5, 54), (2, 2.0, 1.0, 58), (2, 3.5, 1.5, 54)],
         bass=[[(.5, .4, 'r', 60), (1.5, .4, 'r', 58), (2.5, 1.0, 'r', 62)],
               [(.5, .4, 'r', 60), (2.5, .4, 'f', 56), (3.5, .4, 'r', 58)]],
         drops=[(33, 40, {'kick_broken'})], pad=(33, 56),
         break_txt='브로큰 킥(1박 + 2박 뒷박만, 2-스텝), 나머지 유지 + 패드 진입',
         loop_txt='G♯m9 ↔ B13 (i–♭III13, A 내추럴 7도, D♯·F♯ 공통음), 2마디씩, EP 3박 1박 + 4박 뒷박 1.5박 마디 걸침',
         bass_txt='1·2·3박 뒷박 3개(마지막만 1박 길이) / 1박 뒷박 + 3박 뒷박 5도 아래(B1 구간만 F♯1) + 4박 뒷박',
         feature='6/16 햇(뒷박 + 2박 정박 + 3박 첫 16분 고스트), 약한 스네어, 오픈햇 3마디에 1개, 브레이크는 킥만 2-스텝으로 쪼개고 패드가 들어옵니다',
         notes='G#m9 <-> B13 (i - bIII thirteenth; A natural on top of the shared D# and F#); EP '
               'plays beat 3 then pushes the and-of-4 across the bar line; three off-beat subs; '
               'break turns the kick into a broken 2-step (one and the and-of-2) and adds the pad.'),
    dict(slot=15, sid='dh15-deep-meridian', title='Deep Meridian', bpm=122, key='Bb minor',
         energy=3, sf=-5, n_bars=64, pcs=(25, 38, 4, 89), kick=92, back=('snare+clap', 80, 9),
         swing=False,
         hats=[(2, 60), (3, 40), (4, 44), (6, 60), (8, 44), (10, 60), (11, 40), (12, 44),
               (14, 60), (15, 40)], oh=(2, 6, 56),
         loop=[(ch('Db3 F3 Ab3 Eb4', 'Bb1', 'Bb2'), 2), (ch('Db3 Gb3 Ab3 Eb4', 'Ab1', 'Ab2'), 2)],
         sig=(10, '7sus4'),
         keys=[(0, .75, .3, 62), (0, 1.5, .3, 54), (1, .75, .3, 60), (1, 3.25, .3, 52),
               (2, .75, .3, 62), (2, 1.5, .3, 54), (3, .75, .3, 60), (3, 3.25, .3, 52)],
         bass=[[(0, .5, 'r', 64), (1.75, .25, 'r', 54), (2.0, 1.25, 'r', 62)],
              [(0, .5, 'r', 64), (2.0, .75, 'r', 60), (3.25, .5, 'r', 56)]],
         drops=[(33, 35, {'hats'}), (36, 38, {'hats', 'bass'}), (39, 40, {'hats', 'bass', 'kick'})],
         pad=(17, 56),
         break_txt='3단 감산: 33–35 햇 아웃 → 36–38 +베이스 아웃 → 39–40 +킥 아웃(스네어·EP·패드만)',
         loop_txt='B♭m11 ↔ A♭7sus4 (i–♭VII7sus4, F→G♭ 한 성부만), 2마디씩, EP 1박 둘째 16분 + 2박 뒷박(또는 4박 둘째 16분) 짧은 스탭',
         bass_txt='1박 반 박 + 2박 마지막 16분 고스트 + 3박 1.25박 / 1박 반 박 + 3박 + 4박 둘째 16분 짧게(근음만, B♭1·A♭1)',
         feature='피크입니다. 킥 92, 10/16 햇, 스네어+클랩, 패드 17마디부터, 브레이크는 3마디·3마디·2마디로 햇 → 베이스 → 킥 순서로 걷어 냅니다',
         notes='Peak. Bbm11 <-> Ab7sus4 (i - bVII seventh-sus, only F -> Gb moves); short EP '
               'stabs on the e-of-1 plus the and-of-2 or the e-of-4; 10/16 hats; snare with a '
               'clap under it; low pad from 17; break strips hats, then bass, then kick.'),
    dict(slot=18, sid='dh18-smoke-orchard', title='Smoke Orchard', bpm=123, key='F minor',
         energy=3, sf=-4, n_bars=64, pcs=(25, 38, 16, None), kick=93, back=('rim', 80, 9),
         swing=False,
         hats=[(2, 58), (3, 42), (6, 58), (7, 42), (10, 58), (11, 42), (14, 58), (15, 42)],
         oh=(4, 6, 56),
         loop=[(ch('Ab3 C4 Eb4 G4', 'F2'), 2), (ch('Ab3 Bb3 Db4 Fb4', 'Gb2'), 2)],
         sig=(1, '9'),
         keys=[(0, 1.5, 2.0, 58), (0, 3.5, .35, 52), (1, 1.5, 1.0, 54),
               (2, 1.5, 2.0, 58), (2, 3.5, .35, 52), (3, 1.5, 1.0, 54)],
         bass=[[(0, .5, 'r', 64), (1.5, 1.0, 'o', 62), (3.5, .4, 'r', 58)],
               [(.5, .4, 'r', 60), (1.5, 1.0, 'o', 62), (3.0, .4, 'f', 56)]],
         drops=[(33, 38, {'bass'}), (39, 40, {'kick', 'back', 'hats', 'bass'})], pad=None,
         break_txt='33–38 베이스만 아웃 → 39–40 드럼·베이스 전부 멈추고 오르간 2마디 공백',
         loop_txt='Fm9 ↔ G♭9 (i–♭II9 프리지안 도미넌트, A♭ 유지·C→B♭·E♭→D♭·G→F♭), 2마디씩, 오르간 2박 뒷박 2박 + 4박 뒷박 짧게',
         bass_txt='1박 반 박 + 2박 뒷박 옥타브 아래 1박(F2→F1) + 4박 뒷박 / 1박 뒷박 + 옥타브 아래 + 3박 5도 아래',
         feature='피크입니다. 킥 93, 뒷박+마지막 16분 짝 햇 8개, 림, 브레이크 끝 2마디에 드럼이 완전히 멈췄다가 41마디 크래시로 돌아옵니다',
         notes='Peak. Fm9 <-> Gb9 (i - bII dominant ninth, phrygian shade; three voices step '
               'down under a held Ab); tonewheel organ from the and-of-2; sub drops an octave '
               'on the and-of-2; break drops the bass, then stops all drums for two bars.'),
    dict(slot=21, sid='dh21-slow-orbit', title='Slow Orbit', bpm=121, key='G minor', energy=2,
         sf=-2, n_bars=64, pcs=(25, 38, 4, 89), kick=87, back=('rim', 74, 9), swing=True,
         hats=[(0, 40), (2, 50), (4, 40), (6, 50), (8, 40), (10, 50), (14, 50)], oh=(4, 14, 50),
         loop=[(ch('F3 A3 Bb3 D4', 'G1', 'G2'), 2), (ch('F3 Ab3 C4 Eb4', 'Db2', 'Db2'), 2)],
         sig=(6, 'maj9'),
         keys=[(k, 0, 3.75, 58 if k % 2 == 0 else 52) for k in range(4)],
         bass=[[(0, 5.5, 'r', 60)], [(2.0, .5, 'f', 54), (3.0, .75, 'r', 58)]],
         drops=[(33, 40, {'kick', 'back', 'hats', 'keys'})], pad=(9, 56),
         break_txt='서브+패드만(드럼·EP 아웃)',
         loop_txt='Gm9 ↔ D♭maj9 (i–♭V maj9 트라이톤 이웃, F 공통음·A→A♭·B♭→C·D→E♭), 2마디씩, EP 매 마디 1박 3.75박 홀드(둘째 마디는 약하게)',
         bass_txt='G1→D♭2: 1박부터 5.5박 롱 서브 / 다음 마디 3박 짧게(D♭ 구간만 5도 아래 G♭1) + 4박 근음',
         feature='드리프트입니다. 패드 9마디부터, 스윙 8분 햇에서 4박 정박만 비우고, 브레이크는 서브와 패드만 남깁니다',
         notes='Drift. Gm9 <-> Dbmaj9 (i - bV major ninth, a tritone neighbour sharing F); EP '
               're-holds every bar, softer on the second; long 5.5-beat sub; low pad from bar 9; '
               'break leaves only the sub and the pad.'),
    dict(slot=24, sid='dh24-umber-lane', title='Umber Lane', bpm=120, key='D minor', energy=2,
         sf=-1, n_bars=64, pcs=(25, 33, 0, 89), kick=86, back=('snare', 74, 9), swing=False,
         hats=[(1, 40), (2, 52), (6, 52), (9, 40), (10, 52), (14, 52)], oh=(2, 10, 50),
         loop=[(ch('A3 C4 F4 G4', 'D2', 'D2'), 2), (ch('Ab3 C4 F4 G4', 'D2', 'D2'), 2)],
         sig=(0, 'm7b5'),
         keys=[(0, 2.0, 5.5, 58), (2, 2.0, 5.5, 56)],
         bass=[[(.75, .75, 'r', 62), (2.0, .5, 'r', 58), (2.75, .75, 'r', 60)],
               [(.75, .75, 'r', 62), (3.0, .75, 'f', 56)]],
         drops=[(33, 40, {'hats', 'back', 'keys', 'pad'})], pad=(25, 56),
         break_txt='킥+서브만(햇·스네어·피아노·패드 아웃)',
         loop_txt='Dm11 ↔ Dm11♭5 (토닉이 반쯤 꺼지는 i–i ø, A→A♭ 한 음), 2마디씩, 그랜드 피아노 3박에서 들어와 5.5박 홀드',
         bass_txt='1박 둘째 16분 0.75박 + 3박 짧게 + 3박 둘째 16분 / 1박 둘째 16분 + 4박 5도 아래(A1)',
         feature='e+& 짝 햇 6개, 약한 스네어, 오픈햇 2마디에 1개, 패드 25마디부터, 브레이크는 킥과 서브만 남깁니다',
         notes='Dm11 <-> Dm11b5 (the tonic half-darkens: only A -> Ab moves); soft grand piano '
               'enters on beat 3 and holds 5.5 beats; finger bass on the e-of-1 and e-of-3; '
               'pad from 25; break is kick and sub only.'),
    dict(slot=27, sid='dh27-quiet-pier', title='Quiet Pier', bpm=118, key='D minor', energy=1,
         sf=-1, n_bars=64, pcs=(25, 38, 4, None), kick=82, back=('rim', 70, 9), swing=False,
         hats=[(6, 46), (13, 40), (14, 48)], oh=(4, 2, 48),
         loop=[(ch('F3 A3 C4 E4', 'D2'), 2), (ch('F3 G3 C4', 'F1'), 2)],
         sig=(3, 'sus2'),
         keys=[(0, 0, 2.0, 56), (1, 2.0, .5, 50), (2, 0, 2.0, 54), (3, 2.0, .5, 50)],
         bass=[[(0, 2.5, 'r', 60)], [], [(1.5, 1.5, 'r', 58)], [(3.5, .4, 'f', 54)]],
         drops=[(33, 40, {'kick', 'hats', 'bass'})], pad=None,
         break_txt='림+EP만(킥·햇·베이스 아웃)',
         loop_txt='Dm9 ↔ Fsus2 (i–♭III sus2, A→G 한 음, 3도 없음), 2마디씩, EP 1박 2박 + 2마디째 3박 짧은 터치',
         bass_txt='4마디 셀: 1마디째 1박 2.5박(D2), 3마디째 2박 뒷박 1.5박, 4마디째 4박 뒷박 짧게(F1), 2마디째 쉼',
         feature='쿨다운입니다. 햇 3개(2박 뒷박 + 4박 앞 16분 고스트 + 4박 뒷박), 림, 브레이크는 림과 EP만 남깁니다',
         notes='Cooldown. Dm9 <-> Fsus2 (i - bIII sus2, only A -> G moves); EP plays a half-bar '
               'chord on the one and a short touch in the second bar; four-bar sub cell with one '
               'empty bar; three hats per bar; break is rim and EP alone.'),
    dict(slot=30, sid='dh30-house-lights', title='House Lights', bpm=116, key='A minor', energy=1,
         sf=0, n_bars=72, pcs=(25, 38, 0, 89), kick=82, back=('rim', 70, 9), swing=False,
         hats=[(2, 46), (7, 40), (10, 46)], oh=(4, 14, 48),
         loop=[(ch('G3 B3 C4 E4', 'A1', 'A2'), 2), (ch('F#3 B3 E4', 'E1', 'E2'), 2)],
         sig=(7, 'sus2'),
         keys=[(0, .5, 3.0, 56), (1, 2.5, 1.0, 50), (2, .5, 3.0, 54), (3, 2.5, 1.0, 50)],
         bass=[[(0, 1.0, 'r', 60), (2.5, .5, 'r', 56)], []],
         drops=[(33, 40, {'kick', 'back', 'bass'}),
                (61, 64, {'back'}), (65, 68, {'back', 'hats'}),
                (69, 71, {'back', 'hats', 'bass'}), (72, 72, {'back', 'hats', 'bass', 'kick_one'})],
         pad=(17, 56),
         break_txt='햇+피아노+패드(킥·림·베이스 아웃)',
         loop_txt='Am9 ↔ Esus2 (i–v sus2, 3도 없음, F♯ 도리안 색), 2마디씩, 그랜드 피아노 1박 뒷박 3박 + 2마디째 3박 뒷박 짧게',
         bass_txt='1박 1박 + 3박 뒷박 짧게, 2마디째 쉼(아웃트로는 A1 토닉)',
         feature='클로저, 72마디입니다. 아웃트로 57–72의 16마디에서 57–60 드럼+베이스 → 61–64 림 아웃 → 65–68 햇 아웃(킥+베이스) → 69–71 킥만 → 72마디 1박 킥 하나로 끝납니다',
         notes='Closer. Am9 <-> Esus2 (i - v sus2, no third, dorian F#); soft grand from the '
               'and-of-1; break keeps hats, piano and pad; 72 bars so the outro is 16 bars and '
               'thins rim -> hats -> bass until one kick on the one of bar 72.'),
]


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def section(b):
    return ('intro' if b <= 16 else 'A' if b <= 32 else 'break' if b <= 40
            else 'A2' if b <= 56 else 'outro')


def compose(sid):
    """Return nt, cc, pcs, n_bars, bpm, title, keysig_sf, minor."""
    sp = next((s for s in SKETCHES if s['sid'] == sid), None)
    if sp is None:
        raise ValueError('Unknown sketch: ' + sid)
    n_bars = sp['n_bars']
    end = n_bars * BAR
    ntr = 4 if sp['pcs'][3] is not None else 3
    nt = {i: [] for i in range(ntr)}
    cc = {i: [] for i in range(ntr)}
    pcs = {i: sp['pcs'][i] for i in range(ntr)}
    cc[2].append((0, 64, 0))
    loop = sp['loop']
    cycle = sum(n for _, n in loop)
    starts, acc = [], 0
    for _, n in loop:
        starts.append(acc)
        acc += n
    tonic = loop[0][0]
    base = sp['slot'] * 100000 + 31

    def note(tr, tick, dur, pitch, vel):
        tick = max(0, tick)
        dur = min(dur, end - 1 - tick)
        if dur > 0:
            nt[tr].append((tick, dur, pitch, vel))

    def dropped(b, part):
        return any(lo <= b <= hi and part in parts for lo, hi, parts in sp['drops'])

    def chord_at(b):
        pos = (b - 1) % cycle
        return loop[max(i for i, s in enumerate(starts) if s <= pos)][0]

    for b in range(1, n_bars + 1):
        sec = section(b)
        o = bt(b)

        # ---- drums
        seed(base + b * 10)
        if not dropped(b, 'kick'):
            beats = ((0,) if dropped(b, 'kick_one') else (0, 1.5) if dropped(b, 'kick_broken')
                     else (0, 1, 2, 3))
            for beat in beats:
                v = clamp(hum_v(sp['kick'] + (2 if beat == 0 else -3 if beat % 2 else 0), 5), 78, 96)
                t = hum_t(bt(b, beat), 7)
                note(0, max(o, t) if b == n_bars else t, 100, KICK, v)   # last kick stays in the last bar
        kind, bvel, bfrom = sp['back']
        if b >= bfrom and not dropped(b, 'back'):
            for beat in (1, 3):
                t = hum_t(bt(b, beat), 7)
                for pitch, dv in BACK[kind]:
                    lo, hi = (70, 85) if pitch != CLAP else (50, 66)
                    note(0, t, 90, pitch, clamp(hum_v(bvel + dv, 5), lo, hi))
        seed(base + b * 10 + 1)
        if not dropped(b, 'hats'):
            every, ostep, ovel = sp['oh']
            steps = dict(sp['hats'])
            if b % every == 0:
                steps[ostep] = None
            for step in sorted(steps):
                shift = (SW if step % 4 == 2 else SW // 2 if step % 2 else 0) if sp['swing'] else 0
                t = hum_t(o + step * S16 + shift, 6)
                if steps[step] is None:
                    note(0, t, int(PPQ * .45), OHAT, clamp(hum_v(ovel, 4), 46, 60))
                else:
                    note(0, t, 50, HAT, clamp(hum_v(steps[step], 5), 40, 64))
        if b == 41:
            note(0, o, PPQ, CRASH, 80)

        # ---- bass: tonic in intro/outro (mix-safe), chord root in A / break / A2
        seed(base + b * 10 + 2)
        if b >= 9 and not dropped(b, 'bass'):
            root = (tonic if sec in ('intro', 'outro') else chord_at(b))['bass']
            for beat, dur, deg, v in sp['bass'][(b - 1) % len(sp['bass'])]:
                pitch = {'r': root, 'f': root - 5, 'o': root - 12}[deg]
                if pitch < 28:
                    pitch = root
                assert 28 <= pitch <= 45, (sid, b, pitch)
                stop = bt(b + 1) if dropped(b + 1, 'bass') else end   # no sub into a bass drop
                s = hum_t(bt(b, beat), 5)
                note(1, s, min(int(dur * PPQ) - 20, stop - s - 10), pitch, clamp(hum_v(v, 4), 52, 70))

        # ---- keys: hint from bar 12, out before the outro
        seed(base + b * 10 + 3)
        if 12 <= b <= KEYS_LAST and not dropped(b, 'keys'):
            pos = (b - 1) % cycle
            soft = 6 if sec == 'intro' else 0
            events = [ev for ev in sp['keys'] if ev[0] == pos]
            if b == 12 and not events:
                events = [(pos, 0, 3.5, 58)]
            for _, beat, dur, v in events:
                s = hum_t(bt(b, beat), 6)
                cb = (bt(b, beat) + PPQ // 2) // BAR + 1   # chord by nominal position, not jitter
                if cb > KEYS_LAST or dropped(cb, 'keys'):
                    continue
                e = min(s + int(dur * PPQ), bt(KEYS_LAST + 1) - 1)
                nb = cb + 1
                while nb <= KEYS_LAST and bt(nb) < e:      # cut a hold at a keys drop
                    if dropped(nb, 'keys'):
                        e = bt(nb) - 1
                        break
                    nb += 1
                for p in chord_at(cb)['v']:
                    assert 48 <= p <= 72, (sid, p)
                    note(2, s, e - s - 15, p, clamp(hum_v(v - soft, 4), 50, 70))
                if dur >= 1.5:   # held: catch, re-pedal at every bar line, release at the end
                    cc[2] += [(s, 64, 0), (s + 12, 64, 127)]
                    nb = b + 1
                    while bt(nb) < e:
                        cc[2] += [(bt(nb), 64, 0), (bt(nb) + 12, 64, 127)]
                        nb += 1
                    cc[2].append((e, 64, 0))

        # ---- pad: low root + fifth, one pair per chord span (or from pad start / after a drop)
        if ntr == 4 and sp['pad']:
            pf, pt = sp['pad']
            pt = min(pt, KEYS_LAST)
            pos = (b - 1) % cycle
            fresh = b == pf or pos in starts or dropped(b - 1, 'pad')
            if pf <= b <= pt and not dropped(b, 'pad') and fresh:
                seed(base + b * 10 + 4)
                nb = b + 1
                while nb <= pt and (nb - 1) % cycle not in starts and not dropped(nb, 'pad'):
                    nb += 1
                r = chord_at(b)['pad']
                v = 38 if sec == 'intro' else 44
                for p in (r, r + 7):
                    note(3, hum_t(o, 6), bt(min(nb, pt + 1)) - o - 40, p, clamp(hum_v(v, 4), 35, 50))

    cc[2].append((end - 1, 64, 0))
    return nt, cc, pcs, n_bars, sp['bpm'], sp['title'], sp['sf'], True


def audit(nt, n_bars):
    """Measured ranges vs the brief's recipe; FAIL flags anything outside it."""
    drums = nt[0]
    k = [v for _, _, p, v in drums if p == KICK]
    h = [v for _, _, p, v in drums if p == HAT]
    bk = [v for _, _, p, v in drums if p in (RIM, SNARE)]
    cl = [v for _, _, p, v in drums if p == CLAP]
    oh = sum(1 for _, _, p, _ in drums if p == OHAT)
    bass = [p for _, _, p, _ in nt[1]]
    bv = [v for _, _, _, v in nt[1]]
    keys = [p for _, _, p, _ in nt[2]]
    kv = [v for _, _, _, v in nt[2]]
    pad = nt.get(3, [])
    pv = [v for _, _, _, v in pad] or [40]
    last_key_bar = (max(t + d for t, d, _, _ in nt[2]) - 1) // BAR + 1
    last_end = max(t + d for tr in nt.values() for t, d, _, _ in tr)
    oh_per64 = oh * 64 / n_bars
    ok = (78 <= min(k) and max(k) <= 96 and 40 <= min(h) and max(h) <= 64
          and 70 <= min(bk) and max(bk) <= 85 and (not cl or max(cl) <= 66)
          and 28 <= min(bass) and max(bass) <= 45 and max(bv) < max(k)
          and 48 <= min(keys) and max(keys) <= 72 and 50 <= min(kv) and max(kv) <= 70
          and 35 <= min(pv) and max(pv) <= 50 and 12 <= oh_per64 <= 32
          and last_key_bar <= KEYS_LAST and last_end <= n_bars * BAR)
    return (f'  check {"OK" if ok else "FAIL"} kick {min(k)}-{max(k)} hat {min(h)}-{max(h)} '
            f'back {min(bk)}-{max(bk)} clap={len(cl)} oh={oh}/{n_bars}bars bass {min(bass)}-{max(bass)} '
            f'v{min(bv)}-{max(bv)} keys {min(keys)}-{max(keys)} v{min(kv)}-{max(kv)} pad={len(pad)} '
            f'last_key_bar={last_key_bar} last_end_bar={last_end / BAR:.3f}')


def set_audit():
    """Signatures new vs astra/fable/brief; cells, hat sets and breaks distinct inside this batch."""
    sigs = [s['sig'] for s in SKETCHES]
    clash = [s for s in sigs if s in SIGS_TAKEN]
    cells = [repr(s['bass']) for s in SKETCHES]
    hats = [tuple(st for st, _ in s['hats']) for s in SKETCHES]
    brk = [repr(sorted((lo, hi, sorted(p)) for lo, hi, p in s['drops'] if lo <= 40))
           for s in SKETCHES]
    ok = (not clash and len(set(sigs)) == 10 and len(set(cells)) == 10
          and len(set(hats)) == 10 and len(set(brk)) == 10)
    return (f'set check {"OK" if ok else "FAIL"} sigs_unique={len(set(sigs))}/10 '
            f'taken_clash={clash} bass_cells={len(set(cells))}/10 hat_sets={len(set(hats))}/10 '
            f'breaks={len(set(brk))}/10')


if __name__ == '__main__':
    import sys
    lines = []
    for sk in SKETCHES:
        nt, cc, pcs, n_bars, bpm, title, sf, minor = compose(sk['sid'])
        smf = build_smf(title, bpm, sf, minor, n_bars, TRACKS[:len(pcs)],
                        pcs, nt, cc, markers=MARKERS)
        print(f'slot {sk["slot"]:02d} ' + write_smf(os.path.join(SK_DIR, sk['sid'] + '-v1.mid'), smf))
        lines.append(audit(nt, n_bars)); print(lines[-1])
    lines.append(set_audit()); print(lines[-1])
    sys.exit(1 if any('FAIL' in ln for ln in lines) else 0)
