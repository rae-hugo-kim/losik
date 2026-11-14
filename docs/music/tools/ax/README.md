# ax/ — Logic 조작 보조 도구

- `cgevent.js` — CGEvent 마우스 클릭·우클릭·이동(JXA). System Events 의 `click`/`keystroke` 가 닿지 않는 원격 열기 패널(`com.apple.appkit.xpc.openAndSavePanelService`)과 컨텍스트 메뉴에 쓴다.
- `ocr.swift` — Vision 텍스트 인식. 화면 캡처에서 텍스트와 위치(화면 포인트)를 돌려준다. 컨텍스트 메뉴·열기 패널처럼 AX 트리에 없는 UI 를 텍스트로 찾아 클릭하기 위한 것이다.
  - 빌드: `swiftc -O -o docs/music/tools/ax/ocr docs/music/tools/ax/ocr.swift` (바이너리는 커밋하지 않는다; `pipeline.ensure_ocr()` 가 없으면 빌드한다)
  - 사용: `ocr <png> <scale>` → 줄마다 `x,y,w,h<TAB>text` (scale = 픽셀/포인트, Retina 2)

2026-11-13 실측(seed 20261113-220009-a606 AC0): 열기 패널의 파일 목록과 트랙 헤더 컨텍스트 메뉴는 AX 로 보이지 않고 System Events `click at` 도 받지 않지만, CGEvent 는 받는다.
