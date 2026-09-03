# DRAFT — comment for `MongLong0214/logic-pro-mcp#683` (revised after adversarial review)

---

Thank you for the four comments. Correcting your own best hypothesis by measuring it, and telling me
not to spend time on it first, is what made the rest of this tractable. I did not run
`Scripts/test_mcu_feedback_jsonrpc_liveness.py`, per your warning, and nothing below uses a
`MIDIThruConnection`.

Before any of my data: my original report was environmentally confounded, and one of the claims in it
was wrong. That comes first, because it probably explains why you could not reproduce anything.

## My report was made on a machine running three different logic-pro-mcp implementations

Installed here: your v3.14.0 release tarball at `~/.local/opt/logic-pro-mcp`, a Swift fork
(`bigkrys/logic-pro-mcp-creator`) whose two instances were running as live MCP clients throughout,
and `rubenknol/logic-pro-mcp` (Node). All three produce a process named `LogicProMCP`, so the command
you asked me to run three times is ambiguous on this host:

```
$ pgrep -x LogicProMCP
91782
9842
```

Both of those are the other fork. `sample $(pgrep -x LogicProMCP) 5 -file …` expands to two PIDs and
misparses, so no sample I could have taken then was reliably a sample of your process.

The crash reports on this machine tell the same story. Matching binary UUIDs (`dwarfdump --uuid`
against each install, then the `usedImages` array in each `.ips`), the current inventory is 14 reports
belonging to the other fork, all faulting in its own `MIDIFeedback.parse(packetList:)`, and 4
belonging to your v3.14.0 — every one of which I produced today with the repro in the last section.
Your binary has no crash on this machine that I did not cause deliberately.

I also have to withdraw something I was about to send you. I had read Logic's control-surface
preference file and concluded the Mackie surface was bound through an IAC bridge to the other fork's
ports. That inference was wrong. `Mackie Control C4 …` and `Logic Control` turn out to be shipped
vocabulary, present inside the Logic application bundle whether or not any device is configured, and
the port names in that file read as a cached enumeration of available endpoints rather than an
assignment — `LogicProMCP-In` and `LogicProMCP-Out` each appear twice, matching the two concurrently
running instances of the other fork. What survives is only the narrow part: `LogicProMCP-MCU-Internal`
does not appear in that file at all.

Worse for the report, the precondition of my own repro step 1 is not present. Checked in the GUI
today: Control Surfaces → Setup contains no Mackie Control device. I cannot reconstruct what was bound
on 08-24, and I cannot assert that the process which stopped answering was yours. **If you close this
as not-reproducible-as-reported, that is the correct disposition.** I will re-file from a clean
single-install environment if it recurs there.

There is a second, smaller retraction: the repeated device-ID queries (`0x10/0x11/0x15/0x17`) I
highlighted originally are not evidence of anything, because that capture was taken with a bare
virtual destination and no server running, so no reply was possible by construction.

## The tests you asked for

Everything below ran against your v3.14.0 tarball (arm64 UUID `93583E13-EF9A-3AC1-A515-ECA3F3A2224C`)
on macOS 26.5.2 (M4), with `LOGIC_PRO_BUNDLE_ID=com.apple.mobilelogic` and `LOG_LEVEL=debug`. Logic
Pro Creator Studio was installed and running, but no control surface was bound at any point, which
limits what these results can mean — see the caveat in the routing section.

### The wedged `sample` — not delivered, and here is why

I cannot give you a sample of a wedged process. Per the section above, the surface binding my repro
depended on no longer exists on this machine, so this is not a matter of waiting for a free moment:
the binding has to be re-created from scratch, on a host where your server is the only install, so the
port and the PID are unambiguous. Until that is true, a sample is not evidence about your code.

What I can give you is the same artifact from your binary under the traffic shape from the report,
which at least answers "is the loop blocked?" positively rather than by absence:

```
$ sample 17224 5 -file /tmp/sample-under-mcu-flood.txt   # during a 40-packet-per-list MCU flood

4146 Thread_38766993   DispatchQueue_1: com.apple.main-thread  (serial)
+ 4146 swift_task_asyncMainDrainQueue  (in libswift_Concurrency.dylib) + 92
+   4146 swift_task_asyncMainDrainQueueImpl  + 140
+     4146 protocol witness for RunLoopExecutor.run() in conformance DispatchMainExecutor + 40
+       4146 CFMainExecutor.run()  + 48
...
+ 4077 MIDIProcess::MIDIInPortThread::Run()  (in CoreMIDI) + 148
+   : 57 closure #3 in MCUChannel.start()  (in LogicProMCP) + 144
+   : 3  specialized static MIDIFeedback.parseBytes(_:)  (in LogicProMCP) + 1548
```

The main thread is parked in `CFMainExecutor.run()` — an idle run loop, not a blocked write, not a
lock, not an actor wait — while MCU ingress works. In the same run `tools/list` answered before,
during, and after the flood.

### stderr as a file, and then as a pipe that is never read

With stderr to a file, `initialize` returned in 0.7s and `tools/list` in 0.0s. On its own that says
little, because no surface was bound, so I tested the pipe condition directly instead — that is the
half of your hypothesis that lives on the client side, where you could not reach it.

I gave the server stderr as a pipe and never read it, then drove `tools/list` in a loop. It answered
**7,000 consecutive requests** without wedging, and draining the pipe afterwards found 2,472 bytes
sitting in it. Your own figure was 2,467 bytes for 198 requests. Those two numbers being nearly equal
across a 35-fold difference in request count is the finding: the volume is startup logging, and
protocol-local requests contribute essentially nothing. A 64 KB pipe is never approached, so an
undrained stderr pipe cannot be filled by request traffic on this build. I would treat that
hypothesis as closed rather than merely weakened. (Evidence: `stderr-pipe.log`.)

### What the log says last before a fault

For the crash I did reproduce, the final lines are routine, with no error or warning:

```
[DEBUG] [midi] MIDIPortManager notification: 2 (MIDIPortManager.swift:35)
[DEBUG] [midi] MIDI object added (MIDIEngine.swift:267)
[DEBUG] [cache] stale write refused for tracks: observed (epoch 0, rev 12) vs current (epoch 0, rev 18)
```

A memory fault on a CoreMIDI delivery thread leaves nothing behind, which is consistent with both the
silence you asked about and with the absence of a timeout envelope.

### MIDIServer

```
$ ls -t ~/Library/Logs/DiagnosticReports | grep -i midi     # LogicProMCP only; zero MIDIServer reports
$ pgrep -x MIDIServer
13201                                                        # alive throughout, including right after a server death
```

MIDIServer has never crashed on this machine, so the mechanism from your 02:04 comment is real but is
not what this host experienced. Consistent with my never having used Thru.

## Your last open row: what I can and cannot say

Your table still lists *"MCU-preferred routing awaits an echo Creator Studio never sends"* as
untested. I tried to test it by reproducing its observable shape — no feedback returning on the MCU
port — and the result is informative but **narrower than a refutation**, so I want to state it
precisely rather than claim your row.

Three runs, each a fresh server, each calling `logic_transport { command: "play" }`. With feedback
present (flooding the MCU destination) the router logged `transport.play succeeded via MCU` and
returned in 1.5s. With no feedback at all, and again with a peer that consumed every command and
replied to none, the router logged this instead:

```
[DEBUG] [router] Channel MCU unhealthy: MCU feedback not detected. Register 'LogicProMCP-MCU-Internal'
                 in Logic Pro > Control Surfaces > Setup, trying next (ChannelRouter.swift:168)
```

and fell through to another channel, returning a `readback_unavailable` envelope in about 2s.

So on the transport path a missing feedback stream is health-gated, not awaited: your router declines
MCU and moves on, which is the behaviour you would want. What this does **not** establish is that no
code path awaits an echo, because the health gate meant that path was never entered, and because no
real Creator Studio surface was bound — the exact condition your hypothesis is about. Your row should
stay open; I can only report that the transport fallback is sound and that I could not produce an
unbounded wait this way.

The same measurement disposes of a hypothesis of my own that I would otherwise have handed you: that I
had the surface's input and output ports assigned backwards. It is a real hazard in principle, since
this machine has IAC loopback buses (`MCU Cmd`, `MCU Fb`) and a loopback bus appears as both a source
and a destination, so Logic's pickers cannot filter a wrong choice out of either list. But a feedback
path that returns nothing still produced an envelope in about 2s rather than silence, and there is no
Mackie device configured now for the assignment to exist in. Not worth your time on this issue.

## One real defect in v3.14.0: legacy `MIDIPacketList` ingress on multi-packet lists

This is not the reported wedge. It is a separate, reproducible memory-safety fault I hit while
unwinding the environment problem above.

`LogicProMCP-MIDI-In` is a virtual destination your server creates at startup. Sending it
`MIDIPacketList`s that contain many packets each kills the server. Three trials today, each a fresh
server given `initialize` and `notifications/initialized` first, then flooded with 3,870 packets in
40-packet lists: two died with `SIGBUS`, one survived. Four crash reports now exist for your binary
across today's runs, all with the same faulting stack, and the legacy thunk is the giveaway:

```
LogicProMCP  closure #1 in closure #1 in closure #3 in variable initialization expression of …
LogicProMCP  thunk for @escaping @callee_guaranteed (@unowned UnsafePointer<MIDIPacketList>, …)
CoreMIDI     MIDI::PacketizerBase<MIDI::LegacyPacketList>::~PacketizerBase()
CoreMIDI     MIDI::MIDIPacketList_Deliverer::operator()(MIDI::EventList const*)
CoreMIDI     MIDIProcess::MIDIInPortThread::Run()
```

Your MCU port is not affected. The same sender aimed at `LogicProMCP-MCU-Internal` — created at
`LogicProServer.swift:1445` through `portManager.createBidirectionalPort`, the `MIDIEventList` path you
hardened on 08-31 — delivered 5,167 packets in 40-packet lists with `tools/list` answering in 0.0s
before, during and after, and no crash. The defect is on the other path.

### Cause

`MIDIEngine.swift:47-61` on `main` @ `434267f`:

```swift
let status = MIDIDestinationCreateWithBlock(client, name as CFString, &destination) { packetList, _ in
    let packets = packetList.pointee
    var list = packets                                  // value copy of a VARIABLE-LENGTH struct
    withUnsafePointer(to: &list.packet) { firstPacket in
        var packet = firstPacket
        for _ in 0..<list.numPackets {                  // count read from the copy
            let current = packet.pointee
            let length = Int(current.length)
            let bytes = withUnsafeBytes(of: current.data) { raw in
                Array(raw.prefix(length).bindMemory(to: UInt8.self))
            }
            onBytes(bytes)
            packet = UnsafePointer(MIDIPacketNext(packet))   // advances past the end of the copy
        }
    }
}
```

A `MIDIPacketList` is a header followed by a run of variable-length `MIDIPacket`s packed tightly, each
occupying a timestamp, a length, and exactly `length` bytes. The Swift-imported `MIDIPacket` declares
its `data` as a fixed 256-byte array, so `var list = packets` copies the packet count from the
original but only about 266 bytes of packet storage. That copied window is not empty of later packets —
because the original is packed tightly, the window happens to contain the first several packets
verbatim, which is exactly why short lists parse correctly and survive. The failure begins when the
walk crosses the end of the window: from there `length` is itself read from whatever follows on the
stack, so the next `MIDIPacketNext` advances an arbitrary distance and the traversal degenerates
quickly.

That mechanism also predicts the shape of the measurements below. The traffic mix used here averages
about 19 bytes per packed packet, so a 266-byte window covers roughly the first fourteen packets;
observed behaviour is survival at 20 packets per list and under, and deterministic death at 24 and
above, which is what "leaves the window, then leaves mapped stack a little later" looks like. The
exact threshold is a property of the stack frame, not of the protocol.

It is the shape you described on 08-31 — the read is clamped, the advance is not — still present on the
legacy `MIDIDestinationCreateWithBlock` path.

`MIDIFeedback.parse(packetList:into:)` at `MIDIFeedback.swift:20` is identical, and a whole-tree grep
finds its only caller in `Tests/LogicProMCPTests/MIDIFeedbackTests.swift:186`, so the test that covers
it shares the defect and passes anyway.

### Isolated, and a fix that holds

Because the in-server fault is intermittent, I lifted the traversal out verbatim into a standalone
harness that creates its own virtual destination and floods itself, with no Logic, no MCP client and
no Thru involved. `buggy` is byte-for-byte the closure above; `fixed` traverses the original list. Each
trial is its own process, so a fault appears as a signal:

| packets per list | `buggy` | `fixed` |
|---|---|---|
| 40 | died 5 of 5 | survived 8 of 8 |
| 36 / 32 / 24 | died 3 of 3 each | — |
| 20 / 16 / 8 / 2 / 1 | survived 3 of 3 each | — |

The threshold on this host sits between 20 and 24 packets per list, and above it the fault is
deterministic in isolation; the in-server two-of-three is the same bug against a different stack
layout. This is also why your harness stayed clean: driving `LogicProMCP-MCU-Internal` exercises the
EventList path, and a replay that sends one packet per list never trips the legacy one even when it
reaches it. The two variables are which port and how many packets per list.

The `fixed` variant that survived 8 of 8 while still delivering every byte:

```swift
for packet in packetList.unsafeSequence() {
    let length = min(Int(packet.pointee.length), 256)
    let bytes = withUnsafeBytes(of: packet.pointee.data) { raw in
        Array(raw.prefix(length).bindMemory(to: UInt8.self))
    }
    onBytes(bytes)
}
```

I verified that in isolation rather than in your tree, because `main` @ `434267f` does not compile
here: with a pristine checkout and only `Package.resolved` touched by dependency resolution,
`swift build -c release` fails at
`Sources/LogicProMCP/Channels/AccessibilityChannel+MIDIImport.swift:640:75` with *"the compiler is
unable to type-check this expression in reasonable time"*. My local toolchain is Swift 6.3.1 and your
CI pins Xcode 16.4 / Swift 6.2, so I read this as toolchain-specific rather than as a defect in the
repo. I re-ran it on the untouched tree specifically to confirm my patch was not the cause.

## Cumulative, in your format

| hypothesis | verdict | how |
|---|---|---|
| `StateCache` starved by the feedback flood | refuted (yours) | 1.96 µs cache read under 20k-event flood vs 16.7 µs quiet |
| lock shared between receive callback and send | refuted (yours) | destination block parses and yields; no lock, no actor hop |
| per-event MCU logging floods stderr | refuted (yours) | feedback path logs only start/stop; `Log` rate-limits |
| undrained stderr pipe fills and blocks a logging thread | closed (mine) | stderr as a never-read pipe: 7,000 requests answered, 2,472 B pending — same magnitude as your 2,467 B for 198 |
| MCU-preferred routing awaits an echo that never arrives | still open | health gate declined MCU before that path was entered; no real surface bound, so untested as you framed it |
| reversed input/output binding through the IAC bridge | not the cause | a feedback path returning nothing still answers in ~2s; and no Mackie device exists on this machine now |
| whole-loop block during MCU ingress | not observed (mine) | `sample` under 40-packet flood: main thread idle in `CFMainExecutor.run()`; `tools/list` answers during the flood |
| MIDIServer died, so nothing could answer | not this host (mine) | zero MIDIServer crash reports; `pgrep -x MIDIServer` alive throughout |
| the wedged process was v3.14.0 | cannot assert (mine) | three installs share the process name; all other crashes UUID-match the other fork; the surface my repro needed is gone |
| legacy `MIDIPacketList` traversal reads out of bounds | confirmed (mine) | 2 of 3 in-server deaths on `LogicProMCP-MIDI-In`; 5 of 5 in isolation at 40 packets/list; 0 of 8 with the fix |

## Artifacts

Held on this machine and postable: four `.ips` reports for your binary from today's runs
(`163929`, `164019`, `024420`, `024422`), the two `sample` files (idle and under flood), and logs for
each measurement above — the never-read-pipe run, the three in-server trials with their per-trial
stderr, the buggy-versus-fixed matrix, the MCU-port control flood, and the clean-build error. The three
harnesses are small enough to paste on request: `mcuflood.swift` (multi-packet sender),
`pkttest.swift` (buggy-versus-fixed traversal, usable as a regression test) and `echoswallow.swift`
(the command-consuming peer). Raw `.ips` files carry hardware identifiers, so I have quoted the
relevant fields rather than pasting them wholesale.

One correction about evidence itself: two reports I mentioned in passing earlier, an `OSCClient`
double-resume belonging to the other fork, have since been rotated off disk. I am describing those
from my own notes and cannot attach them, so they should not count toward anything here.

Two things I owe you and will post unprompted rather than wait to be asked: the wedged `sample` from a
clean single-install host with a surface actually bound, and the result of that attempt even if it
turns out the wedge does not recur — which, after everything above, is what I now expect.
