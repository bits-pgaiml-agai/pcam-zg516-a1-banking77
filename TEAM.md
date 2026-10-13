# Team — Group 15

| Member | Track (2-week plan) |
|--------|---------------------|
| Anil Kumar Reddy K | Data + baseline Colab (E1) + notebook backbone |
| Takkars Bhavani | Prompt engineering (E2) + decoding study (E3) |
| Nisha Palanisamy | Structured JSON (E4) + tool calling (E5) + templates |
| Venkata Srinivasa Rao Tunuguntla | Architecture/adaptation + eval/failures (E6) + integrate demo (E7) + report merge |

## Shared contracts (freeze Day 0)

- Dataset: BANKING77 (Hugging Face)
- Model: one Hugging Face causal instruct model (decide in Day-0 sync)
- Eval set: 30 fixed examples in `data/eval/`
- Output schema: `schemas/response.schema.json`
- Tool: `get_transaction_status` only (mock data; no real banking credentials)
