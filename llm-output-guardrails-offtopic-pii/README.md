# Problem Statement

Implement an LLM output guardrails system that checks for off-topic responses and PII leakage.

# Requirements

## Functional requirements
- Detect off-topic responses.
- Detect potential PII leakage in output.
- Aggregate risk signals.
- Apply policy action: `pass`, `redact`, or `block`.

## Non-functional requirements
- Interview-sized implementation.
- Deterministic local checks.
- Extensible check interface.

## Assumptions
- Off-topic can be approximated by lexical overlap.
- PII patterns use regex heuristics.

# Design Overview

Main components:
- `OffTopicCheck`
- `PIICheck`
- `OutputGuardrails` policy engine

Data flow:
1. Run checks on `(query, output)`.
2. Collect signals and sum risk.
3. If high risk -> block.
4. If moderate risk -> redact PII.
5. Else -> pass.

# Class / Module Design

- `models.py`: input/result/signal models
- `interfaces.py`: `OutputCheck`
- `checks.py`: off-topic + PII checks + redaction helper
- `guardrails.py`: actioning logic

# Technology Selection Rationale

- Pure Python: Used.
  - Why: focused guardrail logic for 1-hour implementation.
- LangChain/LangGraph: Not used.
  - Why: this is a lightweight post-processing policy utility.

# Error Handling

- Threshold validation.
- Empty checks list rejected.
- Risk score normalized to `[0,1]`.

# Testing Strategy

- Relevant non-PII output passes.
- PII-containing output gets redacted or blocked.
- Combined risk scenario behavior validated.

# Tradeoffs

- Regex PII detection is heuristic.
- Off-topic check is lexical, not semantic.
- No compliance/audit pipeline integration.

# How to Run

Install:
```bash
cd llm-output-guardrails-offtopic-pii
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
