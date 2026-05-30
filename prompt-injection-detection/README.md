# Problem Statement

Write code to detect prompt injection attempts in user inputs.

# Requirements

## Functional requirements
- Analyze user input for prompt-injection patterns.
- Produce a risk score and detection signals.
- Map risk score to policy action (`allow`, `warn`, `block`).

## Non-functional requirements
- Interview-friendly implementation.
- Deterministic and testable behavior.
- Extensible detection rules.

## Assumptions
- Rule-based detection is acceptable baseline.
- Risk scoring can be additive and capped at 1.0.

# Design Overview

Main components:
- `RuleBasedPromptInjectionDetector`: pattern/signal detector.
- `PromptInjectionGuard`: policy layer that converts risk to action.
- Structured models for signals and final decision.

Data flow:
1. Detector scans text for known injection cues.
2. Detector returns signals + aggregate risk.
3. Guard applies thresholds and returns decision.

# Class / Module Design

- `models.py`: `DetectionSignal`, `DetectionResult`, `GuardDecision`
- `interfaces.py`: `InjectionDetector`
- `detector.py`: rule-based detector
- `handler.py`: guard policy

# Technology Selection Rationale

- Pure Python: Used.
  - Why: problem is security logic and can be implemented clearly in 1 hour.
- LangChain/LangGraph: Not used.
  - Why: no orchestration requirement; this is a reusable guard utility.

# Error Handling

- Threshold config validation.
- Empty input handled safely as low risk.
- Risk score capped to [0, 1].

# Testing Strategy

- Benign input allow path.
- Medium-risk warning path.
- High-risk block path.
- Empty input behavior.

# Tradeoffs

- Rule-based approach has false positives/negatives.
- No model-based semantic classifier.
- No multilingual pattern set.

# How to Run

Install:
```bash
cd prompt-injection-detection
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
