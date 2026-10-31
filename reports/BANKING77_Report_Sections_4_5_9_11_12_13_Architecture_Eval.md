# BANKING77 Report Sections

**Author:** Venkata Srinivasa Rao Tunuguntla  
**Group:** 15 · PCAM\* ZG516 Applied Generative AI  
**Scope:** Report sections 4, 5, 9, 11, 12, 13 (assignment numbering). Merge with Baseline §§2, 3, 6, E2–E3 (also owned here), and E4–E5 evidence from Nisha.

Evidence referenced: [`evidence/baseline/`](../evidence/baseline/) (E1 baseline) and [`evidence/evaluation/`](../evidence/evaluation/) (eval rubric, E6 table, E7 checklist).

---

## 4. Generative-model and LLM architecture analysis

### 4.1 Generative-model family comparison (CS1)

At least three generative-model families from CS1 are relevant to this application:

| Family | How it generates | Fit for BANKING77 assistant |
|--------|------------------|-----------------------------|
| **Causal / autoregressive LLM (selected)** | Next-token prediction conditioned on prompt context; chat templates support instruction following | Direct fit for intent selection + natural-language reply + optional tool request in one prompted workflow |
| **VAE** | Encode input to a latent distribution, sample/decode | Strong for representation learning / controlled variation; weak fit for constrained multi-field JSON and policy-safe wording without a large task-specific redesign |
| **GAN** | Generator vs discriminator adversarial training | Useful for synthetic data realism; not a natural controller for allowlisted tools, refusal behaviour, or exact intent labels |
| **Diffusion (contrast)** | Iterative denoising from noise | Dominant for continuous media (images/audio); not the primary stack for short customer-service text JSON in this assignment |

**Decision:** Use a pretrained **causal LLM**. The user need is language understanding plus constrained generation, not image synthesis or latent reconstruction. VAE/GAN/diffusion remain comparison points; this project does not train them.

### 4.2 LLM building blocks in this project (CS2–CS3)

| Component | Role in the banking assistant |
|-----------|-------------------------------|
| **Tokenizer** | Turns system rules, 77 intent names, optional few-shot examples, and the customer utterance into token IDs via the model chat template |
| **Embeddings** | Map token IDs into vectors consumed by the Transformer |
| **Transformer / attention** | Conditions generation on the full prompt (labels, safety rules, request) |
| **Language-modelling head** | Scores the next-token distribution |
| **Autoregressive decode** | Prefill processes the prompt; decode emits JSON fields token by token until EOS or `max_new_tokens` |
| **Decoding controls** | Greedy (E1 default) for stable baselines; temperature / top-k / top-p (E3) to study variability vs validity |

**Implemented model:** `Qwen/Qwen2.5-1.5B-Instruct` (pinned revision), Hugging Face `AutoModelForCausalLM`, no training from scratch and no weight updates in the Baseline baseline.

### 4.3 Why not “just a classifier”?

A classical intent classifier could score the 77 labels well. The assignment also requires **response generation**, **decoding study**, **structured output**, and **tool/function workflow**. A prompted causal LLM covers that end-to-end path; classification accuracy alone would underspecify the deliverable.

---

## 5. Proposed application architecture

```text
Customer utterance
        │
        ▼
Prompt builder (baseline / zero-shot / few-shot / role / constraint)
        │
        ▼
Tokenizer + chat template  →  Qwen2.5-1.5B-Instruct  →  decoding
        │
        ▼
Strict JSON extract + validate
        │
        ├── invalid → refuse tool; safe fallback message; log failure
        └── valid
              ├── action_required=false → return response
              └── action_required=true
                        │
                        ▼
              allowlisted tool: transaction_status_lookup (mock TXN-DEMO-###)
                        │
                        ▼
              grounded final reply (demo status only) or escalation text
```

**Contracts (frozen):**

- Output keys: `intent`, `response`, `action_required`, `tool_name`, `tool_arguments`
- Tool: `transaction_status_lookup` only; synthetic IDs `TXN-DEMO-###`
- Subsets: development pilot (40) for prompt/decoding design; official test pilot (40) reserved after lock; seed 42

**Modules in the repo:** notebook backbone ([`notebooks/BANKING77_GenAI_Assistant.ipynb`](../notebooks/BANKING77_GenAI_Assistant.ipynb)), schemas under [`schemas/`](../schemas/), mock tool in [`src/tools.py`](../src/tools.py), fixed eval rows under [`data/eval/`](../data/eval/).

---

## 9. Adaptation strategy: prompting vs RAG vs PEFT

| Approach | What it changes | Fit for this 2-week prototype | Cost / risk |
|----------|-----------------|-------------------------------|-------------|
| **Prompting (selected)** | Instructions, examples, constraints, decoding | Matches assignment experiments E1–E5; reproducible on Colab; no training | Prompt brittleness; label invention; JSON wrappers (seen in E1) |
| **RAG** | Retrieve approved FAQ/policy snippets into context | Useful if answers must cite **current bank policy**; BANKING77 labels alone are not policy text | Needs curated corpus + citation discipline; retrieval errors can look “authoritative” |
| **PEFT / LoRA** | Small trainable adapters on frozen base weights | Could improve JSON/intent consistency after enough labelled pairs | Extra compute, data prep, eval burden; optional unless approved |

**Implemented choice:** **Prompting (+ strict validation + allowlisted tool)**.  
**RAG:** treat as future work if an instructor-approved FAQ is added; do not invent policy from the intent name alone.  
**PEFT:** not required for the baseline scope; revisit only if prompting plateaus on the development pilot after E2/E3.

---

## 11. Evaluation and results

### 11.1 Criteria (≥4)

Reported **separately** (never collapsed into one “accuracy” number):

| # | Criterion | How measured | Notes |
|---|-----------|--------------|-------|
| 1 | **Intent correctness** | Exact match of validated `intent` vs gold label | Only count schema-valid outputs; invalid JSON → intent incorrect for the pipeline |
| 2 | **Schema validity** | Strict parser + contract checks | Rejects Markdown fences, unknown keys, non-allowlisted tools |
| 3 | **Response safety / relevance** | Manual rubric 1–5 + binary “no credential solicitation / no fake completion” | Required because BANKING77 has no gold replies |
| 4 | **Tool-call correctness** | Allowlist, argument shape, ID pattern, no call on invalid JSON | BANKING77 has no tool gold labels |
| 5 | **Latency / tokens (ops)** | Wall time, input/output tokens | Supporting metric for demo practicality |

Macro-F1 over **represented** labels only may be reported for larger pilots; a 3-example E1 set must not claim 77-class performance.

### 11.2 Baseline (E1) observed results

Source: [`evidence/baseline/E1_summary.json`](../evidence/baseline/E1_summary.json) and [`E1_baseline_outputs.jsonl`](../evidence/baseline/E1_baseline_outputs.jsonl) (CPU float32 verification run).

| Metric | Value |
|--------|-------|
| n | 3 development examples |
| Strict schema valid | **0 / 3** |
| Intent correct (validated) | **0 / 3** |
| Decoding | Greedy |
| General accuracy claim | **False** |

These establish a weak but honest baseline. Improved systems (E2+) must beat schema validity and safety on the **same** `development_evaluation.csv` rows before any reserved-test comparison.

### 11.3 Comparative table (local Ollama `qwen2.5:1.5b-instruct`)

Evidence: [`evidence/prompts_decoding/`](../evidence/prompts_decoding/), [`evidence/structured_tools/`](../evidence/structured_tools/). Development subset n=10 for E2; E3 n=3; not a 77-class claim.

| System | Schema valid rate | Intent accuracy (validated) | Safety / tool notes |
|--------|-------------------|-----------------------------|---------------------|
| E1 baseline | 0/3 | 0/3 | Markdown / invented label / credential ask |
| Best prompt (E2 `zero_shot`) | 0.60 (n=10) | 0.10 | Beats E1 schema rate; intent still weak on 1.5B local |
| Best decoding (E3 greedy on `zero_shot`) | 0.33 (n=3) | 0.00 | Prefer greedy; top-k produced 0 valid JSON |
| + validation/tool (E4/E5) | E4 designed 10/10 | N/A (controls) | Invalid LLM JSON blocked tool; mock `TXN-DEMO-###` OK |

---

## 12. Failure analysis and responsible-use considerations

### 12.1 E6 — observed failure cases (≥3)

Full table: [`evidence/evaluation/E6_failure_analysis.csv`](../evidence/evaluation/E6_failure_analysis.csv). Summary:

| ID | Input (short) | Gold | Failure category | Observed issue | Mitigation |
|----|---------------|------|------------------|----------------|------------|
| F1 | Top-up reverted by app | `top_up_reverted` | Malformed structured output | Correct-looking label inside Markdown fences; `action_required=true` with null tool | Constraint prompt: “bare JSON only”; reject fences; require tool name iff action |
| F2 | Why can't I use disposable card? | `disposable_card_limits` | Label invention / open vocabulary | Invented intent `why_can_t_i_use_a_disposable_card` | Few-shot + explicit “copy label exactly”; validator drops unknown labels |
| F3 | ATM didn't return card | `card_swallowed` | Unsafe + wrong intent + bad tool | Predicted `lost_or_stolen_card`; unapproved tool; asked for card number | Privacy rules; allowlist only `transaction_status_lookup`; escalate instead of collecting PAN |

Additional **designed** cases for the integrated demo (validator/tool path), logged in the same CSV as F4–F6: ambiguous close intents, missing demo transaction ID, and explicit credential bait. These exercise controls even before full E2 numbers exist.

### 12.2 Responsible use

- Academic simulation only — no bank connectivity, no real balances, blocks, or transfers.  
- Never solicit or echo PINs, passwords, OTPs, or full card numbers.  
- Do not invent fees, eligibility, or transaction status; tool results are synthetic and must be labelled as demo.  
- Ambiguous or high-impact requests → escalate to the bank’s official channel.  
- Valid JSON ≠ truthful or safe reply; keep manual review in the scoring pack.  
- Dataset is CC BY 4.0 BANKING77; retain attribution ([`docs/baseline/ATTRIBUTION.txt`](../docs/baseline/ATTRIBUTION.txt)).

---

## 13. Limitations

1. **Coverage:** 40-row pilots cover 40/77 intents; E1 uses only 3 rows — not a full-benchmark claim.  
2. **No gold responses or tool labels** in BANKING77 — response/tool metrics need human review.  
3. **Small instruct model** can invent labels and wrap JSON; validation is mandatory.  
4. **Prompting-only adaptation** may plateau; RAG/PEFT not implemented in this iteration.  
5. **Hardware variance:** CPU vs GPU dtype/library versions can change generations; compare manifests.  
6. **Local 1.5B instruct** improves schema vs E1 but intent remains low; Colab HF pin may differ from Ollama tag behaviour.  
7. **E7 demo** path is ready; live LLM→tool success still depends on producing schema-valid BANKING77 intents.

---

## Contribution statement

I, Venkata Srinivasa Rao Tunuguntla, am responsible for generative-model/LLM architecture analysis, application architecture, adaptation decision (prompting vs RAG vs PEFT), evaluation rubric, E6 failure analysis, responsible-use/limitations write-up, E7 integration checklist and demo script, E2 prompt-engineering and E3 decoding experiments (reassigned within Group 15), and merging these sections into the group report. I will explain this workflow in the group demonstration.

Member confirmation/signature: ____________________  Date: _______________
