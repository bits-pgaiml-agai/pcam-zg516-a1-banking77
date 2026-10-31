# Team — Group 15

Contribution tracking for the final statement (not used as folder/report labels).

| Name | Workstream |
|------|------------|
| Anil Kumar Reddy K | Data prep, E1 baseline, notebook backbone |
| Nisha Palanisamy | E4 structured output, E5 tool calling, prompt templates |
| Venkata Srinivasa Rao Tunuguntla | E2 prompt engineering, E3 decoding study; architecture/adaptation; E6/E7 evaluation; report merge |

## Shared contracts

- Dataset: BANKING77 (PolyAI CSVs, pinned revision in notebook / [`data/raw/`](data/raw/))
- Model: `Qwen/Qwen2.5-1.5B-Instruct` revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`
- Eval set: [`data/eval/development_evaluation.csv`](data/eval/development_evaluation.csv) (40 rows); test pilot reserved
- Output schema: [`schemas/response.schema.json`](schemas/response.schema.json)  
  Keys: `intent`, `response`, `action_required`, `tool_name`, `tool_arguments`
- Tool: `transaction_status_lookup` only ([`schemas/tool_transaction_status_lookup.json`](schemas/tool_transaction_status_lookup.json), [`src/tools.py`](src/tools.py))
- Seed: 42
