# 8–10 minute group demo script

**Project:** BANKING77 banking assistant (Group 15)  
**Runtime:** Colab T4 · notebook `BANKING77_GenAI_Assistant.ipynb`

| Min | Segment | Content |
|-----|---------|---------|
| 0:00–0:45 | Intro | Problem: intent + safe reply + optional mock tool; not a real bank |
| 0:45–2:00 | Baseline | Dataset prep, seed 42, pilots, model pin, E1 0/3 schema |
| 2:00–3:30 | Prompts/decoding | E2 prompt table + E3 greedy vs sample |
| 3:30–5:00 | Structured tools | Schema validation + `transaction_status_lookup` demo |
| 5:00–7:30 | Evaluation | Architecture; prompting vs RAG vs PEFT; E6 failures; four metrics |
| 7:30–9:00 | Integration | E7 walkthrough: prompt → generate → validate → tool/fallback |
| 9:00–10:00 | Close | Limits, responsible use, Q&A |

## Live clicks

1. Open `evidence/baseline/E1_baseline_outputs.jsonl` — show unsafe card-number ask failure.  
2. Run `dispatch_tool("transaction_status_lookup", {"transaction_id": "TXN-DEMO-001"})`.  
3. Run invalid ID `TXN-999` — show rejection.  
4. State: “We report schema validity and safety separately from intent accuracy.”

## Backup if GPU unavailable

Use committed evidence under `evidence/baseline/` and `evidence/evaluation/`; still narrate the pipeline from the architecture section.
