import sys
import os


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from src.agents.news_agent import NewsAgent


class FakeSearchTool:
    def search(self, keyword, max_results=10):
        return [
            {
                "title": f"{keyword} headline",
                "source": "Test Source",
                "published_time": "2026-08-24",
                "url": f"https://example.com/{keyword}",
                "snippet": "test snippet",
            }
        ]


def test_news_agent_builds_search_keywords():
    agent = NewsAgent()

    assert agent.build_search_keywords("美国航母部署") == [
        "美国航母部署",
        "美国航母部署 最新消息",
        "美国航母部署 news",
    ]
    assert agent.build_search_keywords("  ") == []


def test_news_agent_normalizes_article():
    agent = NewsAgent()

    article = agent._normalize_article(
        {
            "title": "Test title",
            "source": "Test Source",
            "url": "https://example.com/news",
            "published_time": "2026-08-24",
            "snippet": "Test summary",
        },
        0,
    )

    assert article["article_id"] == "article_1"
    assert article["title"] == "Test title"
    assert article["summary"] == "Test summary"
    assert article["content"] is None
    assert article["content_available"] is False
    assert article["summary_available"] is True


def test_news_agent_runs_without_interactive_input(tmp_path):
    project_path = tmp_path / "news_agent_project"
    agent = NewsAgent(project_path=str(project_path))
    agent.search_tool = FakeSearchTool()

    result = agent.run({"topic_keyword": "测试新闻"})

    assert result["topic_keyword"] == "测试新闻"
    assert len(result["search_results"]) == 3
    assert len(result["news_articles"]) == 3
    assert (project_path / "01_新闻资料" / "search_results.json").exists()
    assert (project_path / "01_新闻资料" / "news_articles.json").exists()
