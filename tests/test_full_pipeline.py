import os

from src.core.production_controller import ProductionController


TEST_TOPIC = "美国航母部署"


def test_full_pipeline_entry():
    """
    TASK-006-003-D-01
    Pipeline全链路入口测试

    验证目标：
    ProductionController -> PipelineRunner -> Agent Pipeline
    """

    controller = ProductionController()

    request = {
        "title": TEST_TOPIC,
        "topic": TEST_TOPIC,
        "options": {
            "max_candidates": 5
        }
    }

    result = controller.run_pipeline(request)

    assert result is not None
    assert isinstance(result, dict)

    assert "status" in result or "pipeline_status" in result


if __name__ == "__main__":
    test_full_pipeline_entry()
    print("FULL PIPELINE TEST PASSED")
