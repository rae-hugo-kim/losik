// music-render.test.mjs — docs/music/tools 의 작곡 스크립트가 docs/music/sketches/*.mid 를
// 바이트 동일하게 재생성하는지 검증한다 (PROMPT_GUIDELINES §6: MIDI 원천은 리포, 코드가 단일 진실).
// 각 스크립트는 내부 자기검증(온음계·충돌·코드톤 assert)을 갖고 있어, 실행 성공 자체가 그 검사의 통과다.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const TOOLS = 'docs/music/tools';
const SKETCHES = 'docs/music/sketches';
const md5 = (p) => createHash('md5').update(readFileSync(p)).digest('hex');

// 스크립트가 SK_DIR(리포 sketches/)에 직접 쓰므로, 실행 전 현재 파일의 해시를 찍고 실행 후 비교한다.
// 실패 시에도 리포 파일은 스크립트의 결정론적 출력으로 덮여 있으므로 git diff 로 차이를 볼 수 있다.
const CASES = [
  ['firstlight.py', ['v1'], ['first-light.mid']],
  ['firstlight.py', ['v2'], ['first-light-v2.mid']],
  ['firstlight_v3.py', [], ['first-light-v3.mid']],
  ['dawnset.py', [], ['morning-glass.mid', 'blue-hour.mid', 'paper-kite.mid', 'long-bridge.mid']],
  ['ostinato.py', [], readdirSync(SKETCHES).filter((f) => f.startsWith('ostinato-'))],
];

for (const [script, args, outputs] of CASES) {
  test(`${script} ${args.join(' ')} regenerates ${outputs.join(', ')} byte-identically`, () => {
    const before = Object.fromEntries(outputs.map((f) => [f, md5(join(SKETCHES, f))]));
    execFileSync('python3', [script, ...args], { cwd: TOOLS, stdio: 'pipe' });
    for (const f of outputs) {
      assert.equal(md5(join(SKETCHES, f)), before[f], `${f} drifted from committed version`);
    }
  });
}
