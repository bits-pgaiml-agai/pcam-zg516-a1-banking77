"""E4/E5 runner: E4 structured-output validation + E5 tool calling."""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "structured_tools"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from run_e2_e3 import build_messages, validate_output, intent_names  # noqa: E402
from tools import TOOL_NAME, dispatch_tool, transaction_status_lookup  # noqa: E402

OLLAMA_MODEL = os.environ.get("E4_OLLAMA_MODEL", "qwen2.5:1.5b-instruct")
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434") + "/api/chat"


def ollama_chat(messages, *, temperature=0.0, max_tokens=180):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data.get("message") or {}).get("content", "").strip()


def make_valid(intent="activate_my_card", action=False, tool=None, args=None):
    return json.dumps(
        {
            "intent": intent,
            "response": "I can help with this request. Please use your bank's official support channel for account-specific actions.",
            "action_required": action,
            "tool_name": tool,
            "tool_arguments": args if args is not None else {},
        },
        ensure_ascii=False,
    )


def run_e4():
    cases = [
        {
            "case_id": "V1_valid_no_tool",
            "raw": make_valid(),
            "expect_valid": True,
        },
        {
            "case_id": "V2_valid_tool_request",
            "raw": make_valid(
                intent="pending_transfer",
                action=True,
                tool="transaction_status_lookup",
                args={"transaction_id": "TXN-DEMO-001"},
            ),
            "expect_valid": True,
        },
        {
            "case_id": "R1_markdown_fence",
            "raw": "```json\n" + make_valid() + "\n```",
            "expect_valid": False,
        },
        {
            "case_id": "R2_invented_intent",
            "raw": make_valid(intent="why_cant_i_use_card"),
            "expect_valid": False,
        },
        {
            "case_id": "R3_bad_action_type",
            "raw": '{"intent":"activate_my_card","response":"ok","action_required":"yes","tool_name":null,"tool_arguments":{}}',
            "expect_valid": False,
        },
        {
            "case_id": "R4_unallowlisted_tool",
            "raw": make_valid(action=True, tool="verify_my_identity", args={"card_number": ""}),
            "expect_valid": False,
        },
        {
            "case_id": "R5_action_true_null_tool",
            "raw": make_valid(action=True, tool=None, args={}),
            "expect_valid": False,
        },
        {
            "case_id": "R6_prose_before_json",
            "raw": "Sure!\n" + make_valid(),
            "expect_valid": False,
        },
        {
            "case_id": "R7_extra_keys",
            "raw": '{"intent":"activate_my_card","response":"ok","action_required":false,"tool_name":null,"tool_arguments":{},"confidence":0.9}',
            "expect_valid": False,
        },
        {
            "case_id": "R8_bad_txn_id",
            "raw": make_valid(
                action=True,
                tool="transaction_status_lookup",
                args={"transaction_id": "TXN-999"},
            ),
            "expect_valid": False,
        },
    ]

    # Re-validate a few real Prompt/decoding generations for continuity.
    m2 = ROOT / "evidence" / "prompts_decoding" / "E2_constraint_based.jsonl"
    if m2.exists():
        for i, line in enumerate(m2.read_text(encoding="utf-8").splitlines()[:3]):
            obj = json.loads(line)
            cases.append(
                {
                    "case_id": f"M2_constraint_{i+1}_{obj['source_id']}",
                    "raw": obj["raw_output"],
                    "expect_valid": None,
                    "gold_intent": obj.get("gold_intent"),
                }
            )

    rows = []
    for case in cases:
        item, errors = validate_output(case["raw"])
        valid = item is not None and not errors
        rows.append(
            {
                "case_id": case["case_id"],
                "expect_valid": case.get("expect_valid"),
                "actual_valid": valid,
                "match_expectation": (
                    None
                    if case.get("expect_valid") is None
                    else valid == case["expect_valid"]
                ),
                "predicted_intent": item.get("intent") if item else None,
                "validation_errors": "; ".join(errors),
                "raw_output": case["raw"],
            }
        )

    out_csv = OUT / "E4_validation_cases.csv"
    import pandas as pd

    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    designed = df[df.expect_valid.notna()]
    summary = {
        "n_designed": int(len(designed)),
        "expectation_matches": int(designed.match_expectation.sum()),
        "n_live_m2_checked": int(df.expect_valid.isna().sum()),
        "schema_path": "schemas/response.schema.json",
        "required_keys": [
            "intent",
            "response",
            "action_required",
            "tool_name",
            "tool_arguments",
        ],
    }
    (OUT / "E4_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("E4", summary, flush=True)
    return df


def run_e5_direct():
    invocations = [
        ("ok_001", TOOL_NAME, {"transaction_id": "TXN-DEMO-001"}),
        ("ok_002", TOOL_NAME, {"transaction_id": "TXN-DEMO-002"}),
        ("not_found", TOOL_NAME, {"transaction_id": "TXN-DEMO-999"}),
        ("bad_format", TOOL_NAME, {"transaction_id": "TXN-1001"}),
        ("not_allowlisted", "verify_my_identity", {"card_number": "4111"}),
        ("extra_arg", TOOL_NAME, {"transaction_id": "TXN-DEMO-001", "amount": 10}),
    ]
    rows = []
    for case_id, name, args in invocations:
        result = dispatch_tool(name, args)
        rows.append({"case_id": case_id, "tool_name": name, "arguments": json.dumps(args), "result": json.dumps(result)})
        print(case_id, result, flush=True)
    import pandas as pd

    pd.DataFrame(rows).to_csv(OUT / "E5_tool_invocations.csv", index=False)
    schema = json.loads((ROOT / "schemas" / "tool_transaction_status_lookup.json").read_text(encoding="utf-8"))
    (OUT / "E5_tool_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    return rows


def run_e5_llm_integrated():
    customer = "Please check the status of transaction TXN-DEMO-001."
    e2_summary_path = ROOT / "evidence" / "prompts_decoding" / "E2_summary.json"
    prompt_variant = "constraint_based"
    if e2_summary_path.exists():
        prompt_variant = json.loads(e2_summary_path.read_text(encoding="utf-8")).get(
            "best_variant_by_json_then_intent", prompt_variant
        )
    prompt_variant = os.environ.get("E5_PROMPT_VARIANT", prompt_variant)
    t0 = time.perf_counter()
    raw = ollama_chat(build_messages(customer, variant=prompt_variant, include_tool=True), temperature=0.0)
    item, errors = validate_output(raw)
    tool_result = None
    final_response = "I could not safely interpret that request. Please use your bank's official support channel."
    if item is not None and not errors:
        if item.get("action_required") and item.get("tool_name"):
            tool_result = dispatch_tool(item["tool_name"], item["tool_arguments"])
            final_messages = [
                {
                    "role": "system",
                    "content": "Write a short customer response using only the supplied synthetic tool result. State clearly that it is a demonstration. Do not invent facts or claim a real bank action.",
                },
                {
                    "role": "user",
                    "content": f"Customer request: {customer}\nSynthetic tool result: {json.dumps(tool_result)}",
                },
            ]
            final_response = ollama_chat(final_messages, temperature=0.0, max_tokens=90)
        else:
            final_response = item["response"]
            # Fallback: if model failed to request tool, still demonstrate forced tool path.
            if tool_result is None:
                forced = dispatch_tool(TOOL_NAME, {"transaction_id": "TXN-DEMO-001"})
                tool_result = {"forced_demo": True, **forced}
    elapsed = time.perf_counter() - t0
    demo = {
        "customer_text": customer,
        "runtime": "ollama",
        "model": OLLAMA_MODEL,
        "prompt_variant": prompt_variant,
        "stage1_raw": raw,
        "stage1_parsed": item,
        "validation_errors": errors,
        "tool_result": tool_result,
        "final_response": final_response,
        "latency_seconds": round(elapsed, 3),
        "official_hf_model": "Qwen/Qwen2.5-1.5B-Instruct",
        "note": "Local Ollama fallback; re-run on Colab HF pin if required for checkpoint alignment.",
    }
    (OUT / "E5_integrated_tool_demo.json").write_text(json.dumps(demo, indent=2, ensure_ascii=False), encoding="utf-8")
    print("E5 integrated", json.dumps({k: demo[k] for k in ["validation_errors", "tool_result", "final_response"]}, indent=2), flush=True)
    return demo


def main():
    env = {
        "runtime": "e4_e5",
        "ollama_model": OLLAMA_MODEL,
        "intent_count": len(intent_names),
        "tool": TOOL_NAME,
    }
    (OUT / "environment.json").write_text(json.dumps(env, indent=2), encoding="utf-8")
    run_e4()
    run_e5_direct()
    run_e5_llm_integrated()
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
