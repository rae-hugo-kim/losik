// music-render.test.mjs — docs/music/tools 의 작곡 스크립트가 docs/music/sketches/*.mid 를
// 바이트 동일하게 재생성하는지 검증한다 (PROMPT_GUIDELINES §6: MIDI 원천은 리포, 코드가 단일 진실).
// 각 스크립트는 내부 자기검증(온음계·충돌·코드톤 assert)을 갖고 있어, 실행 성공 자체가 그 검사의 통과다.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const TOOLS = 'docs/music/tools';
const SKETCHES = 'docs/music/sketches';
const md5 = (p) => createHash('md5').update(readFileSync(p)).digest('hex');

// 스크립트는 SK_DIR(리포 sketches/)에 직접 쓴다. 실행 전 바이트를 잡아두고, 실행 후 비교한 다음 원본을 복원한다 —
// 회귀가 나도 워크트리에 새 출력이 남지 않으므로(리뷰 지적) 다음 실행에서 조용히 통과되지 않는다.
const ostinatoOutputs = () => {
  const src = readFileSync(join(TOOLS, 'ostinato.py'), 'utf8');
  const names = [...src.matchAll(/^\s*'([A-Z]-[a-z-]+)':|^CANDIDATES\['([A-Z]-[a-z-]+)'\]/gm)].map((m) => m[1] ?? m[2]);
  assert.ok(names.length >= 2, 'could not enumerate CANDIDATES from ostinato.py');
  return names.map((n) => `ostinato-${n}.mid`);
};

const CASES = [
  ['firstlight.py', ['v1'], ['first-light.mid']],
  ['firstlight.py', ['v2'], ['first-light-v2.mid']],
  ['firstlight_v3.py', [], ['first-light-v3.mid']],
  ['dawnset.py', [], ['morning-glass.mid', 'blue-hour.mid', 'paper-kite.mid', 'long-bridge.mid']],
  ['ostinato.py', [], ostinatoOutputs()],
];

for (const [script, args, outputs] of CASES) {
  test(`${script} ${args.join(' ')} regenerates ${outputs.join(', ')} byte-identically`, () => {
    const paths = outputs.map((f) => join(SKETCHES, f));
    const committed = paths.map((p) => readFileSync(p));
    const mtimeBefore = paths.map((p) => statSync(p).mtimeMs);
    try {
      execFileSync('python3', [script, ...args], { cwd: TOOLS, stdio: 'pipe' });
      paths.forEach((p, i) => {
        assert.notEqual(statSync(p).mtimeMs, mtimeBefore[i], `${outputs[i]} was not written by ${script}`);
        assert.equal(md5(p), createHash('md5').update(committed[i]).digest('hex'), `${outputs[i]} drifted from committed version`);
      });
    } finally {
      paths.forEach((p, i) => writeFileSync(p, committed[i]));
    }
  });
}
