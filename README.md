# pcam-zg516-a1-banking77

**BITS Pilani WILP · PGAIML · PCAM\* ZG516 Applied Generative AI**  
**Group Major Project / Assignment-1 · Dataset D1: BANKING77**

Banking customer-service assistant: intent understanding + safe response generation + structured JSON + simulated tool calling, using a pretrained Hugging Face causal LLM (prompting-focused; no training from scratch).

## Team

See [TEAM.md](TEAM.md). Group 15 (3 active members).

## Status

| Workstream | Owner | Status |
|------------|-------|--------|
| Data prep + E1 baseline + notebook | Anil | Done — `evidence/baseline/` |
| E2 prompts + E3 decoding | Venkat | Done — `evidence/prompts_decoding/` |
| E4 schema + E5 tools + templates | Nisha | Done — `evidence/structured_tools/` |
| Architecture, adaptation, E6/E7 eval | Venkat | Done — `evidence/evaluation/` |

## Start here: run & verify

**Full guide:** [docs/RUN_AND_VERIFY.md](docs/RUN_AND_VERIFY.md) — folder meanings, how to run Colab / Ollama / tools, and how to check each experiment’s evidence files.

**Demo presentation:** [demo/HOW_TO_PRESENT_DEMO.md](demo/HOW_TO_PRESENT_DEMO.md) · [demo/Group15_Demo_Speaking_Script.docx](demo/Group15_Demo_Speaking_Script.docx)

---

## Repository layout

```text
pcam-zg516-a1-banking77/
├── notebooks/                 # Main Colab app + optional E2/E3 helper
│   └── BANKING77_GenAI_Assistant.ipynb
├── data/
│   ├── raw/                   # Pinned PolyAI train/test CSVs
│   └── eval/                  # Frozen subsets (seed 42)
├── schemas/                   # Response + tool JSON contracts
├── src/                       # tools.py, prompt_template.py
├── prompts/                   # E2 variant notes, exact rendered prompts, Jinja template
├── scripts/                   # Batch runners (E2–E5, report builders)
├── evidence/
│   ├── baseline/              # E1 results
│   ├── prompts_decoding/      # E2–E3 results
│   ├── structured_tools/      # E4–E5 results
│   └── evaluation/            # E6–E7 rubric, failures, checklist
├── reports/                   # Technical report (merged Word + sections)
├── docs/                      # Architecture, comparison, RUN_AND_VERIFY
├── demo/                      # Demo timing + speaking + how-to-present
├── requirements.txt
├── TEAM.md
└── README.md
```

| Folder | Purpose |
|--------|---------|
| `notebooks/` | Executable assistant / experiments |
| `data/` | Dataset inputs and fixed eval slices |
| `schemas/` + `src/` | Output/tool contracts and code |
| `scripts/` | Re-run E2–E5 without the full notebook |
| `evidence/` | **Committed results — verify here first** |
| `reports/` | Written report for submission |
| `docs/` | Design notes + [RUN_AND_VERIFY.md](docs/RUN_AND_VERIFY.md) |
| `demo/` | Presentation guides |

---

## Shared contracts

- **Model (official):** `Qwen/Qwen2.5-1.5B-Instruct` (pinned revision in notebook)  
- **Local E2–E5 evidence:** Ollama `qwen2.5:1.5b-instruct`  
- **JSON keys:** `intent`, `response`, `action_required`, `tool_name`, `tool_arguments`  
- **Tool:** `transaction_status_lookup` with `TXN-DEMO-###` ids only  
- **Seed:** 42  
- **Dev set:** `data/eval/development_evaluation.csv` (40) — do **not** tune on `official_test_pilot.csv`

---

## How to run

### 1) Clone and install

```bash
git clone https://github.com/bits-pgaiml-agai/pcam-zg516-a1-banking77.git
cd pcam-zg516-a1-banking77
pip install -r requirements.txt
```

### 2) Google Colab (recommended for live HF model)

1. Upload `notebooks/BANKING77_GenAI_Assistant.ipynb`  
2. **Runtime → T4 GPU**  
3. Keep `RUN_TEAM_EXPERIMENTS=False` and `RUN_FINAL_EVAL=False` for a fast **E1** run  
4. Set `RUN_TEAM_EXPERIMENTS=True` only when you intentionally want notebook E2–E5 (slow)  
5. Set `RUN_FINAL_EVAL=True` only after locking the prompt on development data  

### 3) Local Ollama (matches committed E2–E5)

```bash
ollama pull qwen2.5:1.5b-instruct

# PowerShell
$env:E2_OLLAMA_MODEL="qwen2.5:1.5b-instruct"
python scripts/run_e2_e3_ollama.py

$env:E4_OLLAMA_MODEL="qwen2.5:1.5b-instruct"
python scripts/run_e4_e5.py
```

### 4) Tool smoke test (no LLM)

```bash
python -c "from src.tools import dispatch_tool; print(dispatch_tool('transaction_status_lookup', {'transaction_id': 'TXN-DEMO-001'}))"
```

---

## How to verify results (without re-running)

| Experiment | Open these files | Expect |
|------------|------------------|--------|
| **E1** | `evidence/baseline/E1_summary.json` | n=3; schema_valid=0; intent_correct=0 |
| **E2** | `evidence/prompts_decoding/E2_summary.json` | Best variant `zero_shot`; JSON ~0.60 (n=10) |
| **E3** | `evidence/prompts_decoding/E3_summary.json` | Greedy preferred for JSON |
| **E4** | `evidence/structured_tools/E4_summary.json` | 10/10 designed cases |
| **E5** | `E5_tool_invocations.csv`, `E5_integrated_tool_demo.json` | Mock OK; invalid JSON blocks tool |
| **E6** | `evidence/evaluation/E6_failure_analysis.csv` | ≥3 failure cases (F1–F3+) |
| **E7** | `E7_integration_checklist.md` + `demo/` | End-to-end path documented |

Quick check:

```bash
python -c "import json; print(json.load(open('evidence/baseline/E1_summary.json'))); print(json.load(open('evidence/prompts_decoding/E2_summary.json'))['best_variant_by_json_then_intent']); print(json.load(open('evidence/structured_tools/E4_summary.json')))"
```

Details and more commands: [docs/RUN_AND_VERIFY.md](docs/RUN_AND_VERIFY.md).

---

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

## Key documents

- [docs/RUN_AND_VERIFY.md](docs/RUN_AND_VERIFY.md) — **run + verify**  
- [prompts/ACTUAL_PROMPTS_E2.md](prompts/ACTUAL_PROMPTS_E2.md) — **exact E2 prompts** sent to the LLM (+ `sample_rendered_*.json`)  
- [prompts/E2_prompt_variants.md](prompts/E2_prompt_variants.md) — short variant design table  
- [reports/BANKING77_Group15_Technical_Report.docx](reports/BANKING77_Group15_Technical_Report.docx) — merged report  
- [docs/MODEL_COMPARISON_OLLAMA.md](docs/MODEL_COMPARISON_OLLAMA.md) — 1.5b-instruct vs exploratory 3b  
- [demo/HOW_TO_PRESENT_DEMO.md](demo/HOW_TO_PRESENT_DEMO.md) — how to present  
- [docs/baseline/HANDOFF.txt](docs/baseline/HANDOFF.txt) · [docs/evaluation/HANDOFF.txt](docs/evaluation/HANDOFF.txt)

## Safety

Use only public BANKING77 text and mock tool backends. Do not use real banking credentials, account numbers, or personal financial data.
