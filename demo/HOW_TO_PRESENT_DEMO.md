# How to present the Group 15 demo

**Project:** BANKING77 banking assistant  
**Target length:** 8–10 minutes  
**Speaking lines:** `Group15_Demo_Speaking_Script.docx`  
**Repo:** https://github.com/bits-pgaiml-agai/pcam-zg516-a1-banking77

---

## Recommended approach: hybrid

Use **Google Colab** for a short live run (E1 + tool), and show **committed evidence** for E2–E5 results. That is the most reliable demo.

| Mode | Use for | Risk |
|------|---------|------|
| **Colab T4** (preferred live) | Notebook open, E1 cells, `dispatch_tool` live | HF download / queue can be slow |
| **Committed evidence** (always ready) | E2/E3 tables, E4 10/10, E5 tool CSV, E6 failures | None — already in repo |
| **Local only** | Backup if Colab fails | CPU slow; Ollama results already saved |

Do **not** set `RUN_TEAM_EXPERIMENTS=True` during the live demo (full E2–E5 regen takes too long). Show those results from `evidence/`.

---

## Before the recording (day before)

1. Open repo: https://github.com/bits-pgaiml-agai/pcam-zg516-a1-banking77  
2. Upload `notebooks/BANKING77_GenAI_Assistant.ipynb` to Google Colab  
3. **Runtime → Change runtime type → T4 GPU**  
4. Keep flags:
   - `RUN_TEAM_EXPERIMENTS = False`
   - `RUN_FINAL_EVAL = False`
5. Run top cells once so the model is cached (or accept using evidence if download is slow)  
6. Keep these folders ready in a second tab / File Explorer:
   - `evidence/baseline/`
   - `evidence/prompts_decoding/`
   - `evidence/structured_tools/`
   - `evidence/evaluation/`  
7. Rehearse from `Group15_Demo_Speaking_Script.docx`

---

## Minute-by-minute: what to show on screen

### 0:00–0:45 — Intro (Venkat or Anil)

- Screen: README or title  
- Say: problem, prompting-only, simulation, not a real bank  

### 0:45–2:15 — Anil (data + E1)

**Show in Colab (or evidence if Colab is cold):**

1. Config cell — seed 42, model name, flags False  
2. Data/subset cells — `development_evaluation.csv` (40) vs reserved test  
3. E1 results:
   - Live: run E1 cell if ready, **or**
   - File: `evidence/baseline/E1_summary.json` → **0/3 schema, 0/3 intent**  
   - File: one bad line in `E1_baseline_outputs.jsonl` (Markdown / invented label / card ask)

### 2:15–4:15 — Venkat (E2 + E3) — evidence, not live regen

Open:

1. `evidence/prompts_decoding/E2_prompt_comparison.csv` or `E2_summary.json`  
   - Four variants, n=10; best **zero_shot** JSON **0.60**, intent **0.10**  
2. Optional: `prompts/ACTUAL_PROMPTS_E2.md` or one `prompts/sample_rendered_*.json` — show the exact Task line / few-shot block  
3. `E3_decoding_summary.csv` / `E3_summary.json`  
   - Prefer **greedy** for structured JSON  
4. Optional one line: `docs/MODEL_COMPARISON_OLLAMA.md` (3b stronger; we standardize on 1.5b-instruct)

### 4:15–5:45 — Nisha (E4 + E5)

1. `schemas/response.schema.json` — five keys  
2. `evidence/structured_tools/E4_summary.json` — **10/10**  
3. **Live in Colab** (tool cell works without full LLM wait):

```python
dispatch_tool("transaction_status_lookup", {"transaction_id": "TXN-DEMO-001"})
dispatch_tool("transaction_status_lookup", {"transaction_id": "TXN-999"})
```

4. Optional: `E5_integrated_tool_demo.json` — invalid LLM JSON blocked the tool  

### 5:45–8:30 — Venkat (architecture, E6, E7)

1. Architecture: prompt → generate → validate → tool/fallback  
2. `evidence/evaluation/E6_failure_analysis.csv` — F1, F2, F3  
3. State four metrics separately: intent, schema, safety, tool  
4. `evidence/evaluation/E7_integration_checklist.md`  

### 8:30–10:00 — Close

- Simulation only; small n; no full 77-class claim; Q&A  

---

## Colab vs local — clear choice

**Use Colab if** you can get T4 and finish install + model load before recording.  
**Use evidence-first if** Colab is slow, HF download fails, or you have a hard 10-minute stop.

Local tool-only backup:

```bash
cd pcam-zg516-a1-banking77
python -c "from src.tools import dispatch_tool; print(dispatch_tool('transaction_status_lookup', {'transaction_id':'TXN-DEMO-001'}))"
```

---

## What NOT to do live

- Do not re-run full E2 or E3 during the video  
- Do not enable `RUN_FINAL_EVAL`  
- Do not invent better accuracy than the JSON/CSV summaries  
- Do not show real personal or financial data  

---

## Full backup if live fails

Share screen on the GitHub repo or submission folder and walk:

`E1_summary.json` → `E2_summary.json` → `E3_summary.json` → `E4_summary.json` → `E5_tool_invocations.csv` → `E6_failure_analysis.csv`

That still shows experiments and results using committed evidence.

---

## Demo acceptance checklist

- [ ] Failing E1 raw output / validator rejection  
- [ ] E2 comparison numbers  
- [ ] E3 decoding table  
- [ ] Schema + tool success `TXN-DEMO-001`  
- [ ] Tool rejection on bad ID  
- [ ] Four metrics stated separately  
- [ ] Say: simulation / no real bank credentials  
