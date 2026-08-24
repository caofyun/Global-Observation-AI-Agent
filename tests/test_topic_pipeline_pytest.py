"""
Pytest wrapper for Topic Pipeline V2.0 integration test.

Keeps the original test_topic_pipeline.py executable script unchanged.
Provides pytest discovery entry point.
"""

from tests import test_topic_pipeline as pipeline


def test_topic_pipeline_v2_integration():
    """Run Topic Pipeline V2.0 end-to-end validation."""

    pipeline.prepare_test_root()

    topic_results = []

    for topic in pipeline.TEST_TOPICS:
        result = pipeline.process_topic(topic)
        topic_results.append(result)

    successful_topics = [
        item
        for item in topic_results
        if item["success"]
    ]

    selection = pipeline.run_topic_selector(successful_topics)

    assert selection is not None
    assert pipeline.verify_selection_output(selection)

    assert len(successful_topics) >= 2
