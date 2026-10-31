# Fixed evaluation and example subsets (Baseline)

Seed: **42**. All prompt/decoding comparisons must use these rows.

| File | Rows | Purpose |
|------|------|---------|
| [`few_shot_pool.csv`](few_shot_pool.csv) | 77 | One working-training example per intent |
| [`in_prompt_examples.csv`](in_prompt_examples.csv) | 4 | Fixed few-shot examples used in prompts |
| [`development_evaluation.csv`](development_evaluation.csv) | 40 | Development pilot (same 40 intents) |
| [`official_test_pilot.csv`](official_test_pilot.csv) | 40 | Reserved test pilot (same 40 intents) |
| [`baseline_inputs.csv`](baseline_inputs.csv) | 3 | E1 baseline sample from development |
| [`intent_names.json`](intent_names.json) | 77 | Canonical label order |
| [`class_counts.csv`](class_counts.csv) | — | Per-intent counts after cleaning |

Do not tune prompts on the official test pilot. Full audit: [`evidence/baseline/data_audit.json`](../../evidence/baseline/data_audit.json).
