# E7 — Integrated workflow checklist

**Owner:** Venkata Srinivasa Rao Tunuguntla  
**Notebook:** [`notebooks/BANKING77_GenAI_Assistant.ipynb`](../../notebooks/BANKING77_GenAI_Assistant.ipynb)

## End-to-end path (must demo)

1. Load pinned BANKING77 + build subsets (Baseline cells).  
2. Build messages with chosen prompt variant (`zero_shot` recommended after local `qwen2.5:1.5b-instruct` E2; revisit after Colab HF re-run).  
3. Generate with chosen decoding (greedy recommended for JSON after E3).  
4. `validate_output` — reject Markdown, unknown intents, bad tools.  
5. If valid and `action_required`: `dispatch_tool("transaction_status_lookup", …)`.  
6. Produce final customer-facing string (grounded in mock tool result or escalation).  
7. Log metrics against eval rubric ([`eval_rubric.json`](eval_rubric.json)).

## Flags

| Flag | When |
|------|------|
| `RUN_TEAM_EXPERIMENTS=False` | Baseline default (E1 only) |
| `RUN_TEAM_EXPERIMENTS=True` | E2–E5 generation for group |
| `RUN_FINAL_EVAL=True` | Only after prompt locked on development data |

## Demo acceptance (minimum)

- [ ] Show one **failing E1** raw output and validator rejection (F1 or F3).  
- [ ] Show one **valid JSON** path on development text (after E2, or constraint prompt).  
- [ ] Show **tool** path with `TXN-DEMO-001` (direct `dispatch_tool` always available).  
- [ ] Show **refusal** on credential bait (F6).  
- [ ] State four metrics separately (intent, schema, safety, tool).  

## Local evidence status (`qwen2.5:1.5b-instruct`)

- [x] E2 comparison table ([`evidence/prompts_decoding/E2_summary.json`](../prompts_decoding/E2_summary.json)) — best: `zero_shot`  
- [x] E3 decoding table ([`E3_summary.json`](../prompts_decoding/E3_summary.json)) — greedy preferred  
- [x] E4 designed validation 10/10 ([`E4_summary.json`](../structured_tools/E4_summary.json))  
- [x] E5 direct tool + integrated LLM path (validator blocked unsafe/invalid tool call)  
- [ ] Optional: expand E2 to full 40-row development pilot on Colab HF pin  

Architecture and controls for E7 are ready; use committed evidence if live GPU is unavailable.
