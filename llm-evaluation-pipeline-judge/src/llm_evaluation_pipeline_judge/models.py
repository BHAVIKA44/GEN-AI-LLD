from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    input_prompt: str
    llm_output: str
    reference_output: str | None = None


@dataclass(frozen=True)
class RubricCriterion:
    name: str
    description: str
    weight: float = 1.0


@dataclass(frozen=True)
class CriterionScore:
    criterion_name: str
    score: float
    reasoning: str


@dataclass(frozen=True)
class CaseEvaluation:
    case_id: str
    criterion_scores: list[CriterionScore]
    weighted_score: float
    passed: bool


@dataclass(frozen=True)
class PipelineReport:
    total_cases: int
    pass_rate: float
    average_score: float
    case_results: list[CaseEvaluation]
