# Local Ollama model comparison (informational)

**Primary submission runtime for E2–E5 local evidence:** `qwen2.5:1.5b-instruct`  
**Official group HF pin (Colab):** `Qwen/Qwen2.5-1.5B-Instruct`  
**Earlier exploratory runtime (not primary):** `qwen2.5:3b`

Same protocol: BANKING77 development subset, seed 42, E2 n=10, E3 n=3, greedy for E2. Metrics are observational; do not claim 77-class performance.

## E2 — prompt variants (JSON valid / validated intent)

| Variant | `qwen2.5:1.5b-instruct` (primary) | `qwen2.5:3b` (exploratory) |
|---------|-----------------------------------|----------------------------|
| zero_shot | **0.60 / 0.10** | 0.50 / 0.20 |
| few_shot | 0.30 / 0.10 | 0.60 / 0.30 |
| role_context | 0.30 / 0.10 | **0.70 / 0.20** |
| constraint_based | 0.10 / 0.00 | 0.60 / 0.30 |

**Best by JSON then intent:** `zero_shot` on 1.5b-instruct; `role_context` on 3b.

## E3 — decoding (JSON valid / intent correct)

| Decoding | 1.5b-instruct (prompt = best E2: `zero_shot`) | 3b (prompt = `constraint_based`) |
|----------|-----------------------------------------------|----------------------------------|
| greedy | **0.33 / 0.00** | **0.67 / 0.33** |
| T=0.7 + top-k=50 | 0.00 / 0.00 | 0.67 / 0.33 |
| T=0.7 + top-p=0.9 | 0.33 / 0.00 | 0.33 / 0.33 |

## Takeaways

1. **3b scored higher** on schema validity and validated intent under the same experiment design.  
2. We still **standardize on `qwen2.5:1.5b-instruct`** for local evidence because it matches the assignment HF size/family pin (`Qwen2.5-1.5B-Instruct`).  
3. Longer prompts (`constraint_based`, `role_context`) helped 3b but **hurt** 1.5b-instruct; zero-shot was best on the primary model.  
4. Prefer **greedy** decoding for structured JSON on both runs.  
5. E4 designed validation (10/10) and the mock tool backend are **model-independent**; E5 live LLM→tool success still needs schema-valid BANKING77 intents.

Primary numbers: `evidence/prompts_decoding/`, `evidence/structured_tools/`, reports §§7–8 and §10.
