# BANKING77 Report Sections

**Author:** Venkata Srinivasa Rao Tunuguntla (Group 15)  
**Scope:** Assignment report §§7–8 (prompt engineering + decoding)  
**Evidence:** [`evidence/prompts_decoding/`](../evidence/prompts_decoding/)

## Runtime note

Primary group contract remains Hugging Face `Qwen/Qwen2.5-1.5B-Instruct` (Baseline).  
This Prompt/decoding evidence run used **local Ollama `qwen2.5:1.5b-instruct`** (same family/size as the HF pin; Ollama tag `qwen2.5:1.5b` shares the same local digest). The prompt/decoding protocol matches the shared notebook. Re-run [`scripts/run_e2_e3.py`](../scripts/run_e2_e3.py) on **Colab T4** with the pinned HF model before final submission if the instructor requires identical checkpoint to E1.

An exploratory side-by-side with local `qwen2.5:3b` (higher schema/intent rates, different best prompt) is documented in [`docs/MODEL_COMPARISON_OLLAMA.md`](../docs/MODEL_COMPARISON_OLLAMA.md). **Primary figures in this report are 1.5b-instruct only.**

---

## 7. Prompt-engineering experiments (E2)

### 7.1 Design

| Item | Choice |
|------|--------|
| Variants (4) | `zero_shot`, `few_shot`, `role_context`, `constraint_based` |
| Shared rules | Exact 77-label list + JSON contract + privacy rules |
| Few-shot | 4 fixed examples from [`data/eval/in_prompt_examples.csv`](../data/eval/in_prompt_examples.csv) |
| Evaluation subset | 10 rows from `development_evaluation.csv`, seed 42 (same rows for all variants) |
| Decoding for E2 | Greedy / temperature 0 (stable comparison) |
| Metrics | Schema validity, validated intent correctness, intent accuracy, macro-F1 on represented labels |
| Runtime | Ollama `qwen2.5:1.5b-instruct` |

Baseline E1 (Baseline) used a simpler `baseline` prompt and scored **0/3** schema-valid on its three examples — a separate observational baseline, not part of this four-variant table.

### 7.2 Results (n=10 development subset)

| Variant | JSON valid rate | Intent correct (validated) | Intent accuracy (label string) | Mean latency (s) |
|---------|-----------------|----------------------------|--------------------------------|------------------|
| **zero_shot** | **0.60** | **0.10** | **0.10** | 8.3 |
| few_shot | 0.30 | 0.10 | 0.10 | 6.6 |
| role_context | 0.30 | 0.10 | 0.10 | 8.4 |
| constraint_based | 0.10 | 0.00 | 0.00 | 9.7 |

**Observations**

1. All improved prompts beat E1’s 0% schema acceptance on at least some rows; **zero_shot** was strongest on this 1.5B instruct local run (**0.60** JSON valid).  
2. Validated intent correctness remained low (**0.10** best) — the 1.5B local model often invents labels or breaks the action/tool contract even when JSON parses.  
3. Longer constraint / role prompts did **not** help this small local checkpoint; they reduced schema validity vs zero-shot.  
4. Remaining failures are mostly Markdown fences, invented labels, or action/tool inconsistencies — same classes as E1 F1–F3.  
5. n=10 covers 10 intents only; do not claim 77-class performance.

### 7.3 Recommended improved prompt for later stages

For this **`qwen2.5:1.5b-instruct`** evidence pack, lock **`zero_shot`** (best by JSON then intent). Keep constraint/few-shot wording available for Colab HF re-runs, where longer instructions may behave differently.

Files: [`E2_prompt_comparison.csv`](../evidence/prompts_decoding/E2_prompt_comparison.csv), `E2_*.csv`, [`E2_summary.json`](../evidence/prompts_decoding/E2_summary.json).  
Exact prompts sent to the model: [`prompts/ACTUAL_PROMPTS_E2.md`](../prompts/ACTUAL_PROMPTS_E2.md) and `prompts/sample_rendered_*.json`.

---

## 8. Decoding experiments (E3)

### 8.1 Design

| Item | Choice |
|------|--------|
| Prompt | `zero_shot` (best E2 variant on this runtime) |
| Settings | greedy (T=0); T=0.7 + top-k=50; T=0.7 + top-p=0.9 |
| Rows | 3 utterances from the E2 subset (seed 43) |

### 8.2 Results (n=3 × 3 settings, `zero_shot`)

| Decoding | JSON valid rate | Intent correct rate | Mean latency (s) |
|----------|-----------------|---------------------|------------------|
| greedy (T=0) | **0.33** | 0.00 | 6.3 |
| T=0.7 + top-k=50 | 0.00 | 0.00 | 5.9 |
| T=0.7 + top-p=0.9 | **0.33** | 0.00 | 5.8 |

**Observations**

- On this tiny sample, **greedy** and **top-p** tied on schema validity (0.33); **top-k** produced no valid JSON.  
- Intent correctness was **0** across settings (n=3 is observational only).  
- For production-like JSON, keep **greedy** after locking the prompt; retain the sampling rows as the required decoding study.

Files: [`E3_decoding.csv`](../evidence/prompts_decoding/E3_decoding.csv), [`E3_decoding_summary.csv`](../evidence/prompts_decoding/E3_decoding_summary.csv), [`E3_summary.json`](../evidence/prompts_decoding/E3_summary.json).

---

## Contribution statement

I, Venkata Srinivasa Rao Tunuguntla, am responsible for prompt-engineering experiments (E2: ≥4 variants with comparison table), decoding study (E3: greedy vs temperature + top-k/top-p), the prompt experiment log, and report sections 7–8 (in addition to architecture/evaluation sections listed elsewhere). I will explain these experiments in the group demonstration.

Member confirmation/signature: ____________________  Date: _______________
