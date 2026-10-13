# pcam-zg516-a1-banking77

**BITS Pilani WILP · PGAIML · PCAM\* ZG516 Applied Generative AI**  
**Group Major Project / Assignment-1 · Dataset D1: BANKING77**

Banking customer-service assistant: intent understanding + safe response generation + structured JSON + simulated tool calling, using a pretrained Hugging Face causal LLM (prompting-focused; no training from scratch).

## Team

See [TEAM.md](TEAM.md). Group 15.

## Repository layout

```text
pcam-zg516-a1-banking77/
├── notebooks/          # Colab / executable experiments (E1–E7)
├── data/
│   ├── raw/            # local samples (gitignored); load BANKING77 from HF in notebook
│   └── eval/           # fixed eval subset IDs / samples for fair comparison
├── schemas/            # JSON / tool schemas
├── prompts/            # prompt variants and templates
├── src/                # reusable helpers (validation, tools, generation)
├── docs/               # architecture notes, adaptation decision
├── reports/            # technical report drafts, tables, demo script
├── demo/               # short demo checklist / slides notes
├── requirements.txt
├── TEAM.md
└── README.md
```

## Required experiments (assignment)

| ID | Experiment | Owner lead |
|----|------------|------------|
| E1 | Baseline simple prompt | Anil |
| E2 | ≥4 prompt variants | Bhavani |
| E3 | Greedy + temperature + top-k/top-p | Bhavani |
| E4 | Structured JSON + validation | Nisha |
| E5 | ≥1 tool/function | Nisha |
| E6 | ≥3 failure cases | Venkat |
| E7 | Integrated final workflow | All (Venkat integrates) |

## Quick start (local or Colab)

```bash
git clone https://github.com/venkat-tunuguntla/pcam-zg516-a1-banking77.git
cd pcam-zg516-a1-banking77
pip install -r requirements.txt
```

Open `notebooks/` and run sections in order (baseline → prompts → decoding → structured output → tool → eval).

## Deliverables

- Working Colab/notebook in `notebooks/`
- Technical report (10–15 pages) in `reports/`
- Prompt log, decoding table, schema samples, tool demo, evaluation + failure analysis
- 8–10 minute group demonstration
- Individual contribution statement

## Safety

Use only public BANKING77 text and mock tool backends. Do not use real banking credentials, account numbers, or personal financial data.
