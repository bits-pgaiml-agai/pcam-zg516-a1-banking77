# How to run the application and verify results

Group 15 · BANKING77 assistant · https://github.com/bits-pgaiml-agai/pcam-zg516-a1-banking77

This document explains **folder roles**, **how to run** the notebook/scripts, and **how to verify** each experiment (E1–E7).

---

## 1. Folder structure (what each path is for)

```text
pcam-zg516-a1-banking77/
├── README.md                 # Project overview + links here
├── TEAM.md                   # Active members and workstreams
├── requirements.txt          # Python deps for local / Colab helpers
│
├── notebooks/
│   ├── BANKING77_GenAI_Assistant.ipynb   # Main app + E1–E7 workflow (Colab)
│   └── BANKING77_E2_E3.ipynb             # Optional Colab helper for E2/E3
│
├── data/
│   ├── raw/                  # Pinned PolyAI train.csv / test.csv
│   └── eval/                 # Frozen subsets (seed 42); do not retune on official_test_pilot
│
├── schemas/
│   ├── response.schema.json              # Assistant JSON contract
│   └── tool_transaction_status_lookup.json
│
├── src/
│   ├── tools.py              # Mock transaction_status_lookup + dispatch_tool
│   └── prompt_template.py    # Programmatic prompt rendering
│
├── prompts/
│   ├── E2_prompt_variants.md          # short design table
│   ├── ACTUAL_PROMPTS_E2.md           # exact system/user prompts per variant
│   ├── sample_rendered_*.json         # full rendered chats (77 labels included)
│   └── assistant_template.jinja2
│
├── scripts/
│   ├── run_e2_e3.py          # E2/E3 on Hugging Face (Colab / GPU)
│   ├── run_e2_e3_ollama.py   # E2/E3 on local Ollama (default: qwen2.5:1.5b-instruct)
│   ├── run_e4_e5.py          # E4 validation + E5 tool demos
│   ├── build_group_report.py
│   └── build_demo_speaking_script.py
│
├── evidence/                 # COMMITTED results — primary place to verify
│   ├── baseline/             # E1
│   ├── prompts_decoding/     # E2–E3
│   ├── structured_tools/     # E4–E5
│   └── evaluation/           # E6–E7 rubric + failures + checklist
│
├── reports/                  # Technical report (merged + section sources)
├── docs/                     # Plans, architecture, comparison notes, this file
└── demo/                     # Demo speaking / presentation guides
```

| Path | Role |
|------|------|
| `notebooks/` | Executable application / experiments |
| `data/` | Inputs (raw + fixed eval slices) |
| `schemas/` + `src/` | Contracts and tool/prompt code |
| `scripts/` | Batch runners for E2–E5 |
| `evidence/` | Saved outputs — **use these to verify** without re-running |
| `reports/` | Written analysis for submission |
| `demo/` | How to present / what to say |

---

## 2. Shared contracts (do not change casually)

| Item | Value |
|------|--------|
| Model (official) | `Qwen/Qwen2.5-1.5B-Instruct` (pinned revision in notebook) |
| Local E2–E5 evidence | Ollama `qwen2.5:1.5b-instruct` |
| Seed | `42` |
| JSON keys | `intent`, `response`, `action_required`, `tool_name`, `tool_arguments` |
| Tool | `transaction_status_lookup` only; IDs `TXN-DEMO-###` |
| Dev design set | `data/eval/development_evaluation.csv` (40 rows) |
| Reserved test | `data/eval/official_test_pilot.csv` — **do not tune prompts on this** |

---

## 3. Setup

### 3.1 Clone

```bash
git clone https://github.com/bits-pgaiml-agai/pcam-zg516-a1-banking77.git
cd pcam-zg516-a1-banking77
pip install -r requirements.txt
```

### 3.2 Option A — Google Colab (recommended for live HF model)

1. Upload `notebooks/BANKING77_GenAI_Assistant.ipynb` to Colab.  
2. **Runtime → Change runtime type → T4 GPU**.  
3. Run cells top to bottom.  
4. Default flags (config cell):
   - `RUN_TEAM_EXPERIMENTS = False` → data prep + **E1 only**  
   - `RUN_FINAL_EVAL = False` → keep reserved test locked  

To regenerate E2–E5 inside the notebook (long): set `RUN_TEAM_EXPERIMENTS = True` and re-run from the top.  
Only after locking the prompt on development data: set `RUN_FINAL_EVAL = True`.

### 3.3 Option B — Local Ollama (matches committed E2–E5 evidence)

1. Install [Ollama](https://ollama.com) and pull the model:

```bash
ollama pull qwen2.5:1.5b-instruct
```

2. From the repo root:

```bash
# E2 + E3 (writes evidence/prompts_decoding/)
set E2_OLLAMA_MODEL=qwen2.5:1.5b-instruct
python scripts/run_e2_e3_ollama.py

# E4 + E5 (writes evidence/structured_tools/)
set E4_OLLAMA_MODEL=qwen2.5:1.5b-instruct
python scripts/run_e4_e5.py
```

On PowerShell use `$env:E2_OLLAMA_MODEL="qwen2.5:1.5b-instruct"` instead of `set`.

### 3.4 Option C — Tool-only smoke test (no LLM)

```bash
python -c "from src.tools import dispatch_tool; print(dispatch_tool('transaction_status_lookup', {'transaction_id': 'TXN-DEMO-001'}))"
```

Expected: `ok: True`, `status: pending`, `simulation: True`.

---

## 4. How to run each experiment

| Experiment | How to run | Writes / shows |
|------------|------------|----------------|
| **E1** Baseline | Colab notebook, default flags | `evidence/baseline/` (or notebook `banking77_baseline_outputs/`) |
| **E2** Prompt variants | `python scripts/run_e2_e3_ollama.py` **or** Colab with `RUN_TEAM_EXPERIMENTS=True` | `evidence/prompts_decoding/E2_*` |
| **E3** Decoding | Same as E2 (script continues into E3) | `evidence/prompts_decoding/E3_*` |
| **E4** Schema validation | `python scripts/run_e4_e5.py` **or** notebook E4 cells | `evidence/structured_tools/E4_*` |
| **E5** Tool calling | Same `run_e4_e5.py` / notebook tool cells | `evidence/structured_tools/E5_*` |
| **E6** Failures | Analysis table (manual + E1 observations) | `evidence/evaluation/E6_failure_analysis.csv` |
| **E7** Integration | Notebook end-to-end + checklist | `evidence/evaluation/E7_integration_checklist.md`, `demo/` |

**Demo tip:** For an 8–10 minute presentation, run Colab for E1 + live `dispatch_tool`, and open committed files under `evidence/` for E2–E6. See [demo/HOW_TO_PRESENT_DEMO.md](../demo/HOW_TO_PRESENT_DEMO.md).

---

## 5. How to verify results

Open the files below. You should see the stated checks without re-running.

### E1 — Baseline

| File | What to check |
|------|----------------|
| `evidence/baseline/E1_summary.json` | `n=3`, `schema_valid=0`, `intent_correct=0`, `general_accuracy_claim=false` |
| `evidence/baseline/E1_baseline_outputs.jsonl` | Three raw generations; validation errors present |
| `evidence/baseline/environment.json` | Model / runtime recorded |

### E2 — Prompt comparison

| File | What to check |
|------|----------------|
| `evidence/prompts_decoding/E2_summary.json` | Four variants; best by JSON then intent = `zero_shot` |
| `evidence/prompts_decoding/E2_prompt_comparison.csv` | Table of rates |
| `evidence/prompts_decoding/environment.json` | `ollama_model`: `qwen2.5:1.5b-instruct` |
| `prompts/ACTUAL_PROMPTS_E2.md` | Exact Task lines + shared OUTPUT_RULES for each variant |
| `prompts/sample_rendered_*.json` | Full messages that were sent (system + user, 77 labels) |

**Primary local numbers (n=10):** zero_shot JSON valid **0.60**, validated intent **0.10**.

### E3 — Decoding

| File | What to check |
|------|----------------|
| `evidence/prompts_decoding/E3_summary.json` | Prompt = `zero_shot`; greedy / top-k / top-p rows |
| `evidence/prompts_decoding/E3_decoding_summary.csv` | Prefer greedy for structured JSON |

### E4 — Structured output

| File | What to check |
|------|----------------|
| `schemas/response.schema.json` | Five required keys |
| `evidence/structured_tools/E4_summary.json` | `expectation_matches` = **10** of `n_designed` = **10** |
| `evidence/structured_tools/E4_validation_cases.csv` | Accept/reject cases |

### E5 — Tool / function

| File | What to check |
|------|----------------|
| `src/tools.py` | Mock table + allowlist |
| `evidence/structured_tools/E5_tool_invocations.csv` | TXN-DEMO-001 ok; bad ID / wrong tool rejected |
| `evidence/structured_tools/E5_integrated_tool_demo.json` | Invalid LLM JSON → `tool_result` null (blocked) |
| `evidence/structured_tools/E5_representative_valid_pipeline.json` | Valid path → mock status + simulation disclosed |

### E6 — Failure analysis

| File | What to check |
|------|----------------|
| `evidence/evaluation/E6_failure_analysis.csv` | At least F1–F3 (observed); F4–F6 designed controls |

### E7 — Integrated workflow

| File | What to check |
|------|----------------|
| `evidence/evaluation/E7_integration_checklist.md` | End-to-end steps + demo acceptance list |
| `evidence/evaluation/eval_rubric.json` | Criteria C1–C5 reported separately |
| `demo/E7_demo_script.md` | Timing / speakers |

### Quick verification commands

```bash
# Summaries
python -c "import json; from pathlib import Path
print('E1', json.load(open('evidence/baseline/E1_summary.json')))
print('E2 best', json.load(open('evidence/prompts_decoding/E2_summary.json'))['best_variant_by_json_then_intent'])
print('E4', json.load(open('evidence/structured_tools/E4_summary.json')))
"

# Tool smoke test
python -c "from src.tools import dispatch_tool
print(dispatch_tool('transaction_status_lookup', {'transaction_id':'TXN-DEMO-001'}))
print(dispatch_tool('transaction_status_lookup', {'transaction_id':'TXN-999'}))
"
```

---

## 6. Metrics rules (when reading results)

1. Report **intent**, **schema**, **safety**, and **tool** separately — never one unsupported “accuracy”.  
2. Always state **n** and whether the split is development or reserved test.  
3. E1 n=3 is observational only (`general_accuracy_claim` must stay false).  
4. E2 n=10 / E3 n=3 on local 1.5b-instruct do **not** claim 77-class performance.  
5. Do not tune on `official_test_pilot.csv`.

---

## 7. Safety

Use only public BANKING77 text and mock `TXN-DEMO-###` tools. Do not use real banking credentials, account numbers, PINs, OTPs, or personal financial data.
