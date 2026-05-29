# Problem Statement

Write code to detect and handle hallucinations in LLM outputs.

# Requirements

## Functional requirements
- Detect hallucination risk signals from LLM output.
- Aggregate signals into a normalized risk score.
- Apply handling policy based on severity:
  - pass
  - sanitize
  - abstain
- Return final answer plus detection metadata.

## Non-functional requirements
- Interview-sized design and code.
- Extensible detector architecture.
- Offline deterministic behavior and tests.

## Assumptions
- Retrieved context is available for grounding checks.
- Confidence score may be available from upstream model.
- Heuristic detection is acceptable for baseline.

# Design Overview

Main components:
- `CompositeHallucinationDetector`: runs multiple checks and aggregates risk.
- `HallucinationHandler`: policy engine for action selection.
- Data models for input, signals, detection result, and handled response.

Data flow:
1. Input answer + context enters detector.
2. Detector emits risk signals (grounding/confidence/claim style).
3. Handler chooses action by threshold.
4. Final response includes action, answer, risk score, and signals.

# Class / Module Design

- `models.py`
  - `LLMOutput`
  - `HallucinationSignal`
  - `DetectionResult`
  - `HandledResponse`
- `interfaces.py`
  - `HallucinationDetector`
- `detectors.py`
  - `CompositeHallucinationDetector`
- `handler.py`
  - `HallucinationHandler`

# Technology Selection Rationale

- LangChain/LangGraph: Not used.
  - Why: task is focused on detection/handling policy logic and can be implemented clearly without orchestration framework overhead.
  - Tradeoff: fewer built-in integrations.
- Guardrails frameworks (Guardrails AI, NeMo, etc.): Not used in baseline.
  - Why: 1-hour scope; design leaves clean adapter points.
  - Tradeoff: less policy depth out of the box.

# Error Handling

- Threshold validation on handler construction.
- Safe defaults when confidence is unavailable.
- Deterministic fallback behaviors for moderate/high risk.

# Testing Strategy

- Low-risk output passes unchanged.
- Moderate-risk output is sanitized and flagged.
- High-risk output is abstained with safe response.

# Tradeoffs

- Heuristic signals are lightweight and imperfect.
- No model-based factual verification.
- No external policy service integration.

# How to Run

Install:
```bash
cd hallucination-detection-handling
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
