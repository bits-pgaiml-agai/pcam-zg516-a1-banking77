# E2 prompt variants (Member 2)

Shared `OUTPUT_RULES` plus the 77-label list are always included. Variants differ only in the task instruction / examples.

| Variant | Instruction focus |
|---------|-------------------|
| `zero_shot` | Classify + safe response; no examples |
| `few_shot` | Same + 4 fixed in-prompt examples from `data/eval/in_prompt_examples.csv` |
| `role_context` | First-line support persona; escalate account-specific actions |
| `constraint_based` | Emphasize bare JSON, exact keys/types, exact label copy |

Baseline (`baseline`) remains Member 1 E1 only and is not part of the four-variant E2 table.

Runner: `scripts/run_member2_e2_e3.py`
