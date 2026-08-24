"""ProductionController + PipelineRunner integration acceptance test.

TASK-006-003-D-03-B

This test verifies that ProductionController does not merely report a
completed Pipeline, but actually executes the configured Agent chain.
"""

from src.core.production_controller import ProductionController


TEST_TOPIC = "美国航母部署"

EXPECTED_AGENTS = [
    "NewsAgent",
    "NewsVerifier",
    "SourceRanker",
    "TopicScorer",
    "TopicSelector",
]


def test_production_controller_runs_full_pipeline():
    """ProductionController must execute the complete topic pipeline."""
    controller = ProductionController()

    result = controller.run_pipeline(
        {
            "title": TEST_TOPIC,
            "topic": TEST_TOPIC,
            "options": {
                "max_candidates": 5
            },
        }
    )

    assert isinstance(result, dict)
    assert result.get("status") == "COMPLETED"

    pipeline_result = result.get("pipeline_result")
    assert isinstance(pipeline_result, dict)
    assert pipeline_result.get("pipeline_status") == "COMPLETED"
    assert pipeline_result.get("failed_agent") is None
    assert pipeline_result.get("completed_agents") == EXPECTED_AGENTS
