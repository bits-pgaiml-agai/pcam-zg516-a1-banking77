# 8–10 minute group demo script

**Project:** BANKING77 banking assistant (Group 15)  
**Runtime:** Colab T4 · notebook `BANKING77_GenAI_Assistant.ipynb`

| Min | Speaker | Content |
|-----|---------|---------|
| 0:00–0:45 | Venkat | Problem: intent + safe reply + optional mock tool; not a real bank |
| 0:45–2:00 | Anil | Dataset prep, seed 42, pilots, model pin, E1 0/3 schema |
| 2:00–3:30 | Bhavani | E2 prompt table + E3 greedy vs sample (once run) |
| 3:30–5:00 | Nisha | Schema validation + `transaction_status_lookup` demo |
| 5:00–7:30 | Venkat | Architecture diagram; prompting vs RAG vs PEFT; E6 F1–F3 live; F6 refusal; four metrics |
| 7:30–9:00 | Venkat | E7 walkthrough: prompt → generate → validate → tool/fallback |
| 9:00–10:00 | All | Limits, responsible use, Q&A |

## Live clicks (Venkat segment)

1. Open `evidence/member1/E1_baseline_outputs.jsonl` — show F3 unsafe card-number ask.  
2. Run `dispatch_tool("transaction_status_lookup", {"transaction_id": "TXN-DEMO-001"})`.  
3. Run invalid ID `TXN-999` — show rejection.  
4. State: “We report schema validity and safety separately from intent accuracy.”

## Backup if GPU unavailable

Use committed evidence under `evidence/member1/` and `evidence/member4/`; still narrate the pipeline from the architecture section.
