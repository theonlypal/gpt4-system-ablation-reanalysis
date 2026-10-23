#!/usr/bin/env python3
"""Read-only replay of the public evidence archive. No provider/network calls."""
import argparse
import base64
import csv
import hashlib
import io
import json
import types
import zipfile
from collections import Counter
from pathlib import Path

CSV_SHA = "139332401aa7213b6e725df7e79707940eee754d68ed05c56011be94f728b7d3"
ZIP_SHA = "04d79ddb0f961729369da8ae46c58f7293e42dfd278d2e9b703edc0cec6455d2"
CHAIN_HEAD = "b3a01f4178e750532bb79d1c5efc2654a6d76cab31e536f1dead9ca756369460"
COMMIT = "3fd330869c1a4a410047bc70b3f661f1a9d69aca"
BASE = "https://github.com/theonlypal/void-matrix-complete-analysis"
PREFIX = "void-matrix-evidence-v1.0.0/"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def read_rows(path):
    data = Path(path).read_bytes()
    require(sha(data) == CSV_SHA, "CSV SHA-256 mismatch")
    rows = list(csv.DictReader(io.StringIO(data.decode())))
    require(len({r['slot_id'] for r in rows}) == len(rows), "duplicate CSV slots")
    return rows

def independent_openai(payload):
    """Independent successful Chat Completions classifier, frozen Matrix semantics."""
    choice = (payload.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    text = msg.get("content")
    present = text is not None and "content" in msg
    if isinstance(text, list):
        parts = [p.get("text", "") for p in text if isinstance(p, dict) and p.get("type") in ("text", "output_text")]
        text, present = "".join(parts), bool(parts)
    elif text is not None and not isinstance(text, str):
        text = str(text)
    stop = choice.get("finish_reason")
    if stop == "content_filter":
        label = "SB"
    elif msg.get("refusal") or stop == "refusal":
        label = "RF"
    elif msg.get("tool_calls") or msg.get("function_call"):
        label = "TC"
    elif text:
        invisible = {0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0xFEFF, 0x2060,
                     0x2061, 0x2062, 0x2063, 0x2064, 0x2066, 0x2067, 0x2068,
                     0x2069, 0x202A, 0x202B, 0x202C, 0x202D, 0x202E}
        near = all(c.isspace() or ord(c) in invisible for c in text) or text.strip() in {".", "..", "...", "....", "…", "…."}
        label = "NV" if near else "R"
    elif stop == "length":
        label = "V1"
    elif stop == "stop":
        label = "V0" if present else "V2"
    else:
        label = "VU"
    return label, text, stop, present

def audit(csv_path, archive, out):
    rows = read_rows(csv_path)
    by_slot = {r['slot_id']: r for r in rows}
    with open(archive, "rb") as f:
        h = hashlib.file_digest(f, "sha256").hexdigest()
    require(h == ZIP_SHA, "Evidence archive SHA-256 mismatch")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    checked = Counter()
    receipt_index = []
    final_slots, raw_paths = set(), set()
    returned_mismatches = []
    with zipfile.ZipFile(archive) as z:
        read = lambda p: z.read(PREFIX + p)
        protocol = json.loads(read("study/protocol.json"))
        prompts = json.loads(read("study/prompts.json"))
        source = read("void_matrix.FROZEN.py")
        module = types.ModuleType("frozen_matrix")
        module.__file__ = str(Path(archive).resolve()) + "/void_matrix.FROZEN.py"
        exec(compile(source, module.__file__, "exec"), module.__dict__)
        frozen = json.loads(read('study/frozen_manifest.json'))
        require(module.unsigned_manifest_sha256(frozen) == frozen['manifest_sha256'], 'frozen manifest self hash')
        for filename, expected in frozen['files'].items():
            content = source if filename == 'void_matrix.py' else read('study/' + filename)
            require(sha(content) == expected, f'frozen source {filename}')
        schedule = {s['slot_id']: s for s in map(json.loads, read("study/schedule.jsonl").splitlines())}
        sm = json.loads(read('study/schedule_manifest.json'))
        reconstructed, exclusions = module.build_schedule_artifacts(protocol, prompts, json.loads(read('study/models.json')), sm['profile'], sm['public_seed'])
        require(reconstructed == list(schedule.values()), 'schedule reconstruction')
        require(exclusions == sm['structural_exclusions'], 'schedule exclusions')
        require(sha(read('study/schedule.jsonl')) == sm['schedule_sha256'], 'schedule hash')
        require(set(schedule) == set(by_slot), "CSV and frozen schedule differ")
        previous, started = "0" * 64, {}
        with z.open(PREFIX + "study/run/events.jsonl") as events:
            for line_number, line in enumerate(events, 1):
                event = json.loads(line)
                unsigned = {k: v for k, v in event.items() if k != "event_sha256"}
                require(event['previous_event_sha256'] == previous, f"chain predecessor {line_number}")
                require(sha(canonical(unsigned)) == event['event_sha256'], f"chain hash {line_number}")
                previous = event['event_sha256']
                checked['event_hashes'] += 1
                aid, kind = event['attempt_id'], event['event_type']
                if kind == 'trial_started':
                    require(aid not in started, "duplicate attempt start")
                    started[aid] = event
                    continue
                require(kind in ('trial_completed', 'trial_attempt_completed'), f"unhandled event {kind}")
                require(aid in started, "completion without start")
                start = started.pop(aid)
                raw_path = event['raw_path']
                require(raw_path not in raw_paths, "duplicate raw reference")
                raw_paths.add(raw_path)
                data = read("study/" + raw_path)
                require(sha(data) == event['raw_sha256'], f"raw hash {raw_path}")
                raw = json.loads(data)
                slot, transport = raw['slot'], raw['transport']
                require(slot == event['slot'] == start['slot'] == schedule[slot['slot_id']], "slot mismatch")
                require(raw['attempt_id'] == aid and raw['attempt_number'] == event['attempt_number'] == start['attempt_number'], "attempt mismatch")
                require(raw['request'] == start['request'], "request/start mismatch")
                require(raw['system_prompt'] == prompts['systems'][slot['system_id']], "system mismatch")
                require(raw['user_prompt'] == prompts['cases'][slot['prompt_id']], "user mismatch")
                url, headers, body = module.request_shape_for_slot(slot, raw['system_prompt']['text'], raw['user_prompt']['text'])
                require(module.public_request_record(url, headers, body) == raw['request'], "request reconstruction mismatch")
                require(sha(canonical(body)) == raw['request']['body_sha256'], "request body hash")
                response = base64.b64decode(transport['raw_body_base64'], validate=True)
                require(sha(response) == transport['raw_body_sha256'] == event['raw_body_sha256'], "response hash")
                require(len(response) == transport['raw_body_bytes'], "response length")
                if transport.get('json') is not None:
                    require(json.loads(response) == transport['json'], "body/parsed JSON mismatch")
                replay = module.classify_response(slot['endpoint'], transport, protocol)
                require(replay == event['classification'], "frozen classifier replay mismatch")
                checked['raw_attempts'] += 1
                if kind != 'trial_completed':
                    require(event['retry_scheduled'] is True, "retry marker")
                    checked['nonfinal_attempts'] += 1
                    continue
                sid = slot['slot_id']
                require(sid not in final_slots, "duplicate final slot")
                final_slots.add(sid)
                r = by_slot[sid]
                for k, value in slot.items():
                    require(str(value) == r[k], f"CSV slot field {k}")
                require(int(r['event_line']) == line_number, "CSV event line")
                require(r['event_utc'] == event['event_utc'], 'CSV event time')
                require(r['prompt_text'] == raw['user_prompt']['text'] and r['prompt_sha256'] == raw['user_prompt']['sha256'], 'CSV prompt text/hash')
                require(r['attempt_id'] == aid and int(r['attempt_number']) == raw['attempt_number'], 'CSV final attempt')
                require(r['http_status'] == str(transport['http_status']), 'CSV HTTP status')
                require(r['raw_sha256'] == event['raw_sha256'] and r['raw_body_sha256'] == event['raw_body_sha256'], "CSV raw hashes")
                require(r['classification'] == r['independent_classification'] == replay['classification'], "CSV classification")
                require(int(r['utf8_bytes']) == replay['visible_text']['utf8_bytes'], "CSV byte count")
                require(r['visible_sha256'] == replay['visible_text']['sha256'], "CSV answer hash")
                checked['final_trials'] += 1
                if slot['provider'] == 'openai' and transport['http_status'] == 200:
                    label, text, stop, present = independent_openai(json.loads(response))
                    require(label == r['classification'], "independent classification mismatch")
                    require(stop == r['stop_reason'] and present == (r['text_container_present'] == 'True'), "CSV termination/container")
                    require(sha((text or '').encode()) == r['visible_sha256'], "independent output hash")
                    checked['independent_openai_successes'] += 1
                    if transport['json']['model'] != slot['model_id']:
                        returned_mismatches.append(sid)
                    if slot['prompt_id'] in ('core_silence', 'core_nothing', 'core_null', 'matched_speech', 'matched_something', 'matched_value') and slot['system_id'] in ('primary', 'no_embodiment', 'no_output_restriction', 'none'):
                        receipt_index.append({**{k: r[k] for k in ('slot_id', 'model_id', 'study_id', 'system_id', 'parameter_track', 'budget', 'prompt_id', 'classification', 'raw_path', 'raw_sha256', 'raw_body_sha256', 'event_line')},
                            'request_sha256': raw['request']['body_sha256'], 'answer': text, 'utf8_bytes': len((text or '').encode()),
                            'stop': stop, 'returned_model': transport['json']['model'], 'started_utc': transport['started_utc'],
                            'ended_utc': transport['ended_utc'], 'request': body})
                if checked['raw_attempts'] % 5000 == 0:
                    print(f"Checked {checked['raw_attempts']} raw attempts", flush=True)
        require(not started, "unfinished attempts")
        require(final_slots == set(by_slot), "missing final receipts")
        require(previous == CHAIN_HEAD, "published chain head mismatch")
        actual_raw = {n.removeprefix(PREFIX + 'study/') for n in z.namelist() if n.startswith(PREFIX + 'study/run/raw/') and n.endswith('.json')}
        require(actual_raw == raw_paths, "unreferenced or missing raw records")
        for filename in ('protocol.json', 'prompts.json', 'schedule_manifest.json', 'frozen_manifest.json'):
            (out / filename).write_bytes(read('study/' + filename))
        source_hashes = {p: sha(read(p)) for p in ('void_matrix.FROZEN.py', 'study/protocol.json', 'study/prompts.json', 'study/schedule.jsonl', 'study/frozen_manifest.json')}
    require(not returned_mismatches, f"returned model mismatches: {returned_mismatches}")
    report = {'status': 'PASS', 'source_commit': COMMIT, 'csv_sha256': CSV_SHA, 'archive_sha256': ZIP_SHA,
              'event_chain_head': previous, 'checks': dict(checked), 'source_hashes': source_hashes,
              'openai_returned_model_mismatches': returned_mismatches,
              'scope': 'All scheduled final CSV rows and all raw attempts replayed against frozen classifier; successful OpenAI responses additionally independently classified. No inference or provider API calls.'}
    (out / 'receipt_index.json').write_text(json.dumps(receipt_index, ensure_ascii=False, indent=2) + '\n')
    (out / 'audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--csv', default='inputs/trial_level.csv')
    p.add_argument('--archive', default='inputs/void-matrix-evidence-v1.0.0.zip')
    p.add_argument('--out', default='generated')
    args = p.parse_args()
    audit(args.csv, args.archive, args.out)
