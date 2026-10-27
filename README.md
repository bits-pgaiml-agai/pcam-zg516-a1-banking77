# pcam-zg516-a1-banking77

**BITS Pilani WILP · PGAIML · PCAM\* ZG516 Applied Generative AI**  
**Group Major Project / Assignment-1 · Dataset D1: BANKING77**

Banking customer-service assistant: intent understanding + safe response generation + structured JSON + simulated tool calling, using a pretrained Hugging Face causal LLM (prompting-focused; no training from scratch).

## Team

See [TEAM.md](TEAM.md). Group 15.

## Status

| Workstream | Status |
|------------|--------|
| Data prep + E1 baseline + notebook | Done — `evidence/baseline/` |
| E2 prompts + E3 decoding | Done — `evidence/prompts_decoding/` |
| E4 schema + E5 tools + templates | Done — `evidence/structured_tools/` |
| Architecture, adaptation, E6/E7 eval | Done — `evidence/evaluation/` |

## Key paths

- Baseline notes: [docs/baseline/HANDOFF.txt](docs/baseline/HANDOFF.txt)  
- Evaluation notes: [docs/evaluation/HANDOFF.txt](docs/evaluation/HANDOFF.txt)  
- Report §§2, 3, 6: [reports/BANKING77_Report_Sections_2_3_6_Problem_Dataset_Baseline.docx](reports/BANKING77_Report_Sections_2_3_6_Problem_Dataset_Baseline.docx)  
- Report §§4, 5, 9, 11–13: [reports/BANKING77_Report_Sections_4_5_9_11_12_13_Architecture_Eval.md](reports/BANKING77_Report_Sections_4_5_9_11_12_13_Architecture_Eval.md)  
- Report §§7–8: [reports/BANKING77_Report_Sections_7_8_Prompts_Decoding.md](reports/BANKING77_Report_Sections_7_8_Prompts_Decoding.md)  
- Report §10: [reports/BANKING77_Report_Section_10_Structured_Tools.md](reports/BANKING77_Report_Section_10_Structured_Tools.md)  
- Demo script: [demo/E7_demo_script.md](demo/E7_demo_script.md)

## Repository layout

```text
pcam-zg516-a1-banking77/
├── notebooks/BANKING77_GenAI_Assistant.ipynb
├── data/raw/                  # pinned PolyAI train/test CSVs
├── data/eval/                 # fixed pool + pilots
├── schemas/                   # response + tool contracts
├── src/                       # tools + prompt templating
├── evidence/baseline/         # E1
├── evidence/prompts_decoding/ # E2–E3
├── evidence/structured_tools/ # E4–E5
├── evidence/evaluation/       # E6–E7 + rubric
├── reports/
├── docs/
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

| ID | Experiment | Evidence |
|----|------------|----------|
| E1 | Baseline simple prompt | `evidence/baseline/` |
| E2 | ≥4 prompt variants | `evidence/prompts_decoding/` |
| E3 | Greedy + temperature + top-k/top-p | `evidence/prompts_decoding/` |
| E4 | Structured JSON + validation | `evidence/structured_tools/` |
| E5 | ≥1 tool/function | `evidence/structured_tools/` |
| E6 | ≥3 failure cases | `evidence/evaluation/` |
| E7 | Integrated final workflow | `evidence/evaluation/` + `demo/` |

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
