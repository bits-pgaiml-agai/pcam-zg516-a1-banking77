"""E2/E3 via local Ollama (fallback when HF weights unavailable)."""

from __future__ import annotations

import json
import os
import random
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = ROOT / "data" / "eval"
OUT_DIR = ROOT / "evidence" / "prompts_decoding"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
OLLAMA_MODEL = os.environ.get("E2_OLLAMA_MODEL", "qwen2.5:3b")
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434") + "/api/chat"
E2_N = int(os.environ.get("E2_N", "10"))
E3_N = int(os.environ.get("E3_N", "3"))
MAX_TOKENS = 180

random.seed(SEED)
np.random.seed(SEED)

# Reuse prompt/validator builders from the HF runner module path by duplicating essentials.
sys.path.insert(0, str(ROOT / "scripts"))
from run_e2_e3 import (  # noqa: E402
    PROMPT_VARIANTS,
    build_messages,
    validate_output,
    intent_names,
)

dev_eval_df = pd.read_csv(EVAL_DIR / "development_evaluation.csv")


def ollama_chat(messages, *, temperature=0.0, top_k=None, top_p=None):
    options = {"num_predict": MAX_TOKENS, "temperature": temperature}
    if top_k is not None:
        options["top_k"] = top_k
    if top_p is not None:
        options["top_p"] = top_p
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": options,
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


def evaluate_prompt(frame, variant):
    records = []
    for idx, row in enumerate(frame.itertuples(), start=1):
        t0 = time.perf_counter()
        raw = ollama_chat(build_messages(row.text, variant=variant), temperature=0.0)
        elapsed = time.perf_counter() - t0
        item, errors = validate_output(raw)
        predicted = item.get("intent") if item and item.get("intent") in intent_names else "__INVALID__"
        records.append(
            {
                "source_id": row.source_id,
                "text": row.text,
                "gold_intent": row.intent,
                "predicted_intent": predicted,
                "json_valid": item is not None and not errors,
                "intent_correct": bool(item and not errors and item.get("intent") == row.intent),
                "response": item.get("response", "") if item else "",
                "raw_output": raw,
                "validation_errors": "; ".join(errors),
                "latency_seconds": round(elapsed, 3),
                "variant": variant,
            }
        )
        print(
            f"[{variant}] {idx}/{len(frame)} {row.source_id} valid={records[-1]['json_valid']} "
            f"correct={records[-1]['intent_correct']} {elapsed:.1f}s",
            flush=True,
        )
    result_df = pd.DataFrame(records)
    metric_labels = sorted((set(result_df.gold_intent) | set(result_df.predicted_intent)) - {"__INVALID__"})
    metrics = {
        "variant": variant,
        "rows": len(result_df),
        "gold_class_coverage": int(result_df.gold_intent.nunique()),
        "intent_accuracy": float(accuracy_score(result_df.gold_intent, result_df.predicted_intent)),
        "intent_correct_validated": float(result_df.intent_correct.mean()),
        "intent_macro_f1_represented_labels": float(
            f1_score(
                result_df.gold_intent,
                result_df.predicted_intent,
                labels=metric_labels,
                average="macro",
                zero_division=0,
            )
        ),
        "json_valid_rate": float(result_df.json_valid.mean()),
        "mean_latency_seconds": float(result_df.latency_seconds.mean()),
    }
    return metrics, result_df


def main():
    compare_df = dev_eval_df.sample(n=min(E2_N, len(dev_eval_df)), random_state=SEED).reset_index(drop=True)
    compare_df.to_csv(OUT_DIR / "E2_evaluation_subset.csv", index=False)

    env = {
        "runtime": "ollama",
        "ollama_model": OLLAMA_MODEL,
        "official_hf_model": "Qwen/Qwen2.5-1.5B-Instruct",
        "note": "Local Ollama fallback used because HF weight download was unavailable/slow. Re-run scripts/run_e2_e3.py on Colab T4 for the pinned HF checkpoint before final submission if required.",
        "seed": SEED,
        "e2_n": len(compare_df),
        "e3_n": E3_N,
    }
    (OUT_DIR / "environment.json").write_text(json.dumps(env, indent=2), encoding="utf-8")

    prompt_results = []
    for variant in PROMPT_VARIANTS:
        metrics, outputs = evaluate_prompt(compare_df, variant)
        prompt_results.append(metrics)
        outputs.to_csv(OUT_DIR / f"E2_{variant}.csv", index=False)
        (OUT_DIR / f"E2_{variant}.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in outputs.to_dict(orient="records")),
            encoding="utf-8",
        )
        print("METRICS", metrics, flush=True)

    prompt_comparison = pd.DataFrame(prompt_results).sort_values(
        ["json_valid_rate", "intent_correct_validated"], ascending=False
    )
    prompt_comparison.to_csv(OUT_DIR / "E2_prompt_comparison.csv", index=False)
    best_variant = str(prompt_comparison.iloc[0]["variant"])
    (OUT_DIR / "E2_summary.json").write_text(
        json.dumps(
            {
                "best_variant_by_json_then_intent": best_variant,
                "comparison": prompt_results,
                "subset_source_ids": compare_df["source_id"].tolist(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    decode_rows = compare_df.sample(n=min(E3_N, len(compare_df)), random_state=SEED + 1)
    decode_settings = [
        ("greedy", {"temperature": 0.0}),
        ("temperature_0.7_top_k_50", {"temperature": 0.7, "top_k": 50}),
        ("temperature_0.7_top_p_0.9", {"temperature": 0.7, "top_p": 0.9}),
    ]
    decode_records = []
    for row in decode_rows.itertuples():
        for setting_name, kwargs in decode_settings:
            t0 = time.perf_counter()
            raw = ollama_chat(build_messages(row.text, variant="constraint_based"), **kwargs)
            elapsed = time.perf_counter() - t0
            item, errors = validate_output(raw)
            decode_records.append(
                {
                    "source_id": row.source_id,
                    "customer_text": row.text,
                    "gold_intent": row.intent,
                    "decoding": setting_name,
                    "predicted_intent": item.get("intent") if item else "__INVALID__",
                    "json_valid": item is not None and not errors,
                    "intent_correct": bool(item and not errors and item.get("intent") == row.intent),
                    "response": item.get("response", "") if item else "",
                    "raw_output": raw,
                    "validation_errors": "; ".join(errors),
                    "latency_seconds": round(elapsed, 3),
                }
            )
            print(
                f"[E3 {setting_name}] {row.source_id} valid={decode_records[-1]['json_valid']} {elapsed:.1f}s",
                flush=True,
            )

    decoding_comparison = pd.DataFrame(decode_records)
    decoding_comparison.to_csv(OUT_DIR / "E3_decoding.csv", index=False)
    e3_summary = (
        decoding_comparison.groupby("decoding", as_index=False)
        .agg(
            rows=("source_id", "count"),
            json_valid_rate=("json_valid", "mean"),
            intent_correct_rate=("intent_correct", "mean"),
            mean_latency_seconds=("latency_seconds", "mean"),
        )
    )
    e3_summary.to_csv(OUT_DIR / "E3_decoding_summary.csv", index=False)
    (OUT_DIR / "E3_summary.json").write_text(
        json.dumps(
            {
                "prompt_variant": "constraint_based",
                "rows": decode_rows["source_id"].tolist(),
                "by_setting": e3_summary.to_dict(orient="records"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("DONE", flush=True)
    print(prompt_comparison.to_string(index=False), flush=True)
    print(e3_summary.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
