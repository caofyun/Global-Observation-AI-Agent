import json
import os

from src.core.discovery_pipeline_adapter import DiscoveryPipelineAdapter


class StubAgent:
    def __init__(self, name, calls, status="SUCCESS"):
        self.name = name
        self.calls = calls
        self.status = status

    def run(self, input_data):
        self.calls.append((self.name, input_data))
        if self.status == "RAISE":
            raise RuntimeError(self.name + " failed")
        return {"status": self.status, "result": {"agent": self.name}, "error": ""}


def write_discovery_output(tmp_path, articles=None, status="SUCCESS", topic="全球军事热点"):
    output_dir = tmp_path / "01_新闻资料"
    output_dir.mkdir()
    output = {
        "schema_version": "2.1", "status": status, "domain": "军事", "topic": topic,
        "discovery": {}, "statistics": {}, "articles": articles if articles is not None else [{"title": "候选"}],
    }
    (output_dir / "news_articles.json").write_text(json.dumps(output, ensure_ascii=False), encoding="utf-8")


def make_adapter(calls, statuses=None):
    statuses = statuses or {}
    return DiscoveryPipelineAdapter(
        news_verifier=StubAgent("NewsVerifier", calls, statuses.get("NewsVerifier", "SUCCESS")),
        source_ranker=StubAgent("SourceRanker", calls, statuses.get("SourceRanker", "SUCCESS")),
        topic_scorer=StubAgent("TopicScorer", calls, statuses.get("TopicScorer", "SUCCESS")),
        topic_selector=StubAgent("TopicSelector", calls, statuses.get("TopicSelector", "SUCCESS")),
    )


def test_success_runs_pipeline_in_order_and_passes_topic_and_project_path(tmp_path):
    write_discovery_output(tmp_path)
    calls = []
    result = make_adapter(calls).run(str(tmp_path))
    assert result["status"] == "SUCCESS"
    assert result["topic"] == "全球军事热点"
    assert [call[0] for call in calls] == ["NewsVerifier", "SourceRanker", "TopicScorer", "TopicSelector"]
    assert calls[0][1] == {"project_path": str(tmp_path), "topic_keyword": "全球军事热点"}
    assert calls[1][1] == {"project_path": str(tmp_path)}
    assert calls[2][1] == {"project_path": str(tmp_path), "topic": "全球军事热点"}
    assert calls[3][1] == {}


def test_discovery_failed_does_not_enter_pipeline(tmp_path):
    write_discovery_output(tmp_path, status="FAILED")
    calls = []
    result = make_adapter(calls).run(str(tmp_path))
    assert result["status"] == "FAILED"
    assert calls == []


def test_empty_articles_are_successfully_skipped_without_fake_data(tmp_path):
    write_discovery_output(tmp_path, articles=[])
    calls = []
    result = make_adapter(calls).run(str(tmp_path))
    assert result["status"] == "SUCCESS"
    assert result["skipped"] is True
    assert result["topic"] == "全球军事热点"
    assert calls == []


def test_any_failed_stage_stops_following_stages(tmp_path):
    write_discovery_output(tmp_path)
    calls = []
    result = make_adapter(calls, {"SourceRanker": "FAILED"}).run(str(tmp_path))
    assert result["status"] == "FAILED"
    assert result["failed_stage"] == "source_ranker"
    assert [call[0] for call in calls] == ["NewsVerifier", "SourceRanker"]


def test_stage_exception_returns_failure_and_stops_pipeline(tmp_path):
    write_discovery_output(tmp_path)
    calls = []
    result = make_adapter(calls, {"TopicScorer": "RAISE"}).run(str(tmp_path))
    assert result["status"] == "FAILED"
    assert "TopicScorer failed" in result["error"]
    assert [call[0] for call in calls] == ["NewsVerifier", "SourceRanker", "TopicScorer"]


def test_missing_or_invalid_topic_never_enters_pipeline(tmp_path):
    write_discovery_output(tmp_path, topic="未知主题")
    calls = []
    result = make_adapter(calls).run(str(tmp_path))
    assert result["status"] == "FAILED"
    assert calls == []


def test_missing_project_path_fails_without_agent_calls():
    calls = []
    result = make_adapter(calls).run("")
    assert result["status"] == "FAILED"
    assert calls == []


def test_default_selector_receives_projects_root(tmp_path):
    write_discovery_output(tmp_path)
    adapter = DiscoveryPipelineAdapter()

    agents = adapter._get_agents(str(tmp_path))

    assert agents[1].project_path == str(tmp_path)
    assert agents[2].project_path == str(tmp_path)
    assert agents[3].project_path == os.path.dirname(str(tmp_path))