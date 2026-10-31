# E2 prompt variants (Prompt/decoding)

Shared `OUTPUT_RULES` plus the 77-label list are always included. Variants differ only in the task instruction / examples.

| Variant | Instruction focus |
|---------|-------------------|
| `zero_shot` | Classify + safe response; no examples |
| `few_shot` | Same + 4 fixed in-prompt examples from [`data/eval/in_prompt_examples.csv`](../data/eval/in_prompt_examples.csv) |
| `role_context` | First-line support persona; escalate account-specific actions |
| `constraint_based` | Emphasize bare JSON, exact keys/types, exact label copy |

Baseline (`baseline`) remains Baseline E1 only and is not part of the four-variant E2 table.

Runner: [`scripts/run_e2_e3.py`](../scripts/run_e2_e3.py) / [`scripts/run_e2_e3_ollama.py`](../scripts/run_e2_e3_ollama.py)

## Exact prompts sent to the LLM

| File | Contents |
|------|----------|
| [ACTUAL_PROMPTS_E2.md](ACTUAL_PROMPTS_E2.md) | Readable copy of system/user messages for all four variants |
| [`sample_rendered_zero_shot.json`](sample_rendered_zero_shot.json) | Full rendered chat (includes all 77 labels) |
| [`sample_rendered_few_shot.json`](sample_rendered_few_shot.json) | Same + 4 few-shot examples |
| [`sample_rendered_role_context.json`](sample_rendered_role_context.json) | Role-context task line |
| [`sample_rendered_constraint_based.json`](sample_rendered_constraint_based.json) | Constraint-based task line |

Sample customer text in the JSON files: `What I topped up was reverted by the app.`  
Jinja template used by programmatic rendering: [assistant_template.jinja2](assistant_template.jinja2)
