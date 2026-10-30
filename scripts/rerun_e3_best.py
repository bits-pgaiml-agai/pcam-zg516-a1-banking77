"""Re-run E3 only using best E2 prompt variant."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_e2_e3_ollama as m  # noqa: E402

OUT = ROOT / "evidence" / "prompts_decoding"
compare_df = pd.read_csv(OUT / "E2_evaluation_subset.csv")
summary = json.loads((OUT / "E2_summary.json").read_text(encoding="utf-8"))
best = summary["best_variant_by_json_then_intent"]
decode_rows = compare_df.sample(n=min(m.E3_N, len(compare_df)), random_state=m.SEED + 1)
decode_settings = [
    ("greedy", {"temperature": 0.0}),
    ("temperature_0.7_top_k_50", {"temperature": 0.7, "top_k": 50}),
    ("temperature_0.7_top_p_0.9", {"temperature": 0.7, "top_p": 0.9}),
]
decode_records = []
for row in decode_rows.itertuples():
    for setting_name, kwargs in decode_settings:
        t0 = time.perf_counter()
        raw = m.ollama_chat(m.build_messages(row.text, variant=best), **kwargs)
        elapsed = time.perf_counter() - t0
        item, errors = m.validate_output(raw)
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
                "prompt_variant": best,
            }
        )
        print(
            f"[E3 {setting_name}] {row.source_id} valid={decode_records[-1]['json_valid']} {elapsed:.1f}s",
            flush=True,
        )

decoding_comparison = pd.DataFrame(decode_records)
decoding_comparison.to_csv(OUT / "E3_decoding.csv", index=False)
e3_summary = decoding_comparison.groupby("decoding", as_index=False).agg(
    rows=("source_id", "count"),
    json_valid_rate=("json_valid", "mean"),
    intent_correct_rate=("intent_correct", "mean"),
    mean_latency_seconds=("latency_seconds", "mean"),
)
e3_summary.to_csv(OUT / "E3_decoding_summary.csv", index=False)
(OUT / "E3_summary.json").write_text(
    json.dumps(
        {
            "prompt_variant": best,
            "rows": decode_rows["source_id"].tolist(),
            "by_setting": e3_summary.to_dict(orient="records"),
        },
        indent=2,
    ),
    encoding="utf-8",
)
print(e3_summary.to_string(index=False), flush=True)
print("DONE", flush=True)
