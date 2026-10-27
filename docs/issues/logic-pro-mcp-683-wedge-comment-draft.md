# Comment posted to `MongLong0214/logic-pro-mcp#683` (wedge re-test after #759)

Status: posted 2026-09-05 as issue comment 5543875069
(https://github.com/MongLong0214/logic-pro-mcp/issues/683#issuecomment-5543875069). Korean record of
the same run: [`logic-pro-mcp-683-wedge-retest.md`](logic-pro-mcp-683-wedge-retest.md).

---

Here is the re-test you asked for, and the second of the two things I said I would post unprompted.
The short version: **with a real Mackie Control surface bound, the wedge did not reproduce on either
v3.14.0 or `main` with #759.** So I cannot separate the crash from the deadlock on this host, because
there is no deadlock to separate.

## Setup

Same machine as before (macOS 26.5.2, M4), Logic Pro Creator Studio 12.3.1, server pinned with
`LOGIC_PRO_BUNDLE_ID=com.apple.mobilelogic`, `LOG_LEVEL=debug`, stderr to a file.

The confound from my last comment is controlled this time. One instance of the other fork was still
running (another session keeps it alive as its MCP server), but it publishes `LogicProMCP-In/Out`, not
`LogicProMCP-MCU-Internal`, so Logic could only bind to your server's port; and the runner samples its
own child pid rather than `pgrep -x LogicProMCP`, so a sample — had one been needed — would have been
unambiguous.

The surface was bound by hand in the GUI: Control Surfaces → Setup → New → Install → Mackie Control,
Out Port and Input both set to `LogicProMCP-MCU-Internal`, with your v3.14.0 binary running so the
port was visible. No `CoreMidi에서 오류` modal appeared.

Two binaries:

| label | binary |
|---|---|
| before | v3.14.0 release tarball — the binary from the original report |
| after | `main` @ `8d3730c`, built 09-03, carrying #759 |

## Procedure

Each trial is a fresh server process driven over stdio with the original repro sequence: `initialize`
→ `notifications/initialized` → settle → `tools/list` with a 60-second budget. On no reply it would
have taken `sample <pid> 5` and checked `pgrep -x MIDIServer`; that branch never ran. After a reply it
calls `logic_system { command: "health" }` and reads `mcu.connected`, `registered_as_device` and
`last_feedback_at`, so each row below states whether Logic was actually talking to that process
rather than assuming it from the Setup window.

The settle step exists because the first attempt finished in about one second and the health probe
would have shown nothing bound; the surface needs a moment to reattach to a freshly created port. I
only count trials where health confirmed the connection.

## Results

| trial | binary | MCU per health | `initialize` | `tools/list` |
|---|---|---|---|---|
| 1 | v3.14.0 | connected, registered as device, feedback at 16:34:42Z | 0.076s | 0.022s |
| 2 | `main` @ 8d3730c | connected, registered as device, feedback at 16:35:12Z | 0.116s | 0.025s |
| 3 | v3.14.0 | connected, registered as device | 0.046s | 0.021s |

Six further trials (three per binary, back-to-back) also answered every request in under 0.03s, but
by then health reported `connected: false`, so they are not evidence about the surface-bound case and I
am not counting them. No trial hit the 60-second budget; no sample was taken because nothing was
wedged.

One incidental observation from those later trials, in case it is useful: after the server process had
been restarted a few times in a row, Logic stopped reattaching to the new `LogicProMCP-MCU-Internal`
even though the Setup window still showed the port name. I did not investigate; the virtual endpoint's
uid changes per process, so it may simply be reattach latency. It does not bear on this issue.

## Where that leaves the report

Your last table row — *"MCU-preferred routing awaits an echo Creator Studio never sends"* — was the
one I could not test without a real surface. It is now tested in the only way that matters for this
issue: with Creator Studio bound and answering the Device Query, `tools/list` still returns
immediately on the reported binary. Whatever happened on 08-24, it is not reproducible here with the
surface bound, on either side of #759.

Combined with the process-name confound and the crash-report attribution from my previous comment, I
think the right disposition is to close this as **not reproducible as reported**. #759 stands on its
own measurements and does not need this issue to justify it. If a wedge recurs on a clean
single-install host I will open a new issue with the sample attached from the start.

Thank you for taking the original report seriously despite the noise I brought with it.

## Artifacts

Per-trial stderr for all eleven runs and the results JSON are kept locally and can be pasted on
request; they are a few KB each and contain nothing beyond the startup/shutdown log you have already
seen.
