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


def test_news_agent_v2_project_output(tmp_path):
    project_path = tmp_path / "news_agent_v2_project"
    agent = NewsAgent(project_path=str(project_path))
    agent.search_tool = FakeSearchTool()

    result = agent.run({
        "topic_keyword": "美国航母部署"
    })

    assert result["topic_keyword"] == "美国航母部署"
    assert len(result["search_keywords"]) == 3
    assert len(result["news_articles"]) == 3

    articles_path = (
        project_path
        / "01_新闻资料"
        / "news_articles.json"
    )

    assert articles_path.exists()


def test_news_agent_v2_rejects_empty_topic():
    agent = NewsAgent()

    try:
        agent.run({"topic_keyword": ""})
    except Exception as exc:
        assert "topic_keyword" in str(exc)
    else:
        raise AssertionError("empty topic should fail")
