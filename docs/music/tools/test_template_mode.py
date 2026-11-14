"""템플릿 모드(pipeline.produce(template=...)) 단위 테스트 — Logic 을 건드리지 않는다.

실행: python3 -m unittest docs/music/tools/test_template_mode.py
seed 20261113-220009-a606, test-plan T1–T8.
"""
import contextlib
import hashlib
import os
import plistlib
import shutil
import struct
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P  # noqa: E402

# RED 단계(2026-11-13)에서 변경 전 build_smf 로 고정한 골든 다이제스트 — pcs 딕셔너리 경로는 바이트가 변하면 안 된다.
GOLDEN_ARGS = ('golden', 100, 0, False, 2, [('A', 0), ('B', 1)], {0: 1, 1: 33},
               {0: [(0, 240, 60, 100)], 1: [(P.BAR, 240, 40, 90)]}, {0: [(0, 64, 127)]})
GOLDEN_SHA = 'a42aaa7fe3ece723e6f51310409743589d5c2a935d90e71bbb3e85f10e7a6bf5'


def _write(path, data):
    with open(path, 'wb') as f:
        f.write(data)


def _read(path):
    with open(path, 'rb') as f:
        return f.read()


def _plist_logicx(root, tracks=4, bpm=92.0, fmt=plistlib.FMT_XML, extra=None, drop=()):
    alt = os.path.join(root, 'Alternatives', '000')
    os.makedirs(alt, exist_ok=True)
    d = {'NumberOfTracks': tracks, 'BeatsPerMinute': bpm, 'SongName': 'x'}
    d.update(extra or {})
    for k in drop:
        d.pop(k, None)
    with open(os.path.join(alt, 'MetaData.plist'), 'wb') as f:
        plistlib.dump(d, f, fmt=fmt)
    with open(os.path.join(alt, 'ProjectData'), 'wb') as f:
        f.write(b'data')
    return root


class T1BuildSmfPcsNone(unittest.TestCase):
    def test_pcs_dict_bytes_unchanged(self):
        smf = P.build_smf(*GOLDEN_ARGS, markers=[(2, 'M')])
        self.assertEqual(hashlib.sha256(smf).hexdigest(), GOLDEN_SHA)

    def test_pcs_none_emits_no_program_change(self):
        args = list(GOLDEN_ARGS)
        args[6] = None
        smf = P.build_smf(*args)
        _, ntrk, _, info = P.parse_smf(smf)
        self.assertEqual(ntrk, 3)
        for tr in info:
            self.assertEqual(tr['pcs'], [])

    def test_pcs_none_track_has_only_name_and_notes(self):
        smf = P.build_smf('t', 100, 0, False, 1, [('Only', 0)], None, {0: [(0, 100, 60, 90)]}, {})
        _, _, _, info = P.parse_smf(smf)
        self.assertEqual(info[1]['notes'], 1)
        self.assertEqual(info[1]['ccs'], [])
        self.assertEqual(info[1]['pcs'], [])


class T2ParseSmfCcAndFirstNote(unittest.TestCase):
    def test_ccs_and_first_note_tick(self):
        smf = P.build_smf('t', 100, 0, False, 2, [('A', 0), ('B', 1)], {0: 1, 1: 2},
                          {0: [(P.BAR + 7, 100, 60, 90)], 1: []},
                          {0: [(0, 7, 100), (10, 10, 64)], 1: []})
        _, _, _, info = P.parse_smf(smf)
        self.assertEqual(info[1]['ccs'], [7, 10])
        self.assertEqual(info[1]['first_note_tick'], P.BAR + 7)
        self.assertIsNone(info[2]['first_note_tick'])
        self.assertEqual(info[2]['ccs'], [])
        self.assertIsNone(info[0]['first_note_tick'])

    def test_velocity_zero_note_on_is_not_a_note(self):
        smf = P.build_smf('t', 100, 0, False, 1, [('A', 0)], {0: 1}, {0: [(0, 100, 60, 0)]}, {})
        _, _, _, info = P.parse_smf(smf)
        self.assertEqual(info[1]['notes'], 0)
        self.assertIsNone(info[1]['first_note_tick'])

    def test_last_note_off_tick(self):
        smf = P.build_smf('t', 100, 0, False, 2, [('A', 0)], {0: 1},
                          {0: [(0, 100, 60, 90), (P.BAR, 300, 62, 90)]}, {})
        _, _, _, info = P.parse_smf(smf)
        self.assertEqual(info[1]['last_note_off_tick'], P.BAR + 300)


class T3TemplateMeta(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_reads_tracks_and_bpm_xml(self):
        root = _plist_logicx(os.path.join(self.tmp, 'a.logicx'))
        self.assertEqual(P.template_meta(root), {'tracks': 4, 'bpm': 92.0})

    def test_reads_binary_plist(self):
        root = _plist_logicx(os.path.join(self.tmp, 'b.logicx'), tracks=3, bpm=120, fmt=plistlib.FMT_BINARY)
        self.assertEqual(P.template_meta(root), {'tracks': 3, 'bpm': 120.0})

    def test_missing_plist_raises(self):
        root = os.path.join(self.tmp, 'c.logicx')
        os.makedirs(root)
        with self.assertRaises(P.TemplateError):
            P.template_meta(root)

    def test_missing_or_bad_fields_raise(self):
        for i, kw in enumerate((dict(drop=('NumberOfTracks',)), dict(drop=('BeatsPerMinute',)),
                                dict(tracks=0), dict(tracks='4'), dict(bpm=0), dict(bpm='fast'))):
            root = _plist_logicx(os.path.join(self.tmp, f'd{i}.logicx'), **kw)
            with self.assertRaises(P.TemplateError, msg=str(kw)):
                P.template_meta(root)

    def test_only_alternative_000_is_read(self):
        root = _plist_logicx(os.path.join(self.tmp, 'e.logicx'), tracks=4)
        alt1 = os.path.join(root, 'Alternatives', '001')
        os.makedirs(alt1)
        with open(os.path.join(alt1, 'MetaData.plist'), 'wb') as f:
            plistlib.dump({'NumberOfTracks': 9, 'BeatsPerMinute': 60.0}, f)
        self.assertEqual(P.template_meta(root)['tracks'], 4)


class T4TreeHash(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.a = _plist_logicx(os.path.join(self.tmp, 'a.logicx'))
        os.makedirs(os.path.join(self.a, 'Media', 'sub'))
        with open(os.path.join(self.a, 'Media', 'sub', 'x.bin'), 'wb') as f:
            f.write(b'\x00\x01')
        self.b = os.path.join(self.tmp, 'b.logicx')
        shutil.copytree(self.a, self.b)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_copies_hash_equal(self):
        self.assertEqual(P.tree_hash(self.a), P.tree_hash(self.b))

    def test_one_byte_change_differs(self):
        p = os.path.join(self.b, 'Media', 'sub', 'x.bin')
        with open(p, 'wb') as f:
            f.write(b'\x00\x02')
        self.assertNotEqual(P.tree_hash(self.a), P.tree_hash(self.b))

    def test_rename_add_delete_swap_differ(self):
        base = P.tree_hash(self.a)
        os.rename(os.path.join(self.b, 'Media', 'sub', 'x.bin'), os.path.join(self.b, 'Media', 'sub', 'y.bin'))
        self.assertNotEqual(base, P.tree_hash(self.b))
        c = os.path.join(self.tmp, 'c.logicx')
        shutil.copytree(self.a, c)
        _write(os.path.join(c, 'Media', 'new'), b'')
        self.assertNotEqual(base, P.tree_hash(c))
        d = os.path.join(self.tmp, 'd.logicx')
        shutil.copytree(self.a, d)
        p1, p2 = os.path.join(d, 'Media', 'sub', 'x.bin'), os.path.join(d, 'Alternatives', '000', 'ProjectData')
        c1, c2 = _read(p1), _read(p2)
        _write(p1, c2)
        _write(p2, c1)
        self.assertNotEqual(base, P.tree_hash(d))

    def test_empty_dir_allowed_and_symlink_rejected(self):
        e = os.path.join(self.tmp, 'e.logicx')
        os.makedirs(e)
        self.assertIsInstance(P.tree_hash(e), str)
        os.symlink(os.path.join(self.a, 'Media'), os.path.join(self.b, 'Link'))
        with self.assertRaises(P.TemplateError):
            P.tree_hash(self.b)


def _smf_with_tracks(n, bpm=100):
    tracks = [(f'T{i}', i) for i in range(n)]
    nt = {i: [(P.BAR, 100, 60, 90)] for i in range(n)}
    return P.build_smf('pf', bpm, 0, False, 2, tracks, None, nt, {})


class T5Preflight(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tpl = _plist_logicx(os.path.join(self.tmp, 'tpl.logicx'), tracks=4, bpm=92)
        self.proj_dir = os.path.join(self.tmp, 'projects')
        os.makedirs(self.proj_dir)
        self.mid4 = os.path.join(self.tmp, 'four.mid')
        _write(self.mid4, _smf_with_tracks(4))
        self.mid5 = os.path.join(self.tmp, 'five.mid')
        _write(self.mid5, _smf_with_tracks(5))
        self.patch = mock.patch.object(P, 'PROJ_DIR', self.proj_dir)
        self.patch.start()
        self.osa = mock.patch.object(P, 'osa', side_effect=AssertionError('osascript must not run in preflight'))
        self.osa.start()

    def tearDown(self):
        self.osa.stop()
        self.patch.stop()
        shutil.rmtree(self.tmp)

    def test_ok_returns_meta_with_smf_tracks(self):
        m = P.preflight_template(self.tpl, 'proj x', self.mid4)
        self.assertEqual((m['tracks'], m['bpm'], m['smf_tracks'], m['smf_bpm']), (4, 92.0, 4, 100.0))
        self.assertEqual(m['copy'], os.path.join(self.proj_dir, 'proj x.logicx'))

    def test_missing_template(self):
        with self.assertRaisesRegex(P.TemplateError, 'template'):
            P.preflight_template(os.path.join(self.tmp, 'nope.logicx'), 'p', self.mid4)

    def test_copy_exists(self):
        os.makedirs(os.path.join(self.proj_dir, 'p.logicx'))
        with self.assertRaisesRegex(P.TemplateError, 'exists'):
            P.preflight_template(self.tpl, 'p', self.mid4)

    def test_too_many_smf_tracks_conductor_excluded(self):
        with self.assertRaisesRegex(P.TemplateError, 'tracks'):
            P.preflight_template(self.tpl, 'p', self.mid5)

    def test_fewer_smf_tracks_than_template_rejected(self):
        mid3 = os.path.join(self.tmp, 'three.mid'); _write(mid3, _smf_with_tracks(3))
        with self.assertRaisesRegex(P.TemplateError, 'must match'):
            P.preflight_template(self.tpl, 'p', mid3)

    def test_non_44_and_tempo_map_rejected(self):
        tracks = [(f'T{i}', i) for i in range(4)]; nt = {i: [(P.BAR, 100, 60, 90)] for i in range(4)}
        m34 = os.path.join(self.tmp, 'm34.mid'); _write(m34, P.build_smf('x', 100, 0, False, 2, tracks, None, nt, {}, timesig=(3, 4)))
        with self.assertRaisesRegex(P.TemplateError, '4/4'):
            P.preflight_template(self.tpl, 'p', m34)
        mt = os.path.join(self.tmp, 'mt.mid'); _write(mt, P.build_smf('x', 100, 0, False, 2, tracks, None, nt, {}, tempos=[(P.BAR, 120)]))
        with self.assertRaisesRegex(P.TemplateError, 'one tempo'):
            P.preflight_template(self.tpl, 'p', mt)
        # 4/4 → 7/8 → 4/4 같은 박자 변경: 마지막 0x58 만 보면 통과하므로 개수를 센다
        buf = P.build_smf('x', 100, 0, False, 2, tracks, None, nt, {})
        cond_end = 14 + 8 + struct.unpack('>I', buf[18:22])[0]
        cond = buf[22:cond_end]
        extra = b'\x00' + bytes([0xFF, 0x58, 4, 7, 3, 24, 8]) + b'\x00' + bytes([0xFF, 0x58, 4, 4, 2, 24, 8])
        # 끝 메타(FF 2F 00) 앞에 삽입
        assert cond.endswith(b'\xff\x2f\x00')
        cond2 = cond[:-4] + extra + cond[-4:]
        buf2 = buf[:14] + b'MTrk' + struct.pack('>I', len(cond2)) + cond2 + buf[cond_end:]
        _, _, _, info = P.parse_smf(buf2)
        self.assertEqual(info[0]['n_timesig'], 3)
        mts = os.path.join(self.tmp, 'mts.mid'); _write(mts, buf2)
        with self.assertRaisesRegex(P.TemplateError, 'constant 4/4'):
            P.preflight_template(self.tpl, 'p', mts)

    def test_names_with_quotes_rejected_before_logic(self):
        for bad in ('He said "x"', 'back\\slash', 'a/b'):
            with self.assertRaisesRegex(P.TemplateError, 'quote'):
                P.preflight_template(self.tpl, bad, self.mid4)

    def test_duplicate_track_name_prefixes_rejected(self):
        mid = os.path.join(self.tmp, 'dup.mid')
        tracks = [('Strings Hi Violin', 0), ('Strings Hi Viola', 1)]
        _write(mid, P.build_smf('d', 100, 0, False, 2, tracks, None, {i: [(P.BAR, 100, 60, 90)] for i in range(2)}, {}))
        with self.assertRaisesRegex(P.TemplateError, 'distinct'):
            P.preflight_template(self.tpl, 'p', mid)
        mid2 = os.path.join(self.tmp, 'pfx.mid')
        _write(mid2, P.build_smf('d', 100, 0, False, 2, [('Violin', 0), ('Violin 2', 1)], None, {i: [(P.BAR, 100, 60, 90)] for i in range(2)}, {}))
        with self.assertRaisesRegex(P.TemplateError, 'prefix-free'):
            P.preflight_template(self.tpl, 'p', mid2)

    def test_smf_end_bar(self):
        self.assertEqual(P.preflight_template(self.tpl, 'p', self.mid4)['smf_end_bar'], 3)   # 2마디 + END 마커(3마디 시작) = 3
        # 마디선 뒤에 꼬리가 있으면 올림 — 마디 3 중간에 끝나는 노트는 종료 마디 4
        mid = os.path.join(self.tmp, 'tail.mid')
        tracks = [(f'T{i}', i) for i in range(4)]
        nt = {i: [(P.BAR, 100, 60, 90)] for i in range(4)}; nt[0].append((2 * P.BAR + 100, 200, 62, 90))
        _write(mid, P.build_smf('t', 100, 0, False, 2, tracks, None, nt, {}))
        self.assertEqual(P.preflight_template(self.tpl, 'p', mid)['smf_end_bar'], 4)

    def test_failed_name(self):
        self.assertEqual(P.failed_name('proj x', '20261113-220000'), 'proj x.failed-20261113-220000.logicx')


class T6SmokeSmf(unittest.TestCase):
    def test_layout(self):
        import template_smoke as S
        smf = S.smoke_smf()
        _, ntrk, _, info = P.parse_smf(smf)
        self.assertEqual(ntrk, 5)
        self.assertEqual(len(set(P.smf_track_names(smf))), 4)
        self.assertEqual(info[0]['last_tick'], S.SMOKE_BARS * P.BAR)   # END 마커 = 10마디 시작 → 바운스 종료 마디 10
        self.assertEqual(round(60_000_000 / info[0]['tempo_us']), S.SMOKE_BPM)
        self.assertEqual(S.SMOKE_BPM, 100)
        self.assertEqual(S.SMOKE_BARS, 9)
        names = S.SMOKE_TRACKS
        self.assertEqual(len(set(names)), 4)
        starts, ends = [1, 3, 5, 7], [3, 5, 7, 9]
        for i, tr in enumerate(info[1:]):
            self.assertEqual(tr['pcs'], [], i)
            self.assertFalse(set(tr['ccs']) & {0, 7, 10, 32}, i)
            self.assertGreater(tr['notes'], 0, i)
            self.assertGreaterEqual(tr['first_note_tick'], starts[i] * P.BAR, i)
            self.assertLessEqual(tr['last_note_off_tick'], ends[i] * P.BAR, i)
            self.assertGreaterEqual(tr['first_note_tick'], P.BAR, 'bar 1 must be silent')


class _Logic:
    """produce(template=) 의 Logic 접점을 전부 기록용 스텁으로 바꾼다."""

    def __init__(self, windows=(), strips=(('A1', 'B1'), ('A1', 'B1')), open_raises=None):
        self.calls = []
        self.windows = windows
        self.strips = list(strips)
        self.open_raises = open_raises
        self.tmp = tempfile.mkdtemp()
        self.proj_dir = os.path.join(self.tmp, 'projects')
        os.makedirs(self.proj_dir)

    def rec(self, name, ret=None):
        def f(*a, **k):
            self.calls.append((name, a, k))
            return ret
        return f

    def windows_strict(self):
        self.calls.append(('windows_strict', (), {}))
        if isinstance(self.windows, Exception):
            raise self.windows
        return list(self.windows)

    def run(self, cmd, *a, **k):
        self.calls.append(('open', tuple(cmd), {}))
        if self.open_raises:
            raise self.open_raises
        return mock.Mock(returncode=0)

    def mixer_strips(self):
        self.calls.append(('mixer_strips', (), {}))
        return ' '.join(f'[{n}]' for n in self.strips.pop(0)) + ' [Stereo Out] [Master] [1]'

    @contextlib.contextmanager
    def lock(self, owner):
        self.calls.append(('lock', (owner,), {}))
        yield

    def names(self):
        return [c[0] for c in self.calls]

    def __enter__(self):
        forbid = lambda n: mock.patch.object(P, n, side_effect=AssertionError(f'{n} forbidden in template mode'))  # noqa: E731
        self.stack = contextlib.ExitStack()
        s = self.stack
        s.enter_context(mock.patch.object(P, 'PROJ_DIR', self.proj_dir))
        s.enter_context(mock.patch.object(P, 'windows_strict', self.windows_strict))
        s.enter_context(mock.patch.object(P, 'LogicLock', self.lock))
        s.enter_context(mock.patch.object(P.subprocess, 'run', self.run))
        s.enter_context(mock.patch.object(P, 'wait_window', self.rec('wait_window', True)))
        s.enter_context(mock.patch.object(P, 'open_mixer', self.rec('open_mixer')))
        s.enter_context(mock.patch.object(P, 'mixer_strips', self.mixer_strips))
        s.enter_context(mock.patch.object(P, 'close_mixer', self.rec('close_mixer')))
        s.enter_context(mock.patch.object(P, 'dismiss_panels', self.rec('dismiss_panels')))
        s.enter_context(mock.patch.object(P, 'dismiss_crash_reporter', self.rec('dismiss_crash_reporter', False)))
        s.enter_context(mock.patch.object(P, 'click_dialog_button', self.rec('click_dialog_button', False)))
        s.enter_context(mock.patch.object(P, 'menu_click', self.rec('menu_click')))
        s.enter_context(mock.patch.object(P, 'set_library_pane', self.rec('set_library_pane', True)))
        s.enter_context(mock.patch.object(P, 'assert_only_project', self.rec('assert_only_project')))
        s.enter_context(mock.patch.object(P, 'ocr_screen', lambda *a, **k: (_ for _ in ()).throw(AssertionError('ocr_screen must be stubbed at a higher level'))))
        s.enter_context(mock.patch.object(P, 'import_midi_menu', self.rec('import_into_project')))
        s.enter_context(mock.patch.object(P, 'move_regions_to_template', self.rec('move_regions')))
        s.enter_context(mock.patch.object(P, 'track_region_names', lambda n, proj: ['T0', 'T1', 'T2', 'T3'][:n]))
        s.enter_context(mock.patch.object(P, 'lcd_tempo_value', lambda: 100.0))
        s.enter_context(mock.patch.object(P, 'save_quiet', self.rec('save_quiet')))
        s.enter_context(mock.patch.object(P, 'bounce_and_post', lambda *a, **k: (self.calls.append(('bounce_and_post', a, k)) or dict(ok=True, wav='w'))))
        s.enter_context(mock.patch.object(P, 'close_all_projects', self.rec('close_all_projects')))
        s.enter_context(forbid('clear_alerts'))
        s.enter_context(forbid('metronome_off'))
        s.enter_context(forbid('save_project_as'))
        s.enter_context(mock.patch.object(P.time, 'sleep', lambda *_: None))
        return self

    def __exit__(self, *exc):
        self.stack.close()
        shutil.rmtree(self.tmp)


def _fixture(L, tracks=4):
    tpl = _plist_logicx(os.path.join(L.tmp, 'tpl.logicx'), tracks=tracks, bpm=92)
    mid = os.path.join(L.tmp, 's.mid')
    _write(mid, _smf_with_tracks(4))
    return tpl, mid


class THelpers(unittest.TestCase):
    def test_windows_strict_raises_on_query_failure_and_normalizes_nfc(self):
        import unicodedata as ud
        with mock.patch.object(P, 'osa', return_value=(1, '', 'boom')):
            with self.assertRaises(RuntimeError):
                P.windows_strict()
        nfd = ud.normalize('NFD', '프로젝트 선택')
        with mock.patch.object(P, 'osa', return_value=(0, '|' + nfd, '')):
            self.assertEqual(P.windows_strict(), ['프로젝트 선택'])

    def test_save_quiet_uses_menu_not_keystroke(self):
        seen = []
        with mock.patch.object(P, 'osa', side_effect=lambda script, **k: (seen.append(script), (0, '', ''))[1]), \
             mock.patch.object(P.time, 'sleep', lambda *_: None):
            P.save_quiet()
        self.assertIn('click menu item "저장"', seen[0])
        self.assertNotIn('keystroke "s"', seen[0])

    def test_bounce_end_stepper_inserted_only_with_end_bar(self):
        seen = []
        with mock.patch.object(P, 'osa', side_effect=lambda script, **k: (seen.append(script), (0, 'bounce started', ''))[1]):
            P.start_bounce_aiff('P', 'f', end_bar=10)
            P.start_bounce_aiff('P', 'f')
        self.assertIn('if bar = 10 then exit repeat', seen[0])
        self.assertLess(seen[0].index('exit repeat'), seen[0].index('key code 36'))
        self.assertNotIn('종료:', seen[1])

    def test_region_rows_with_fake_ocr(self):
        items = [('Tpl Strings', 650, 461, 619, 454, 64, 14), ('Studio Grand | 채널 1', 368, 473, 306, 466, 125, 14),
                 ('트랜스포즈 없음', 60, 470, 11, 463, 100, 14), ('5', 250, 470, 245, 463, 10, 14),
                 ('Tpl Harpsichord', 760, 527, 717, 519, 89, 17), ('Epic Cloud Formation | 채널 1', 393, 537, 306, 530, 175, 14)]
        with mock.patch.object(P, 'ocr_screen', lambda: items):
            rows = P.region_rows(['Tpl Strings', 'Tpl Harpsichord'])
        self.assertEqual([round(x) for x, _ in rows], [368, 393])
        self.assertEqual([round(y) for _, y in rows], [461, 527])
        with mock.patch.object(P, 'ocr_screen', lambda: items[:1]):
            with self.assertRaisesRegex(P.TemplateError, 'track header not found'):
                P.region_rows(['Tpl Strings'])


class TImportMatching(unittest.TestCase):
    def test_row_pattern_matches_truncated_and_icon_noise_only_with_token(self):
        pat = P.import_row_pattern('221545123')
        self.assertTrue(pat.search('n blue~221545123.mid'))
        self.assertTrue(pat.search('tplsmoke-20...545123.mid'))   # 가운데 줄임: 끝 6자리만 남는다
        self.assertTrue(pat.search('tpls~221545123mid'))
        self.assertFalse(pat.search('blue~221545124.mid'))
        self.assertFalse(pat.search('blue-hour.mid'))
        self.assertFalse(pat.search('221545123.midi'))

    def test_import_copies_to_unique_name_and_removes_it(self):
        tmp = tempfile.mkdtemp()
        try:
            mid = os.path.join(tmp, 'blue-hour.mid'); _write(mid, _smf_with_tracks(2))
            seen = {}
            def fake(path, token, log=print):
                seen['path'] = path; seen['token'] = token; seen['exists'] = os.path.exists(path)
            with mock.patch.object(P, '_import_midi_menu', fake):
                P.import_midi_menu(mid)
            self.assertTrue(seen['exists'])
            self.assertRegex(os.path.basename(seen['path']), r'^blue~\d{9}\.mid$')
            self.assertTrue(seen['path'].endswith(seen['token'] + '.mid'))
            self.assertEqual(sorted(os.listdir(tmp)), ['blue-hour.mid'])
        finally:
            shutil.rmtree(tmp)


class T7StartConditions(unittest.TestCase):
    def test_open_project_window_refuses_before_copy(self):
        with _Logic(windows=['foo - 트랙']) as L:
            tpl, mid = _fixture(L)
            with self.assertRaisesRegex(P.TemplateError, 'open'):
                P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertEqual(os.listdir(L.proj_dir), [])
            self.assertNotIn('open', L.names())

    def test_windows_query_failure_propagates(self):
        with _Logic(windows=RuntimeError('ax down')) as L:
            tpl, mid = _fixture(L)
            with self.assertRaises(RuntimeError):
                P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertEqual(os.listdir(L.proj_dir), [])

    def test_unexpected_window_refuses(self):
        with _Logic(windows=['누락된 샘플']) as L:
            tpl, mid = _fixture(L)
            with self.assertRaisesRegex(P.TemplateError, 'window'):
                P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertEqual(os.listdir(L.proj_dir), [])


class T8TemplateFlow(unittest.TestCase):
    def test_preflight_failure_touches_nothing(self):
        with _Logic(windows=[]) as L:
            tpl, mid = _fixture(L, tracks=2)   # SMF 4 tracks > template 2
            with self.assertRaisesRegex(P.TemplateError, 'tracks'):
                P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertEqual(L.names(), ['lock', 'dismiss_crash_reporter', 'windows_strict'])
            self.assertEqual(os.listdir(L.proj_dir), [])

    def test_happy_path_order_and_copy_only(self):
        with _Logic(windows=[], strips=[('A1', 'B1', 'C1', 'D1'), ('A1', 'B1', 'C1', 'D1')]) as L:
            tpl, mid = _fixture(L)
            before = P.tree_hash(tpl)
            r = P.produce('s', 'Tpl Test', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertTrue(r['ok'], r)
            names = L.names()
            self.assertEqual([n for n in names if n != 'dismiss_crash_reporter'][:2], ['lock', 'windows_strict'])
            copy = os.path.join(L.proj_dir, 'Tpl Test v.logicx')
            self.assertTrue(os.path.isdir(copy))
            i_open = names.index('open')
            self.assertEqual(L.calls[i_open][1], ('open', '-a', P.APP, copy))
            for c in L.calls:
                self.assertNotIn(tpl, [str(x) for x in c[1]], c)
            self.assertLess(names.index('open'), names.index('mixer_strips'))
            self.assertEqual(names.count('mixer_strips'), 2)
            first, second = [i for i, n in enumerate(names) if n == 'mixer_strips']
            self.assertLess(first, names.index('import_into_project'))
            self.assertLess(names.index('import_into_project'), second)
            self.assertLess(second, names.index('save_quiet'))
            self.assertLess(names.index('save_quiet'), names.index('bounce_and_post'))
            self.assertEqual(r['snapshot'], ['A1', 'B1', 'C1', 'D1'])
            self.assertEqual(r['strips'], ['A1', 'B1', 'C1', 'D1'])
            self.assertEqual(r['regions'], ['T0', 'T1', 'T2', 'T3'])
            self.assertEqual(r['tempo'], 100.0)
            self.assertLess(names.index('import_into_project'), names.index('move_regions'))
            self.assertLess(names.index('move_regions'), second)
            self.assertEqual(L.calls[names.index('bounce_and_post')][1][1], 'Tpl Test v.logicx')
            self.assertEqual(P.tree_hash(tpl), before)

    def test_changed_strips_fail_closed_before_bounce(self):
        with _Logic(windows=[], strips=[('A1', 'B1', 'C1', 'D1'), ('A1', 'B1', 'C1', 'D1', 'NEW')]) as L:
            tpl, mid = _fixture(L)
            with self.assertRaisesRegex(P.TemplateError, 'strips changed'):
                P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            names = L.names()
            self.assertEqual(names.count('mixer_strips'), 2)
            self.assertNotIn('bounce_and_post', names)
            self.assertNotIn('save_quiet', names)
            self.assertEqual(len([c for c in L.calls if c[0] == 'close_all_projects']), 1)

    def test_bounce_failure_dict_takes_cleanup_path(self):
        with _Logic(windows=[], strips=[('A1', 'B1', 'C1', 'D1'), ('A1', 'B1', 'C1', 'D1')]) as L:
            tpl, mid = _fixture(L)
            with mock.patch.object(P, 'bounce_and_post', lambda *a, **k: dict(ok=False, stage='file', msg='aif missing')):
                with self.assertRaisesRegex(P.TemplateError, 'bounce failed'):
                    P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertRegex(os.listdir(L.proj_dir)[0], r'\.failed-')
            self.assertEqual(len([c for c in L.calls if c[0] == 'close_all_projects']), 1)

    def test_tempo_mismatch_fails_closed(self):
        with _Logic(windows=[], strips=[('A1', 'B1', 'C1', 'D1'), ('A1', 'B1', 'C1', 'D1')]) as L:
            tpl, mid = _fixture(L)
            with mock.patch.object(P, 'lcd_tempo_value', lambda: 92.0):
                with self.assertRaisesRegex(P.TemplateError, 'tempo'):
                    P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertNotIn('bounce_and_post', L.names())

    def test_region_name_mismatch_fails_closed(self):
        with _Logic(windows=[], strips=[('A1', 'B1', 'C1', 'D1'), ('A1', 'B1', 'C1', 'D1')]) as L:
            tpl, mid = _fixture(L)
            with mock.patch.object(P, 'track_region_names', lambda n, proj: ['T0', '', 'T2', 'T3']):
                with self.assertRaisesRegex(P.TemplateError, 'regions per track'):
                    P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertNotIn('bounce_and_post', L.names())

    def test_cleanup_helper_failure_still_renames_copy_and_reraises_cause(self):
        with _Logic(windows=[], open_raises=RuntimeError('import hung')) as L:
            tpl, mid = _fixture(L)
            with mock.patch.object(P, 'dismiss_panels', side_effect=RuntimeError('ax down')), \
                 mock.patch.object(P, 'close_all_projects', side_effect=RuntimeError('ax down 2')):
                with self.assertRaisesRegex(RuntimeError, 'import hung'):
                    P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertRegex(os.listdir(L.proj_dir)[0], r'\.failed-')

    def test_empty_mixer_read_fails_closed(self):
        with _Logic(windows=[], strips=[(), ()]) as L:
            tpl, mid = _fixture(L)
            with self.assertRaisesRegex(P.TemplateError, 'mixer read'):
                P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            self.assertNotIn('import_into_project', L.names())

    def test_end_bar_forwarded_to_bounce(self):
        with _Logic(windows=[], strips=[('A1', 'B1', 'C1', 'D1'), ('A1', 'B1', 'C1', 'D1')]) as L:
            tpl, mid = _fixture(L)
            P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            call = [c for c in L.calls if c[0] == 'bounce_and_post'][0]
            self.assertEqual(call[2].get('end_bar'), 3)

    def test_failure_after_copy_cleans_up_and_keeps_failed_copy(self):
        with _Logic(windows=[], open_raises=RuntimeError('open failed')) as L:
            tpl, mid = _fixture(L)
            before = P.tree_hash(tpl)
            with self.assertRaises(RuntimeError):
                P.produce('s', 'T', 'v', mid, template=tpl, log=lambda *_: None)
            left = os.listdir(L.proj_dir)
            self.assertEqual(len(left), 1)
            self.assertRegex(left[0], r'^T v\.failed-\d{8}-\d{6}\.logicx$')
            close = [c for c in L.calls if c[0] == 'close_all_projects']
            self.assertEqual(len(close), 1)
            self.assertEqual(close[0][2].get('save', close[0][1][0] if close[0][1] else None), False)
            self.assertEqual(P.tree_hash(tpl), before)

    def test_legacy_finish_default_window_title(self):
        import inspect
        sig = inspect.signature(P.finish)
        self.assertEqual(sig.parameters['win_title'].default, '무제 - 트랙')


if __name__ == '__main__':
    unittest.main()
