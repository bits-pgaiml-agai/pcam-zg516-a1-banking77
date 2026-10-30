# 8–10 minute group demo script

**Project:** BANKING77 banking assistant (Group 15)  
**Runtime:** Colab T4 · notebook `BANKING77_GenAI_Assistant.ipynb`

| Min | Segment | Speaker | Content |
|-----|---------|---------|---------|
| 0:00–0:45 | Intro | Any | Problem: intent + safe reply + optional mock tool; not a real bank |
| 0:45–2:00 | Baseline | Anil | Dataset prep, seed 42, pilots, model pin, E1 0/3 schema |
| 2:00–4:00 | Prompts/decoding | Venkat | E2 prompt table + E3 greedy vs sample |
| 4:00–5:30 | Structured tools | Nisha | Schema validation + `transaction_status_lookup` demo |
| 5:30–8:00 | Evaluation + E7 | Venkat | Architecture; prompting vs RAG vs PEFT; E6; metrics; integration |
| 8:00–10:00 | Close | All | Limits, responsible use, Q&A |

## Live clicks

1. Open `evidence/baseline/E1_baseline_outputs.jsonl` — show unsafe card-number ask failure.  
2. Run `dispatch_tool("transaction_status_lookup", {"transaction_id": "TXN-DEMO-001"})`.  
3. Run invalid ID `TXN-999` — show rejection.  
4. State: “We report schema validity and safety separately from intent accuracy.”

## Backup if GPU unavailable

Use committed evidence under `evidence/baseline/` and `evidence/evaluation/`; still narrate the pipeline from the architecture section.
