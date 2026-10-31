# Application architecture (Evaluation)

See also report §5 in [`reports/BANKING77_Report_Sections_4_5_9_11_12_13_Architecture_Eval.md`](../../reports/BANKING77_Report_Sections_4_5_9_11_12_13_Architecture_Eval.md).

## Design goals

1. Reproducible Colab workflow on a small instruct LLM.  
2. Strict machine-readable outputs before any tool side effect.  
3. Synthetic tools only — no credentials, no real accounts.  
4. Measurable experiments E1–E7 aligned to the assignment brief.

## Control points

| Stage | Control |
|-------|---------|
| Prompt | Label list + privacy rules + optional few-shot |
| Decode | Greedy for production-like JSON; sampling for E3 study |
| Validate | Bare JSON; exact keys; allowlisted tool |
| Tool | `TXN-DEMO-###` pattern; mock table in [`src/tools.py`](../../src/tools.py) |
| Eval | Separate C1–C5 metrics; development vs reserved split |

## Adaptation

Prompting is the implemented adaptation. RAG/PEFT are documented trade-offs, not required for the baseline submission path.
