# pcam-zg516-a1-banking77

**BITS Pilani WILP · PGAIML · PCAM\* ZG516 Applied Generative AI**  
**Group Major Project / Assignment-1 · Dataset D1: BANKING77**

Banking customer-service assistant: intent understanding + safe response generation + structured JSON + simulated tool calling, using a pretrained Hugging Face causal LLM (prompting-focused; no training from scratch).

---

## Results

> **Primary reported runtime:** Ollama `qwen2.5:1.5b-instruct` (aligned to HF pin `Qwen/Qwen2.5-1.5B-Instruct`) · seed **42** · simulation only  
> **Adaptation choice:** prompting only (no fine-tuning / no RAG corpus)  
> **Demo video:** [Google Drive](https://drive.google.com/file/d/1Dohvy0xKWXzJqEOCO_tHSFkhXZA9JHUY/view?usp=drive_link)

### What we achieved (E1–E7)

| Experiment | Headline result (primary 1.5b-instruct) | Where to verify |
|------------|----------------------------------------|-----------------|
| **E1 Baseline** | Weak baseline: **0/3** schema-valid, **0/3** intent-correct (n=3; observational only) | [E1_summary.json](evidence/baseline/E1_summary.json) |
| **E2 Prompts** | Best variant = **`zero_shot`** → JSON valid **0.60**, validated intent **0.10** (n=10) | [E2_summary.json](evidence/prompts_decoding/E2_summary.json) |
| **E3 Decoding** | Prefer **greedy** for structured JSON (vs temp+top-k / top-p; n=3) | [E3_summary.json](evidence/prompts_decoding/E3_summary.json) |
| **E4 Schema** | Designed validation **10/10** | [E4_summary.json](evidence/structured_tools/E4_summary.json) |
| **E5 Tools** | Allowlisted mock `transaction_status_lookup` (`TXN-DEMO-###`); invalid JSON **never** reaches the tool | [E5_tool_invocations.csv](evidence/structured_tools/E5_tool_invocations.csv) |
| **E6 Failures** | ≥3 analyzed failures (fence/invented intent/unsafe ask) + designed controls | [E6_failure_analysis.csv](evidence/evaluation/E6_failure_analysis.csv) |
| **E7 Integration** | End-to-end path: prompt → generate → validate → tool/fallback | [E7_integration_checklist.md](evidence/evaluation/E7_integration_checklist.md) |

**Locked production-style choices after experiments:** prompt = **`zero_shot`**, decoding = **greedy**, then schema validation + allowlisted tool.

### Comparison: `qwen2.5:1.5b-instruct` (primary) vs `qwen2.5:3b` (exploratory)

Same protocol (E2 n=10, E3 n=3, seed 42). Full write-up: [docs/MODEL_COMPARISON_OLLAMA.md](docs/MODEL_COMPARISON_OLLAMA.md).

**E2 — JSON valid / validated intent**

| Variant | **1.5b-instruct (primary)** | 3b (exploratory) |
|---------|-----------------------------|------------------|
| zero_shot | **0.60 / 0.10** ← best on primary | 0.50 / 0.20 |
| few_shot | 0.30 / 0.10 | 0.60 / 0.30 |
| role_context | 0.30 / 0.10 | **0.70 / 0.20** ← best on 3b |
| constraint_based | 0.10 / 0.00 | 0.60 / 0.30 |

**E3 — JSON valid / intent correct**

| Decoding | 1.5b-instruct (prompt=`zero_shot`) | 3b (prompt=`constraint_based`) |
|----------|------------------------------------|--------------------------------|
| greedy | **0.33 / 0.00** | **0.67 / 0.33** |
| T=0.7 + top-k=50 | 0.00 / 0.00 | 0.67 / 0.33 |
| T=0.7 + top-p=0.9 | 0.33 / 0.00 | 0.33 / 0.33 |

### Conclusion (what to take away)

1. **We completed the full E1–E7 assignment path** with committed evidence, a merged technical report, and a recorded demo.  
2. **Primary figures use 1.5b-instruct** to match the official HF size/family pin — even though **3b scored higher** on schema/intent under the same design.  
3. On the primary model, **shorter prompts win**: `zero_shot` beat few-shot / role / constraint; longer prompts helped 3b but hurt 1.5b.  
4. **Greedy decoding** is preferred for JSON. **E4 is 10/10** and the **tool path is safe** (invalid JSON blocked).  
5. Intent accuracy on 1.5b remains **low** (honest limit of a small prompted model on 77 labels; metrics reported separately — no inflated single “accuracy”).  
6. System is a **simulation** only (mock `TXN-DEMO-###`); not a real banking system.

---

## Quick index

| Need | Link |
|------|------|
| GitHub repo | [bits-pgaiml-agai/pcam-zg516-a1-banking77](https://github.com/bits-pgaiml-agai/pcam-zg516-a1-banking77) |
| Demo video (Google Drive) | [Group 15 BANKING77 demo](https://drive.google.com/file/d/1Dohvy0xKWXzJqEOCO_tHSFkhXZA9JHUY/view?usp=drive_link) |
| Video link file | [demo/VIDEO_LINK.txt](demo/VIDEO_LINK.txt) |
| Team roster | [TEAM.md](TEAM.md) |
| Run & verify (full guide) | [docs/RUN_AND_VERIFY.md](docs/RUN_AND_VERIFY.md) |
| Main notebook | [notebooks/BANKING77_GenAI_Assistant.ipynb](notebooks/BANKING77_GenAI_Assistant.ipynb) |
| Exact E2 prompts | [prompts/ACTUAL_PROMPTS_E2.md](prompts/ACTUAL_PROMPTS_E2.md) |
| Merged technical report | [reports/BANKING77_Group15_Technical_Report.docx](reports/BANKING77_Group15_Technical_Report.docx) |
| Requirements | [requirements.txt](requirements.txt) |

### Evidence by experiment

| ID | Open |
|----|------|
| E1 | [evidence/baseline/E1_summary.json](evidence/baseline/E1_summary.json) |
| E2 | [evidence/prompts_decoding/E2_summary.json](evidence/prompts_decoding/E2_summary.json) · [E2_prompt_comparison.csv](evidence/prompts_decoding/E2_prompt_comparison.csv) |
| E3 | [evidence/prompts_decoding/E3_summary.json](evidence/prompts_decoding/E3_summary.json) · [E3_decoding_summary.csv](evidence/prompts_decoding/E3_decoding_summary.csv) |
| E4 | [evidence/structured_tools/E4_summary.json](evidence/structured_tools/E4_summary.json) |
| E5 | [evidence/structured_tools/E5_tool_invocations.csv](evidence/structured_tools/E5_tool_invocations.csv) · [E5_integrated_tool_demo.json](evidence/structured_tools/E5_integrated_tool_demo.json) |
| E6 | [evidence/evaluation/E6_failure_analysis.csv](evidence/evaluation/E6_failure_analysis.csv) |
| E7 | [evidence/evaluation/E7_integration_checklist.md](evidence/evaluation/E7_integration_checklist.md) |

### All important docs

| Area | Links |
|------|-------|
| Docs | [RUN_AND_VERIFY.md](docs/RUN_AND_VERIFY.md) · [MODEL_COMPARISON_OLLAMA.md](docs/MODEL_COMPARISON_OLLAMA.md) · [ARCHITECTURE.md](docs/evaluation/ARCHITECTURE.md) · [baseline/HANDOFF.txt](docs/baseline/HANDOFF.txt) · [evaluation/HANDOFF.txt](docs/evaluation/HANDOFF.txt) |
| Prompts | [ACTUAL_PROMPTS_E2.md](prompts/ACTUAL_PROMPTS_E2.md) · [E2_prompt_variants.md](prompts/E2_prompt_variants.md) · [assistant_template.jinja2](prompts/assistant_template.jinja2) · [sample_rendered_zero_shot.json](prompts/sample_rendered_zero_shot.json) · [few_shot](prompts/sample_rendered_few_shot.json) · [role_context](prompts/sample_rendered_role_context.json) · [constraint_based](prompts/sample_rendered_constraint_based.json) |
| Schemas / code | [response.schema.json](schemas/response.schema.json) · [tool schema](schemas/tool_transaction_status_lookup.json) · [src/tools.py](src/tools.py) · [src/prompt_template.py](src/prompt_template.py) |
| Scripts | [run_e2_e3_ollama.py](scripts/run_e2_e3_ollama.py) · [run_e2_e3.py](scripts/run_e2_e3.py) · [run_e4_e5.py](scripts/run_e4_e5.py) · [build_group_report.py](scripts/build_group_report.py) |
| Reports | [Technical Report.docx](reports/BANKING77_Group15_Technical_Report.docx) · [§§4–5,9,11–13](reports/BANKING77_Report_Sections_4_5_9_11_12_13_Architecture_Eval.md) · [§§7–8](reports/BANKING77_Report_Sections_7_8_Prompts_Decoding.md) · [§10](reports/BANKING77_Report_Section_10_Structured_Tools.md) · [§§2,3,6.docx](reports/BANKING77_Report_Sections_2_3_6_Problem_Dataset_Baseline.docx) |
| Demo | [VIDEO_LINK.txt](demo/VIDEO_LINK.txt) — [Google Drive video](https://drive.google.com/file/d/1Dohvy0xKWXzJqEOCO_tHSFkhXZA9JHUY/view?usp=drive_link) |
| Data | [data/raw/README.md](data/raw/README.md) · [data/eval/README.md](data/eval/README.md) · [development_evaluation.csv](data/eval/development_evaluation.csv) |
| Notebooks | [BANKING77_GenAI_Assistant.ipynb](notebooks/BANKING77_GenAI_Assistant.ipynb) · [BANKING77_E2_E3.ipynb](notebooks/BANKING77_E2_E3.ipynb) |

## Team

See [TEAM.md](TEAM.md). Group 15 (3 active members).

## Status

| Workstream | Owner | Status |
|------------|-------|--------|
| Data prep + E1 baseline + notebook | Anil | Done — [evidence/baseline/](evidence/baseline/) |
| E2 prompts + E3 decoding | Venkat | Done — [evidence/prompts_decoding/](evidence/prompts_decoding/) |
| E4 schema + E5 tools + templates | Nisha | Done — [evidence/structured_tools/](evidence/structured_tools/) |
| Architecture, adaptation, E6/E7 eval | Venkat | Done — [evidence/evaluation/](evidence/evaluation/) |

## Start here: run & verify

**Full guide:** [docs/RUN_AND_VERIFY.md](docs/RUN_AND_VERIFY.md) — folder meanings, how to run Colab / Ollama / tools, and how to check each experiment’s evidence files.

**Demo video (Google Drive):** [watch / download](https://drive.google.com/file/d/1Dohvy0xKWXzJqEOCO_tHSFkhXZA9JHUY/view?usp=drive_link) · [demo/VIDEO_LINK.txt](demo/VIDEO_LINK.txt)

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
├── demo/                      # Demo video link
├── requirements.txt
├── TEAM.md
└── README.md
```

| Folder | Purpose |
|--------|---------|
| [notebooks/](notebooks/) | Executable assistant / experiments |
| [data/](data/) | Dataset inputs and fixed eval slices |
| [schemas/](schemas/) + [src/](src/) | Output/tool contracts and code |
| [scripts/](scripts/) | Re-run E2–E5 without the full notebook |
| [evidence/](evidence/) | **Committed results — verify here first** |
| [reports/](reports/) | Written report for submission |
| [docs/](docs/) | Design notes + [RUN_AND_VERIFY.md](docs/RUN_AND_VERIFY.md) |
| [demo/](demo/) | Demo video link |

---

## Shared contracts

- **Model (official):** `Qwen/Qwen2.5-1.5B-Instruct` (pinned revision in notebook)  
- **Local E2–E5 evidence:** Ollama `qwen2.5:1.5b-instruct`  
- **JSON keys:** `intent`, `response`, `action_required`, `tool_name`, `tool_arguments`  
- **Tool:** `transaction_status_lookup` with `TXN-DEMO-###` ids only  
- **Seed:** 42  
- **Dev set:** [data/eval/development_evaluation.csv](data/eval/development_evaluation.csv) (40) — do **not** tune on [official_test_pilot.csv](data/eval/official_test_pilot.csv)

---

## How to run

### 1) Clone and install

```bash
git clone https://github.com/bits-pgaiml-agai/pcam-zg516-a1-banking77.git
cd pcam-zg516-a1-banking77
pip install -r requirements.txt
```

### 2) Google Colab (recommended for live HF model)

1. Upload [notebooks/BANKING77_GenAI_Assistant.ipynb](notebooks/BANKING77_GenAI_Assistant.ipynb)  
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
| **E1** | [E1_summary.json](evidence/baseline/E1_summary.json) | n=3; schema_valid=0; intent_correct=0 |
| **E2** | [E2_summary.json](evidence/prompts_decoding/E2_summary.json) | Best variant `zero_shot`; JSON ~0.60 (n=10) |
| **E3** | [E3_summary.json](evidence/prompts_decoding/E3_summary.json) | Greedy preferred for JSON |
| **E4** | [E4_summary.json](evidence/structured_tools/E4_summary.json) | 10/10 designed cases |
| **E5** | [E5_tool_invocations.csv](evidence/structured_tools/E5_tool_invocations.csv), [E5_integrated_tool_demo.json](evidence/structured_tools/E5_integrated_tool_demo.json) | Mock OK; invalid JSON blocks tool |
| **E6** | [E6_failure_analysis.csv](evidence/evaluation/E6_failure_analysis.csv) | ≥3 failure cases (F1–F3+) |
| **E7** | [E7_integration_checklist.md](evidence/evaluation/E7_integration_checklist.md) + [demo/](demo/) | End-to-end path documented |

Quick check:

```bash
python -c "import json; print(json.load(open('evidence/baseline/E1_summary.json'))); print(json.load(open('evidence/prompts_decoding/E2_summary.json'))['best_variant_by_json_then_intent']); print(json.load(open('evidence/structured_tools/E4_summary.json')))"
```

Details and more commands: [docs/RUN_AND_VERIFY.md](docs/RUN_AND_VERIFY.md).

---

## Required experiments

| ID | Experiment | Evidence |
|----|------------|----------|
| E1 | Baseline simple prompt | [evidence/baseline/](evidence/baseline/) |
| E2 | ≥4 prompt variants | [evidence/prompts_decoding/](evidence/prompts_decoding/) |
| E3 | Greedy + temperature + top-k/top-p | [evidence/prompts_decoding/](evidence/prompts_decoding/) |
| E4 | Structured JSON + validation | [evidence/structured_tools/](evidence/structured_tools/) |
| E5 | ≥1 tool/function | [evidence/structured_tools/](evidence/structured_tools/) |
| E6 | ≥3 failure cases | [evidence/evaluation/](evidence/evaluation/) |
| E7 | Integrated final workflow | [evidence/evaluation/](evidence/evaluation/) + [demo/](demo/) |

## Safety

Use only public BANKING77 text and mock tool backends. Do not use real banking credentials, account numbers, or personal financial data.
