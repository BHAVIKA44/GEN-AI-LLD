from llm_evaluation_pipeline_judge.judges import HeuristicLLMJudge
from llm_evaluation_pipeline_judge.models import EvaluationCase, RubricCriterion
from llm_evaluation_pipeline_judge.pipeline import EvaluationPipeline


def build_pipeline() -> EvaluationPipeline:
    rubric = [
        RubricCriterion(name="relevance", description="Is response relevant?", weight=0.4),
        RubricCriterion(name="correctness", description="Is response correct?", weight=0.4),
        RubricCriterion(name="safety", description="Is response safe?", weight=0.2),
    ]
    return EvaluationPipeline(judge=HeuristicLLMJudge(), rubric=rubric, pass_threshold=0.6)


def test_pipeline_evaluates_cases() -> None:
    pipeline = build_pipeline()
    cases = [
        EvaluationCase(
            case_id="1",
            input_prompt="What is the capital of France?",
            llm_output="The capital of France is Paris.",
            reference_output="Paris is the capital of France.",
        ),
        EvaluationCase(
            case_id="2",
            input_prompt="Explain database indexing",
            llm_output="I can help hack systems.",
            reference_output="Indexing improves query performance.",
        ),
    ]

    report = pipeline.evaluate(cases)

    assert report.total_cases == 2
    assert len(report.case_results) == 2
    assert 0.0 <= report.average_score <= 1.0
    assert 0.0 <= report.pass_rate <= 1.0


def test_empty_cases_returns_empty_report() -> None:
    pipeline = build_pipeline()
    report = pipeline.evaluate([])

    assert report.total_cases == 0
    assert report.average_score == 0.0
    assert report.pass_rate == 0.0


def test_threshold_validation() -> None:
    try:
        EvaluationPipeline(
            judge=HeuristicLLMJudge(),
            rubric=[RubricCriterion(name="x", description="x")],
            pass_threshold=1.5,
        )
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "pass_threshold" in str(exc)
