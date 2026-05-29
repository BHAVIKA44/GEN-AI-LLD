from __future__ import annotations

from typing import Protocol

from .models import CriterionScore, EvaluationCase, RubricCriterion


class LLMJudge(Protocol):
    def judge(
        self,
        case: EvaluationCase,
        criterion: RubricCriterion,
    ) -> CriterionScore:
        """Score one criterion for one output."""
