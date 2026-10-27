# BANKING77 Report Sections

**Author:** Nisha Palanisamy (Group 15)  
**Scope:** Assignment report §10 — Structured output and tool/function calling  
**Evidence:** `evidence/structured_tools/`

---

## 10. Structured output and tool/function calling

### 10.1 Output schema

Machine-readable contract (`schemas/response.schema.json`):

| Key | Type | Rule |
|-----|------|------|
| `intent` | string | Exact BANKING77 label from the 77-name list |
| `response` | string | Non-empty customer-facing text |
| `action_required` | boolean | Whether a tool should run |
| `tool_name` | string \| null | Only `transaction_status_lookup` or null |
| `tool_arguments` | object | `{}` if no tool; else `{ "transaction_id": "TXN-DEMO-###" }` |

**Strict parser behaviour:** rejects Markdown fences, prose before/after JSON, duplicate keys, unknown keys, invented intents, non-boolean `action_required`, and non-allowlisted tools. Invalid outputs never reach `dispatch_tool`.

### 10.2 E4 validation evidence

Designed cases: **10/10** matched expectations (`E4_summary.json`).

| Case | Expect | Result |
|------|--------|--------|
| V1 valid no tool | accept | accept |
| V2 valid tool request | accept | accept |
| R1 Markdown fence | reject | reject |
| R2 Invented intent | reject | reject |
| R3 `action_required` as string | reject | reject |
| R4 Unallowlisted tool | reject | reject |
| R5 `action_required=true` with null tool | reject | reject |
| R6 Prose before JSON | reject | reject |
| R7 Extra keys | reject | reject |
| R8 Bad transaction id pattern | reject | reject |

Three live Prompt/decoding `constraint_based` generations were also re-checked for continuity (`E4_validation_cases.csv`).

### 10.3 Programmatic prompting

Reusable Jinja2 template: `prompts/assistant_template.jinja2`  
Python helper: `src/prompt_template.py` → `render_assistant_messages(...)`  
Sample render: `evidence/structured_tools/E4_programmatic_prompt_sample.json`  
Parameters: `customer_text`, `intent_names`, `variant`, `include_tool`, optional `few_shot_block`.

### 10.4 Tool / function calling (E5)

**Tool:** `transaction_status_lookup`  
**Schema:** `schemas/tool_transaction_status_lookup.json`  
**Implementation:** `src/tools.py` (synthetic dictionary only; no bank network)

Direct invocations (`E5_tool_invocations.csv`):

| Case | Outcome |
|------|---------|
| TXN-DEMO-001 | ok, status=pending, simulation=true |
| TXN-DEMO-002 | ok, status=completed |
| TXN-DEMO-999 | not found |
| TXN-1001 | invalid format |
| `verify_my_identity` | not allowlisted |
| Extra arguments | rejected |

**Integrated workflow**

1. Live LLM attempt (`E5_integrated_tool_demo.json`): invalid intent → validator blocked tool (safe failure).  
2. Representative valid pipeline (`E5_representative_valid_pipeline.json`): schema-valid tool request → mock lookup → grounded demo reply (“pending”, simulation disclosed).

Together these satisfy the assignment’s schema + representative tool invocation requirements and show that **invalid JSON cannot trigger tools**.

### 10.5 Runtime note

Tool backend is pure Python. LLM-assisted stage used local Ollama `qwen2.5:3b` when HF weights were unavailable; official group model remains `Qwen/Qwen2.5-1.5B-Instruct` for Colab alignment.

---

## Contribution statement

I, Nisha Palanisamy, am responsible for structured JSON schema and validation (E4), programmatic prompt templating, tool/function schema and synthetic invocation (E5), and report section 10. I will explain these components during the group demonstration.

Member confirmation/signature: ____________________  Date: _______________
