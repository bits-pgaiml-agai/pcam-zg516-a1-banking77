# pcam-zg516-a1-banking77

**BITS Pilani WILP · PGAIML · PCAM\* ZG516 Applied Generative AI**  
**Group Major Project / Assignment-1 · Dataset D1: BANKING77**

Banking customer-service assistant: intent understanding + safe response generation + structured JSON + simulated tool calling, using a pretrained Hugging Face causal LLM (prompting-focused; no training from scratch).

## Team

See [TEAM.md](TEAM.md). Group 15.

## Status

| Area | Status |
|------|--------|
| Member 1 (Anil): data + E1 baseline + notebook backbone | In repo |
| Member 2 (Bhavani): E2 prompts + E3 decoding | In repo (review; see evidence/member2) |
| Member 4 (Venkat): architecture, adaptation, E6/E7, eval rubric | In repo (review) |
| E4–E5 | Scaffold in notebook; Nisha |

Member 1 handoff: [docs/member1/HANDOFF.txt](docs/member1/HANDOFF.txt)  
Member 4 handoff: [docs/member4/HANDOFF.txt](docs/member4/HANDOFF.txt)  
E1 evidence: [evidence/member1/](evidence/member1/)  
E6/E7 + rubric: [evidence/member4/](evidence/member4/)  
Report §§2, 3, 6: [reports/BANKING77_Member1_Report_Sections_2_3_6.docx](reports/BANKING77_Member1_Report_Sections_2_3_6.docx)  
Report §§4, 5, 9, 11–13: [reports/BANKING77_Member4_Report_Sections_4_5_9_11_12_13.md](reports/BANKING77_Member4_Report_Sections_4_5_9_11_12_13.md)  
Report §§7–8: [reports/BANKING77_Member2_Report_Sections_7_8.md](reports/BANKING77_Member2_Report_Sections_7_8.md)  
E2/E3 evidence: [evidence/member2/](evidence/member2/)  
Demo script: [demo/E7_demo_script.md](demo/E7_demo_script.md)

## Repository layout

```text
pcam-zg516-a1-banking77/
├── notebooks/BANKING77_GenAI_Assistant.ipynb
├── data/
│   ├── raw/                 # pinned PolyAI train/test CSVs
│   └── eval/                # fixed pool + 40-row pilots
├── schemas/                 # response + tool contracts
├── src/tools.py             # mock transaction_status_lookup
├── evidence/member1/        # E1 outputs, audit, environment
├── docs/member1/            # attribution, validation, handoff
├── reports/                 # report section drafts
├── prompts/                 # future prompt logs
├── requirements.txt
├── TEAM.md
└── README.md
```

## Shared contracts

- Model: `Qwen/Qwen2.5-1.5B-Instruct` (pinned revision in notebook)
- JSON keys: `intent`, `response`, `action_required`, `tool_name`, `tool_arguments`
- Tool: `transaction_status_lookup` with `TXN-DEMO-###` ids only
- Seed: 42

## Required experiments

| ID | Experiment | Owner lead |
|----|------------|------------|
| E1 | Baseline simple prompt | Anil (done) |
| E2 | ≥4 prompt variants | Bhavani (done — evidence/member2) |
| E3 | Greedy + temperature + top-k/top-p | Bhavani (done — evidence/member2) |
| E4 | Structured JSON + validation | Nisha |
| E5 | ≥1 tool/function | Nisha |
| E6 | ≥3 failure cases | Venkat (observed F1–F3 + designed F4–F6) |
| E7 | Integrated final workflow | Venkat checklist/demo; full numbers after E2–E5 |

## Quick start

```bash
git clone https://github.com/bits-pgaiml-agai/pcam-zg516-a1-banking77.git
cd pcam-zg516-a1-banking77
pip install -r requirements.txt
```

### Colab

1. Upload `notebooks/BANKING77_GenAI_Assistant.ipynb`
2. Runtime → T4 GPU → Run all  
3. Default run: data prep + E1 only (`RUN_TEAM_EXPERIMENTS=False`)  
4. For E2–E5 set `RUN_TEAM_EXPERIMENTS=True`; for reserved-test eval set `RUN_FINAL_EVAL=True` after locking the prompt on development data

## Safety

Use only public BANKING77 text and mock tool backends. Do not use real banking credentials, account numbers, or personal financial data.
