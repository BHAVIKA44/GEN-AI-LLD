# Problem Statement

Build an evaluation pipeline for LLM outputs using LLM-as-a-judge.

# Requirements

## Functional requirements
- Accept evaluation cases (prompt, output, optional reference).
- Evaluate each case across rubric criteria.
- Aggregate weighted scores per case.
- Mark pass/fail using threshold.
- Produce pipeline-level report (pass rate, average score).

## Non-functional requirements
- Interview-sized and easy to explain.
- Extensible judge and rubric design.
- Offline deterministic tests (no API keys/services).

## Assumptions
- Scores are normalized between 0 and 1.
- Rubric is static for one pipeline run.

# Design Overview

Main components:
- `EvaluationPipeline`: orchestration and aggregation.
- `LLMJudge` interface: criterion scoring abstraction.
- `HeuristicLLMJudge`: deterministic mock LLM-as-judge implementation.
- Models for case input, criterion definitions, and report output.

Data flow:
1. Pipeline loops over cases and rubric criteria.
2. Judge returns criterion-level score + reasoning.
3. Pipeline computes weighted score and pass/fail.
4. Pipeline aggregates global metrics.

# Class / Module Design

- `models.py`
  - `EvaluationCase`
  - `RubricCriterion`
  - `CriterionScore`
  - `CaseEvaluation`
  - `PipelineReport`
- `interfaces.py`
  - `LLMJudge`
- `judges.py`
  - `HeuristicLLMJudge`
- `pipeline.py`
  - `EvaluationPipeline`

# Technology Selection Rationale

- LangChain: Not used in implementation.
  - Why: this problem is evaluation orchestration and scoring logic; interface-based design is enough for 1-hour round.
  - Tradeoff: no built-in prompt/model adapters in this baseline.
- LangGraph: Not used.
  - Why: workflow is linear and synchronous.
- Evaluation frameworks (Ragas/DeepEval/TruLens/LangSmith evals): Not used in code.
  - Why: avoid framework overhead in timed round; architecture can wrap them later via `LLMJudge`.

# Error Handling

- Empty rubric rejected.
- Invalid threshold rejected.
- Empty input cases handled gracefully with zeroed report.

# Testing Strategy

- End-to-end multi-case evaluation.
- Empty-case pipeline behavior.
- Threshold validation path.

# Tradeoffs

- Heuristic judge is a stand-in for real LLM judge.
- No async/batching/retry pipeline.
- No experiment tracking or observability integration.

# How to Run

Install:
```bash
cd llm-evaluation-pipeline-judge
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
