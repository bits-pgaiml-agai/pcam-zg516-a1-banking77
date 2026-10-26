# Team — Group 15

| Member | Track |
|--------|-------|
| Anil Kumar Reddy K | Data + baseline Colab (E1) + notebook backbone — **delivered** |
| Takkars Bhavani | Prompt engineering (E2) + decoding study (E3) |
| Nisha Palanisamy | Structured JSON (E4) + tool calling (E5) + templates |
| Venkata Srinivasa Rao Tunuguntla | Architecture/adaptation + eval/failures (E6) + E7 checklist/demo + report §§4,5,9,11–13 — **delivered (review)** |

## Shared contracts (frozen to Member 1)

- Dataset: BANKING77 (PolyAI CSVs, pinned revision in notebook / `data/raw/`)
- Model: `Qwen/Qwen2.5-1.5B-Instruct` revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`
- Eval set: `data/eval/development_evaluation.csv` (40 rows); test pilot reserved
- Output schema: `schemas/response.schema.json`  
  Keys: `intent`, `response`, `action_required`, `tool_name`, `tool_arguments`
- Tool: `transaction_status_lookup` only (`schemas/tool_transaction_status_lookup.json`, `src/tools.py`)
- Seed: 42
