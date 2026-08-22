from datetime import datetime, timezone
import json

import pytest

from src.agents.news_discovery import NewsDiscovery


NOW = datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc)
REQUEST = {
    "domain": "军事",
    "topic": "全球军事热点",
    "time_range": "24h",
    "geographic_scope": ["美国", "中东"],
    "focus_areas": ["航母", "军事部署"],
    "max_candidates": 10,
}


class FakeSearchTool:
    def __init__(self, results_by_query):
        self.results_by_query = results_by_query
        self.calls = []

    def search(self, keyword, max_results=10):
        self.calls.append((keyword, max_results))
        base_keyword = keyword.rsplit(" when:", 1)[0]
        return self.results_by_query.get(keyword, self.results_by_query.get(base_keyword, []))


def result(title="标题", source="来源", url="https://example.com/news", published_time="2026-08-22T10:00:00+00:00"):
    return {
        "title": title,
        "source": source,
        "url": url,
        "published_time": published_time,
    }


def make_agent(results_by_query=None, project_path=None):
    return NewsDiscovery(
        project_path=project_path,
        search_tool=FakeSearchTool(results_by_query or {}),
        now_provider=lambda: NOW,
    )


def test_normal_discovery_returns_v21_object_and_writes_file(tmp_path):
    agent = make_agent({"全球军事热点": [result()]}, str(tmp_path))

    output = agent.run(REQUEST)

    assert output["status"] == "SUCCESS"
    data = output["result"]
    assert data["schema_version"] == "2.1"
    assert data["topic"] == REQUEST["topic"]
    assert data["articles"][0]["topic"] == REQUEST["topic"]
    output_path = tmp_path / "01_新闻资料" / "news_articles.json"
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == data


def test_missing_topic_fails():
    agent = make_agent()
    request = {**REQUEST}
    del request["topic"]

    output = agent.run(request)

    assert output["status"] == "FAILED"
    assert "topic" in output["error"]


def test_empty_topic_fails():
    agent = make_agent()

    output = agent.run({**REQUEST, "topic": "   "})

    assert output["status"] == "FAILED"


@pytest.mark.parametrize("time_range", ["", "2h", "30d", None])
def test_invalid_time_range_fails(time_range):
    output = make_agent().run({**REQUEST, "time_range": time_range})

    assert output["status"] == "FAILED"


@pytest.mark.parametrize("max_candidates", [0, -1, 1.5, True, "2", None])
def test_invalid_max_candidates_fails(max_candidates):
    output = make_agent().run({**REQUEST, "max_candidates": max_candidates})

    assert output["status"] == "FAILED"


def test_query_planner_generates_dynamic_queries_with_schema():
    agent = make_agent()

    queries = agent.build_search_queries(REQUEST)

    assert len(queries) > 5
    assert [item["query_index"] for item in queries] == list(range(1, len(queries) + 1))
    assert all(set(item) == {"query", "category", "priority", "query_index"} for item in queries)


def test_search_tool_is_called_for_every_query():
    fake = FakeSearchTool({})
    agent = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW)

    agent.run(REQUEST)

    assert len(fake.calls) == 7
    assert all(max_results == 10 for _, max_results in fake.calls)


def test_raw_results_counts_all_search_results():
    fake = FakeSearchTool({"全球军事热点": [result("一"), result("二")]})
    output = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run(REQUEST)

    assert output["result"]["statistics"]["raw_results"] == 2


def test_time_range_filters_old_results():
    fake = FakeSearchTool({
        "全球军事热点": [
            result("新", url="https://example.com/new"),
            result("旧", url="https://example.com/old", published_time="2026-08-20T11:59:00+00:00"),
        ]
    })

    data = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run(REQUEST)["result"]

    assert [article["title"] for article in data["articles"]] == ["新"]


def test_missing_published_at_does_not_enter_articles():
    fake = FakeSearchTool({"全球军事热点": [result("无日期", published_time="")]})

    data = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run(REQUEST)["result"]

    assert data["articles"] == []
    assert data["statistics"]["raw_results"] == 1


@pytest.mark.parametrize("field", ["title", "source", "url"])
def test_basic_validity_filter(field):
    invalid = result()
    invalid[field] = ""
    fake = FakeSearchTool({"全球军事热点": [invalid]})

    data = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run(REQUEST)["result"]

    assert data["articles"] == []


def test_invalid_url_is_filtered():
    fake = FakeSearchTool({"全球军事热点": [result(url="not-a-url")]})

    data = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run(REQUEST)["result"]

    assert data["articles"] == []


def test_url_normalization_deduplicates_and_merges_queries():
    fake = FakeSearchTool({
        "全球军事热点": [result("同一报道", url="HTTPS://EXAMPLE.COM/news#part")],
        "军事 全球军事热点": [result("同一报道", url="https://example.com/news/")],
    })
    data = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run(REQUEST)["result"]

    assert data["statistics"]["deduplicated_results"] == 1
    assert len(data["articles"][0]["queries"]) == 2


def test_title_normalization_deduplicates_different_urls():
    fake = FakeSearchTool({
        "全球军事热点": [result("  同一   报道 ", url="https://example.com/a")],
        "军事 全球军事热点": [result("同一 报道", url="https://example.com/b")],
    })
    data = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run(REQUEST)["result"]

    assert data["statistics"]["deduplicated_results"] == 1


def test_primary_query_uses_priority_then_query_index():
    fake = FakeSearchTool({
        "全球军事热点": [result("同一", url="https://example.com/a")],
        "美国 全球军事热点": [result("同一", url="https://example.com/b")],
    })
    data = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run(REQUEST)["result"]

    article = data["articles"][0]
    assert article["query"] == "全球军事热点 when:1d"
    assert article["query"] in article["queries"]


def test_max_candidates_only_limits_final_articles():
    results = [result(str(index), url=f"https://example.com/{index}") for index in range(4)]
    fake = FakeSearchTool({"全球军事热点": results})
    data = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run({**REQUEST, "max_candidates": 2})["result"]

    statistics = data["statistics"]
    assert statistics == {"raw_results": 4, "deduplicated_results": 4, "final_candidates": 2}
    assert len(data["articles"]) == 2


def test_statistics_relationship_is_preserved():
    fake = FakeSearchTool({"全球军事热点": [result(str(index), url=f"https://example.com/{index}") for index in range(3)]})
    statistics = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run({**REQUEST, "max_candidates": 2})["result"]["statistics"]

    assert statistics["final_candidates"] <= statistics["deduplicated_results"] <= statistics["raw_results"]


def test_article_fields_and_content_summary_rules():
    fake = FakeSearchTool({"全球军事热点": [result()]})
    article = NewsDiscovery(search_tool=fake, now_provider=lambda: NOW).run(REQUEST)["result"]["articles"][0]

    assert set(article) == {
        "article_id", "domain", "topic", "query", "queries", "title", "source", "source_id",
        "url", "published_at", "discovered_at", "summary", "content", "discovery_status",
    }
    assert article["summary"] is None
    assert article["content"] is None
    assert article["content"] != article["title"]
    assert article["summary"] != article["title"]
    assert article["discovery_status"] == "DISCOVERED"


def test_empty_results_are_success():
    data = make_agent().run(REQUEST)["result"]

    assert data["status"] == "SUCCESS"
    assert data["articles"] == []
    assert data["statistics"] == {"raw_results": 0, "deduplicated_results": 0, "final_candidates": 0}


def test_top_level_structure_and_query_count():
    data = make_agent().run(REQUEST)["result"]

    assert set(data) == {
        "schema_version", "status", "domain", "topic", "discovery", "statistics", "articles",
    }
    assert data["discovery"]["query_count"] == len(data["discovery"]["search_queries"])
