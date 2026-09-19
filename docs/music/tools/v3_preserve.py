"""Transplant approved MIDI sections without regenerating their performances."""
from collections import defaultdict, deque
from copy import deepcopy
import hashlib
import struct

import pipeline as p


def _vlq(data, pos):
    value = 0
    for _ in range(4):
        if pos >= len(data):
            raise ValueError('Truncated MIDI variable-length quantity')
        byte = data[pos]
        pos += 1
        value = (value << 7) | (byte & 0x7f)
        if byte < 0x80:
            return value, pos
    raise ValueError('MIDI variable-length quantity exceeds four bytes')


def _meta(tick, kind, payload):
    # pipeline.meta encodes a one-byte length; longer metadata needs a VLQ.
    if len(payload) < 128:
        return p.meta(tick, kind, payload)
    return tick, 0, bytes([0xff, kind]) + p.varlen(len(payload)) + payload


def _parse_track(data):
    pos = tick = 0
    running = None
    events, notes = [], []
    pending = defaultdict(deque)
    channels, programs = set(), {}
    while pos < len(data):
        delta, pos = _vlq(data, pos)
        tick += delta
        if pos >= len(data):
            raise ValueError('Missing MIDI event after delta time')
        status = data[pos]
        if status < 0x80:
            if running is None:
                raise ValueError('MIDI running status without channel status')
            status = running
        else:
            pos += 1
        if status == 0xff:
            running = None
            if pos >= len(data) or data[pos] >= 0x80:
                raise ValueError('Invalid MIDI metadata type')
            kind = data[pos]
            length, pos = _vlq(data, pos + 1)
            payload = data[pos:pos + length]
            if len(payload) != length:
                raise ValueError('Truncated MIDI metadata')
            pos += length
            if kind == 0x2f:
                if length or pos != len(data):
                    raise ValueError('Invalid MIDI end-of-track event')
                if any(pending.values()):
                    raise ValueError('Unmatched MIDI note-on')
                return events, notes, (channels, programs), tick
            events.append(_meta(tick, kind, payload))
            continue
        if status in (0xf0, 0xf7):
            running = None
            length, pos = _vlq(data, pos)
            payload = data[pos:pos + length]
            if len(payload) != length:
                raise ValueError('Truncated MIDI system-exclusive event')
            pos += length
            events.append((tick, 0, bytes([status]) + p.varlen(length) + payload))
            continue
        if not 0x80 <= status < 0xf0:
            raise ValueError(f'Unsupported MIDI status {status:02x}')
        running = status
        kind, channel = status & 0xf0, status & 0x0f
        size = 1 if kind in (0xc0, 0xd0) else 2
        payload = data[pos:pos + size]
        if len(payload) != size or any(byte >= 128 for byte in payload):
            raise ValueError('Invalid MIDI channel-event data')
        pos += size
        channels.add(channel)
        message = bytes([status]) + payload
        if kind == 0xc0:
            if channel in programs and programs[channel] != payload[0]:
                raise ValueError('Section preservation requires fixed MIDI programs')
            programs[channel] = payload[0]
        if kind == 0x90 and payload[1]:
            pending[channel, payload[0]].append((tick, 2, message))
        elif kind == 0x80 or (kind == 0x90 and payload[1] == 0):
            queue = pending[channel, payload[0]]
            if not queue:
                raise ValueError('Unmatched MIDI note-off')
            onset = queue.popleft()
            if tick <= onset[0]:
                raise ValueError('MIDI note duration must be positive')
            notes.append((onset, (tick, 1, message)))
        else:
            events.append((tick, 0, message))
    raise ValueError('Missing MIDI end-of-track event')


def _parse(smf):
    if len(smf) < 14 or smf[:4] != b'MThd':
        raise ValueError('Missing MIDI header')
    length, fmt, count, division = struct.unpack('>IHHH', smf[4:14])
    if length != 6 or fmt != 1 or division != p.PPQ or count < 2:
        raise ValueError('Expected format-1 MIDI with 480 PPQ and a conductor')
    pos, tracks = 14, []
    for _ in range(count):
        if pos + 8 > len(smf) or smf[pos:pos + 4] != b'MTrk':
            raise ValueError('Missing MIDI track chunk')
        length = struct.unpack('>I', smf[pos + 4:pos + 8])[0]
        pos += 8
        if pos + length > len(smf):
            raise ValueError('Truncated MIDI track chunk')
        tracks.append(_parse_track(smf[pos:pos + length]))
        pos += length
    if pos != len(smf):
        raise ValueError('Unexpected bytes after MIDI tracks')
    if tracks[0][2][0]:
        raise ValueError('Conductor must not contain channel events')
    return tracks


def _sections(manifest):
    sections = {}
    previous_end = 0
    for section in manifest['sections']:
        name = section['name']
        start = section['tick']
        numerator, denominator = section['meter']
        bars = section['bars']
        if (not isinstance(start, int) or start < previous_end or
                not isinstance(bars, int) or bars <= 0 or
                not isinstance(numerator, int) or numerator <= 0 or
                not isinstance(denominator, int) or denominator <= 0):
            raise ValueError(f'Invalid section geometry: {name}')
        length, remainder = divmod(bars * numerator * 4 * p.PPQ, denominator)
        if remainder or name in sections:
            raise ValueError(f'Invalid or duplicate section: {name}')
        sections[name] = (start, start + length)
        previous_end = start + length
    if not sections:
        raise ValueError('Manifest contains no sections')
    return sections, previous_end


def _chunk(events, end_tick):
    chunk = p.track_chunk(events)
    last_tick = events[-1][0] if events else 0
    # track_chunk adds EOT at the final event; retain any original trailing rest.
    ending = p.varlen(max(last_tick, end_tick) - last_tick) + b'\xff\x2f\x00'
    data = chunk[8:-4] + ending
    return b'MTrk' + struct.pack('>I', len(data)) + data


def preserve_sections(new_smf: bytes, new_manifest: dict, old_smf: bytes,
                      old_manifest: dict, names: list[str]) -> tuple[bytes, dict]:
    """Replace notes by onset and CCs by half-open named section intervals.

    Note-offs travel with their note-ons, even across section boundaries. New
    metadata, non-CC channel events, and final CC64-off events remain intact.
    Inputs are not mutated. Incompatible mappings or malformed MIDI raise.
    """
    new_tracks, old_tracks = _parse(new_smf), _parse(old_smf)
    if (len(new_tracks) != len(old_tracks) or
            len(new_manifest['tracks']) != len(new_tracks) - 1 or
            len(old_manifest['tracks']) != len(old_tracks) - 1):
        raise ValueError('MIDI and manifest track counts must match')
    for index, (new, old) in enumerate(zip(new_tracks[1:], old_tracks[1:])):
        new_info, old_info = new_manifest['tracks'][index], old_manifest['tracks'][index]
        if (new[2] != old[2] or
                any(new_info[key] != old_info[key] for key in ('role', 'pc', 'patch'))):
            raise ValueError(f'Track {index} channel/program mapping differs')
        channels, programs = new[2]
        if channels != programs.keys() or any(pc != new_info['pc'] for pc in programs.values()):
            raise ValueError(f'Track {index} program mapping disagrees with manifest')
    new_sections, new_end = _sections(new_manifest)
    old_sections, old_end = _sections(old_manifest)
    intervals = []
    for name in dict.fromkeys(names):
        if name not in new_sections or name not in old_sections:
            raise ValueError(f'Section missing from old or new manifest: {name}')
        start, end = new_sections[name]
        old_start, old_stop = old_sections[name]
        if end - start != old_stop - old_start:
            raise ValueError(f'Section quarter length differs: {name}')
        intervals.append((start, end, old_start, old_stop))

    def selected(tick):
        return any(start <= tick < end for start, end, _, _ in intervals)

    def is_cc(event):
        return event[2][0] & 0xf0 == 0xb0

    def final_pedal_off(event, end):
        return event[0] == end and event[2][1:] == b'\x40\x00' and is_cc(event)

    manifest = deepcopy(new_manifest)
    chunks = [_chunk(list(new_tracks[0][0]), new_tracks[0][3])]
    windows = []
    sec_per_q = round(60000000 / manifest['bpm']) / 1000000
    for index, (new, old) in enumerate(zip(new_tracks[1:], old_tracks[1:])):
        events = [event for event in new[0]
                  if not (is_cc(event) and selected(event[0]) and
                          not final_pedal_off(event, new_end))]
        notes = [note for note in new[1] if not selected(note[0][0])]
        for start, end, old_start, old_stop in intervals:
            shift = start - old_start
            for onset, off in old[1]:
                if old_start <= onset[0] < old_stop:
                    notes.append(((onset[0] + shift, onset[1], onset[2]),
                                  (off[0] + shift, off[1], off[2])))
            for event in old[0]:
                if (is_cc(event) and old_start <= event[0] < old_stop and
                        not final_pedal_off(event, old_end)):
                    events.append((event[0] + shift, event[1], event[2]))
        for onset, off in notes:
            events.extend((onset, off))
            a = onset[0] / p.PPQ * sec_per_q + .04
            b = min(off[0] / p.PPQ * sec_per_q, onset[0] / p.PPQ * sec_per_q + .8)
            if b > a:
                windows.append((a, b))
        chunks.append(_chunk(events, new[3]))
        manifest['tracks'][index]['notes'] = len(notes)
    merged = []
    for a, b in sorted(windows):
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    smf = b'MThd' + struct.pack('>IHHH', 6, 1, len(chunks), p.PPQ) + b''.join(chunks)
    manifest['active_intervals'] = merged
    manifest['sha256_midi'] = hashlib.sha256(smf).hexdigest()
    return smf, manifest
