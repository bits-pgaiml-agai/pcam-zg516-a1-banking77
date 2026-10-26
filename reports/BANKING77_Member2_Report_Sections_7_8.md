# BANKING77 Member 2 Report Sections

**Author:** Takkars Bhavani (Group 15) · executed with team support  
**Scope:** Assignment report §§7–8 (prompt engineering + decoding)  
**Evidence:** `evidence/member2/`

## Runtime note

Primary group contract remains Hugging Face `Qwen/Qwen2.5-1.5B-Instruct` (Member 1).  
This Member 2 evidence run used **local Ollama `qwen2.5:3b`** because the pinned HF weights could not be downloaded reliably on the workstation. The prompt/decoding protocol matches the shared notebook. Re-run `scripts/run_member2_e2_e3.py` on **Colab T4** with the pinned HF model before final submission if the instructor requires identical checkpoint to E1.

---

## 7. Prompt-engineering experiments (E2)

### 7.1 Design

| Item | Choice |
|------|--------|
| Variants (4) | `zero_shot`, `few_shot`, `role_context`, `constraint_based` |
| Shared rules | Exact 77-label list + JSON contract + privacy rules |
| Few-shot | 4 fixed examples from `data/eval/in_prompt_examples.csv` |
| Evaluation subset | 10 rows from `development_evaluation.csv`, seed 42 (same rows for all variants) |
| Decoding for E2 | Greedy / temperature 0 (stable comparison) |
| Metrics | Schema validity, validated intent correctness, intent accuracy, macro-F1 on represented labels |

Baseline E1 (Member 1) used a simpler `baseline` prompt and scored **0/3** schema-valid on its three examples — a separate observational baseline, not part of this four-variant table.

### 7.2 Results (n=10 development subset)

| Variant | JSON valid rate | Intent correct (validated) | Intent accuracy (label string) | Mean latency (s) |
|---------|-----------------|----------------------------|--------------------------------|------------------|
| zero_shot | 0.50 | 0.20 | 0.30 | 14.3 |
| few_shot | 0.60 | 0.30 | 0.40 | 13.4 |
| role_context | **0.70** | 0.20 | 0.30 | 15.3 |
| constraint_based | 0.60 | **0.30** | 0.30 | 13.7 |

**Observations**

1. All improved prompts beat E1’s 0% schema acceptance on this broader sample.  
2. **`role_context`** produced the highest schema validity (0.70).  
3. **`few_shot`** and **`constraint_based`** tied for best validated intent correctness (0.30).  
4. Remaining failures are mostly Markdown fences, invented labels, or action/tool inconsistencies — same classes as E1 F1–F3.  
5. n=10 covers 10 intents only; do not claim 77-class performance. Expand to the full 40-row pilot on Colab for the final report table if time allows.

### 7.3 Recommended improved prompt for later stages

Prefer **`constraint_based`** (or **`few_shot` + constraint wording**) when locking the system for E4/E5/E7, because validated intent correctness matches the best rate and the instruction explicitly targets bare JSON. Keep **`role_context`** as a strong alternate when schema validity is the priority metric.

Files: `E2_prompt_comparison.csv`, `E2_*.csv`, `E2_summary.json`.

---

## 8. Decoding experiments (E3)

### 8.1 Design

| Item | Choice |
|------|--------|
| Prompt | `constraint_based` (fixed) |
| Settings | greedy (T=0); T=0.7 + top-k=50; T=0.7 + top-p=0.9 |
| Rows | 3 utterances from the E2 subset (seed 43) |

### 8.2 Results (n=3 × 3 settings, `constraint_based`)

| Decoding | JSON valid rate | Intent correct rate | Mean latency (s) |
|----------|-----------------|---------------------|------------------|
| greedy (T=0) | **0.67** | 0.33 | 13.8 |
| T=0.7 + top-k=50 | **0.67** | 0.33 | 12.2 |
| T=0.7 + top-p=0.9 | 0.33 | 0.33 | 11.9 |

**Observations**

- Greedy and top-k sampling matched on schema validity for this tiny sample; **top-p** dropped validity to 0.33.  
- Intent correctness stayed at 0.33 across settings (n=3 is observational only).  
- For production-like JSON, keep **greedy** after locking the prompt; retain the sampling rows as the required decoding study.

Files: `E3_decoding.csv`, `E3_decoding_summary.csv`, `E3_summary.json`.

---

## Contribution statement (Member 2)

I, Takkars Bhavani, am responsible for prompt-engineering experiments (E2: ≥4 variants with comparison table), decoding study (E3: greedy vs temperature + top-k/top-p), the prompt experiment log, and report sections 7–8. I will explain these experiments in the group demonstration.

Member confirmation/signature: ____________________  Date: _______________
