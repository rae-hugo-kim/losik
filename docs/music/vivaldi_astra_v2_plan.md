# Astra의 사계 v2 독립 편곡 계획입니다.

- 작곡 모델은 **openai-codex/gpt-6-astra**입니다. 지정 모델과 세션 모델이 일치합니다.
- 계획 근거는 `VIVALDI_BRIEF_V2.md`, `tools/vivaldi_data.py`, `PROMPT_GUIDELINES.md` §4, `LOGIC_LIBRARY_INVENTORY.md` §4·§4.1·§5·§6입니다. 이 절이 참조하는 `logic_library_inventory.json`으로 아래 B·C 파일 이름을 확인했습니다.
- 병합 충돌 해소에 필요한 FEEDBACK_LOG의 경계와 중복 여부만 확인했습니다. 과거 라운드의 장르·편성은 이 계획의 근거가 아닙니다. 이전 작곡기를 열지 않고, 병합 커밋 `ff42e8b` 뒤 지정된 `vivaldi_astra.py --check`만 실행해 MIDI 12개 불변을 확인했습니다.
- 배제 장르는 없습니다. 표제·원전 박자·선율의 발음과 쉼을 출발점으로 정했으며, 아래 계획을 먼저 커밋한 뒤 구현합니다.

## 악장별 장르와 형식을 정합니다.

BPM은 MIDI 4분음표 기준입니다. 예상 길이는 `마디 × 분자 × 4/분모 × 60/BPM`으로 계산합니다. 트랙 번호는 콘덕터를 제외한 SMF 악기 트랙 순서이며, `patches`의 1-based 번호와 같습니다.

| key / sid | 장르 | 악장 성격에서 나온 선택 이유 | 박자 | BPM | 마디 | 예상 길이 | 원전 주제 |
|---|---|---|---|---:|---:|---:|---|
| spring 1 / vs-spring1-astra | baroque chamber pop | 밝은 리토르넬로의 반복음과 새의 짧은 몸짓을 하프시코드 어택·오보에 선율·피치카토 응답으로 분리합니다. | 4/4 | 88 | 64 | 174.55초 | solo 1–13 |
| spring 2 / vs-spring2-astra | impressionist chamber nocturne | 잠든 목동의 느린 하강선과 3박 호흡을 잉글리시 호른·피아노·하프의 부드러운 시차로 펼칩니다. | 3/4 | 66 | 64 | 174.55초 | solo 2–10 |
| spring 3 / vs-spring3-astra | Celtic folk jig | 시칠리아나의 복합박 춤을 6/8의 두 큰 박으로 묶고 휘슬·스틸 기타·켈틱 하프의 발현과 관악을 대조합니다. | 6/8 | 96 | 96 | 180.00초 | solo 1–12 |
| summer 1 / vs-summer1-astra | desert trip-hop | 뜨거운 공기의 느슨한 한숨과 짧게 끊기는 음형을 우드의 건조한 어택·묵직한 하프타임 비트·발현 응답으로 바꿉니다. | 4/4 | 62 | 48 | 185.81초 | solo 1–30 |
| summer 2 / vs-summer2-astra | chamber suspense score | 긴 독주음 사이의 천둥 같은 끊김을 5/4의 3+2 비대칭으로 만들고 바순·트레몰로 현·팀파니로 긴장을 조절합니다. | 5/4 | 80 | 48 | 180.00초 | solo 1–8 |
| summer 3 / vs-summer3-astra | progressive rock | 폭풍 프레스토의 몰아치는 반복과 하행 런을 7/8의 2+2+3 악센트, 디스토션 기타·오르간·피크 베이스로 밀어갑니다. | 7/8 | 126 | 112 | 186.67초 | solo 1–20 |
| autumn 1 / vs-autumn1-astra | New Orleans second-line jazz | 수확 축제의 반복 춤과 들뜬 강세를 클라리넷·업라이트·업라이트 피아노·트롬본 응답과 행진형 싱코페이션으로 만듭니다. | 4/4 | 100 | 72 | 172.80초 | solo 1–12 |
| autumn 2 / vs-autumn2-astra | chamber passacaglia | 술 취한 잠의 거의 정지된 화음과 반음 움직임을 독주 바이올린의 긴 호흡, 새로 쓴 저음 반복, 하프시코드 내성으로 풀어냅니다. | 3/4 | 64 | 64 | 180.00초 | violin1 4–14 |
| autumn 3 / vs-autumn3-astra | cinematic hunting scherzo | 사냥의 호출 도약을 호른이 맡고, 6/8 스타카토 현과 팀파니의 큰 박으로 추격감을 만듭니다. | 6/8 | 100 | 96 | 172.80초 | solo 1–24 |
| winter 1 / vs-winter1-astra | industrial breakbeat | 떨리는 반복음을 짧은 Sync Lead와 첼레스타의 차가운 어택으로 나누고 불규칙한 킥·스네어와 입자성 신스로 추위를 표현합니다. | 4/4 | 112 | 80 | 171.43초 | solo 4–12 |
| winter 2 / vs-winter2-astra | acoustic bossa nova | 실내에서 듣는 비의 피치카토 반주와 노래하는 선율을 나일론 기타의 엇박·플루트의 긴 선율·비브라폰의 작은 물방울로 만듭니다. | 4/4 | 90 | 64 | 170.67초 | solo 1–8 |
| winter 3 / vs-winter3-astra | contemporary minimalist chamber | 얼음 위에서 맴도는 회전음을 5/8의 3+2로 다시 묶고 피치카토 독주 바이올린·마림바·하프의 서로 다른 주기로 움직입니다. | 5/8 | 92 | 112 | 182.61초 | solo 1–24 |

Winter I는 데이터상 solo가 처음 세 마디 쉬므로 창을 4–12로 정했습니다. Spring I의 피크업은 첫 주제 앞의 전주 마지막 박에 옮겨 음수 틱 없이 살립니다. Autumn II는 브리프가 지정한 violin1을 사용합니다. 나머지는 기본 창을 유지합니다.

## 트랙별 경로와 정확한 이름을 고정합니다.

경로 A는 측정된 PC의 실제 소리를 선택합니다. B·C 트랙의 SMF PC는 0을 초기값으로 두고 반드시 `produce(..., patches=...)`로 아래 이름을 올립니다. C의 바탕 패치 `Violins 1`은 Sampler를 사용하는 `z_Legacy/Orchestral/Strings/Violins 1.patch`입니다. B·C 로드가 실패하면 GM 소리로 조용히 대체하지 않습니다.

| key | 트랙별 편성 및 경로 |
|---|---|
| spring 1 | 1 Rhythm: A PC0 SoCal(ch10); 2 Bass: A PC43 Studio Double Basses; 3 Harmony: B `Harpsichord`; 4 Lead: B `Oboe`; 5 Texture: C (`Violins 1`, `Violins 1 Pizzicato`) |
| spring 2 | 1 Bass: A PC42 Studio Cellos; 2 Harmony: A PC2 Concert Grand; 3 Lead: B `English Horn`; 4 Texture: B `Harp` |
| spring 3 | 1 Rhythm: A PC26 Roots(ch10); 2 Bass: A PC32 Roots Upright; 3 Harmony: A PC25 Acoustic Guitar; 4 Lead: B `Celtic Tin Whistle`; 5 Texture: B `Celtic Harp` |
| summer 1 | 1 Rhythm: A PC24 Drum Synth Kit(ch10); 2 Bass: A PC39 Taureg Moon Bass; 3 Harmony: A PC7 70s Funk Clav; 4 Lead: B `Turkish Oud Lute`; 5 Texture: A PC107 Koto |
| summer 2 | 1 Pulse: B `Timpani`(유음 타악, ch10 아님); 2 Bass: A PC42 Studio Cellos; 3 Harmony: A PC12 Marimba; 4 Lead: B `Bassoon Solo`; 5 Texture: C (`Violins 1`, `Violins 1 Tremolo`) |
| summer 3 | 1 Rhythm: A PC8 Retro Rock(ch10); 2 Bass: A PC34 Punchy Bottom; 3 Harmony: A PC18 Classic Rock Organ; 4 Lead: A PC30 Hard Rock; 5 Texture: A PC48 Kensington |
| autumn 1 | 1 Rhythm: A PC0 SoCal(ch10); 2 Bass: A PC32 Roots Upright; 3 Harmony: A PC1 Vintage Upright; 4 Lead: B `Clarinet Solo`; 5 Texture: A PC57 Studio Trombone 1 |
| autumn 2 | 1 Bass: A PC42 Studio Cellos; 2 Harmony: B `Harpsichord`; 3 Lead: C (`Violins 1`, `Violin (Arco)`); 4 Texture: B `Bassoon Solo` |
| autumn 3 | 1 Pulse: B `Timpani`(유음 타악); 2 Bass: A PC43 Studio Double Basses; 3 Harmony: C (`Violins 1`, `Violins 1 Staccato`); 4 Lead: B `French Horn Solo`; 5 Texture: A PC48 Kensington |
| winter 1 | 1 Rhythm: A PC16 Tough Kit(ch10); 2 Bass: A PC39 Taureg Moon Bass; 3 Harmony: A PC8 Toy Celesta; 4 Lead: A PC82 Sync Lead; 5 Texture: A PC98 Glacial Forms |
| winter 2 | 1 Rhythm: A PC40 Latin(ch10); 2 Bass: A PC32 Roots Upright; 3 Harmony: A PC24 Classical Acoustic Guitar; 4 Lead: B `Flute Solo`; 5 Texture: A PC11 Vibraphone |
| winter 3 | 1 Bass: A PC42 Studio Cellos; 2 Harmony: A PC12 Marimba; 3 Lead: C (`Violins 1`, `Violin (Pizzicato)`); 4 Texture: B `Harp` |

금관·목관·발현의 음역은 악기 성격에 맞춰 주제 전체를 동일 옥타브 단위로 이동합니다. 특히 바순은 원전 바이올린보다 낮게, 오보에·휘슬은 중고역으로 배치합니다. 원전 각 음을 따로 옥타브 접기하지 않아 음정 윤곽을 보존합니다. 합주 현은 원전 성부를 복사하지 않고 새 화음·리듬만 연주합니다.

## 구현과 검증 기준을 정합니다.

- 구조는 전주 8마디, 주제 A `N/4`마디, 자작 전개·간주 `N/2−16`마디, 주제 B `N/4`마디, 후주 8마디를 기준으로 합니다. 주제 구간은 정확히 50%이며 쉼표를 포함한 섹션 길이 비율입니다. 실제 주제 발음 마디 수도 별도로 기록합니다.
- 원전 주제 창 전체를 주제 A의 길이에 맞춰 재구성하고 B에서 표현·반주·레지스터를 바꿉니다. 창의 앞부분만 기계적으로 반복하다 구간 끝에서 잘라내지 않습니다. 자작 전개에는 악장마다 직접 정한 짧은 모티프를 사용합니다.
- 부분 당김과 음가 2배/절반을 기본 변형으로 삼고, 빠른 악장은 런 솎기, 춤·행진 계열은 박 분할 변경을 추가합니다. 원리듬 최장 연속 마디는 같은 박자 기준의 원전 onset 패턴과 비교하고 미세 휴머나이즈는 비교에서 제외합니다.
- 한 성부만 차용하고 원전 베이스·모방 성부는 쓰지 않습니다. 새 저음·보이싱·내성·응답을 만들고, 각 장르의 구체적인 리듬 패턴을 다르게 구현합니다. 인트로·아웃트로 밖에서 한 층만 발음하는 마디의 연속 길이는 최대 2마디로 검사합니다.
- 점검 줄에 트랙별 벨로시티 범위·음/마디, 구간별 음/마디, 베이스 음/마디, 원리듬 최장 연속, 주제 비율, 단층 구간 최장 연속, 마지막 노트 위치를 출력합니다. MIDI에는 Mutopia Project·CC BY-SA 3.0을 텍스트 또는 저작권 메타 이벤트로 넣습니다.
- v1 파일은 수정하지 않습니다. `--check`는 v2도 파일을 쓰지 않고 재생성 바이트와 비교합니다. 박자·템포·마커는 SMF를 다시 파싱해 확인하고, 오디오 길이는 각 박자에 맞춘 기대값과 대조합니다.
- 잠금은 `produce()`에 맡기고 다른 워크트리 파일을 변경하지 않습니다. 바운스 실패는 반환값과 함께 기록하며 `stage='patches'`는 정확한 이름·Sampler 바탕 패치를 인벤토리에서 확인한 뒤 재시도합니다. `TimeoutError`는 대기 초과로 기록하고 다음 곡을 먼저 진행한 뒤 미완료 곡을 다시 처리합니다.
- Suno Style ≤300자, Description ≤1,000자를 측정합니다. 업로드 결과는 사용자 확인 전 미확인입니다. 반려가 오면 브리프 §2-7의 템포 메타 ±2 BPM(`v2u`)·드럼 제외 +1반음(`v2t`) 시험 순서를 따릅니다.

## 자율 결정과 이유를 기록합니다.

1. 별도 장르 선호를 묻지 않고 12악장의 표제·박자·질감에서 서로 다른 12개 편곡 방향을 정했습니다. 계획 전 읽기 제한을 지키기 위한 결정입니다.
2. 악기 비교를 위해 B와 C를 모두 사용하되, 모든 트랙을 이름 로드로 바꾸지는 않습니다. 필요한 목관·하프시코드·하프·팀파니·현악 주법만 이름으로 올리고 나머지는 실제 소리가 확인된 PC를 사용합니다.
3. 솔로 바이올린의 최종 음색 채택은 이번 자동 제작과 구분합니다. 설치된 EXS의 지속음·피치카토 범위에서 작곡하고, 전용 레가토가 있는 것처럼 표기하지 않습니다.
4. 계획 이후 실제 변경은 아래에 날짜·결정·이유·검증을 추가합니다. 계획 커밋의 표를 조용히 바꾸지 않습니다.
