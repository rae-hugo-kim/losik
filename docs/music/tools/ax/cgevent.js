// CGEvent 마우스 헬퍼 (JXA). System Events 의 click/keystroke 가 닿지 않는 곳(원격 열기 패널, 컨텍스트 메뉴)에 쓴다.
//   osascript -l JavaScript cgevent.js click X Y [N]   왼쪽 클릭 N회
//   osascript -l JavaScript cgevent.js rclick X Y      오른쪽 클릭
//   osascript -l JavaScript cgevent.js move X Y        포인터 이동(서브메뉴 열기)
// 좌표는 화면 포인트(1080x1920 UI 기준).
ObjC.import('Cocoa');
function post(type, pt, btn, state) {
  const e = $.CGEventCreateMouseEvent(null, type, pt, btn);
  if (state) $.CGEventSetIntegerValueField(e, $.kCGMouseEventClickState, state);
  $.CGEventPost($.kCGHIDEventTap, e);
}
function run(argv) {
  const cmd = argv[0], x = parseFloat(argv[1]), y = parseFloat(argv[2]);
  const pt = $.CGPointMake(x, y);
  post($.kCGEventMouseMoved, pt, $.kCGMouseButtonLeft, 0);
  delay(0.15);
  if (cmd === 'move') return 'moved';
  if (cmd === 'rclick') {
    post($.kCGEventRightMouseDown, pt, $.kCGMouseButtonRight, 1);
    post($.kCGEventRightMouseUp, pt, $.kCGMouseButtonRight, 1);
    return 'rclicked';
  }
  const n = parseInt(argv[3] || '1');
  for (let i = 1; i <= n; i++) {
    post($.kCGEventLeftMouseDown, pt, $.kCGMouseButtonLeft, i);
    post($.kCGEventLeftMouseUp, pt, $.kCGMouseButtonLeft, i);
    delay(0.08);
  }
  return 'clicked x' + n;
}
