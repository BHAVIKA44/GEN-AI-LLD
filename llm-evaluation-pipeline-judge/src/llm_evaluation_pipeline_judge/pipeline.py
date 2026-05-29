from __future__ import annotations

from .interfaces import LLMJudge
from .models import CaseEvaluation, EvaluationCase, PipelineReport, RubricCriterion


class EvaluationPipeline:
    def __init__(
        self,
        judge: LLMJudge,
        rubric: list[RubricCriterion],
        pass_threshold: float = 0.7,
    ) -> None:
        if not rubric:
            raise ValueError("rubric must not be empty")
        if pass_threshold < 0 or pass_threshold > 1:
            raise ValueError("pass_threshold must be between 0 and 1")
        self._judge = judge
        self._rubric = rubric
        self._pass_threshold = pass_threshold

    def evaluate(self, cases: list[EvaluationCase]) -> PipelineReport:
        if not cases:
            return PipelineReport(total_cases=0, pass_rate=0.0, average_score=0.0, case_results=[])

        case_results: list[CaseEvaluation] = []
        for case in cases:
            scores = [self._judge.judge(case, criterion) for criterion in self._rubric]
            weighted = self._weighted_score(scores)
            case_results.append(
                CaseEvaluation(
                    case_id=case.case_id,
                    criterion_scores=scores,
                    weighted_score=weighted,
                    passed=weighted >= self._pass_threshold,
                )
            )

        passed = sum(1 for r in case_results if r.passed)
        avg = sum(r.weighted_score for r in case_results) / len(case_results)
        return PipelineReport(
            total_cases=len(case_results),
            pass_rate=passed / len(case_results),
            average_score=avg,
            case_results=case_results,
        )

    def _weighted_score(self, scores) -> float:
        weights = {c.name: c.weight for c in self._rubric}
        total_weight = sum(weights.values())
        weighted_sum = sum(score.score * weights.get(score.criterion_name, 1.0) for score in scores)
        return weighted_sum / total_weight if total_weight > 0 else 0.0
