import json
import os

from src.agents.news_agent import NewsAgent
from src.agents.news_verifier import NewsVerifier
from src.agents.source_ranker import SourceRanker
from src.agents.topic_scorer import TopicScorer
from src.agents.topic_selector import TopicSelector
from src.utils.ai_model_client import AIModelClient
from src.agents.news_discovery import NewsDiscovery


class FailedAIClient:
    model = "test-model"

    def analyze(self, prompt):
        return {
            "status": "FAILED",
            "model": self.model,
            "provider_error": "provider unavailable",
            "content": "",
        }


def make_news_project(tmp_path, articles):
    news_dir = tmp_path / "01_新闻资料"
    news_dir.mkdir(parents=True)
    data = {
        "schema_version": "2.1",
        "status": "SUCCESS",
        "topic": "全球军事热点",
        "articles": articles,
    }
    (news_dir / "news_articles.json").write_text(
        json.dumps(data, ensure_ascii=False), encoding="utf-8"
    )


def article(source_id="source_reuters", source="Reuters", content=None, summary=None):
    return {
        "article_id": "ND-1",
        "source_id": source_id,
        "title": "真实标题",
        "source": source,
        "url": "https://example.com/news",
        "published_at": "2026-08-22T10:00:00+00:00",
        "content": content,
        "summary": summary,
    }


def test_ai_client_returns_explicit_failure_for_unsupported_provider():
    client = AIModelClient.__new__(AIModelClient)
    client.provider = "unsupported"
    client.model = "test-model"

    result = client.analyze("test prompt")

    assert result["status"] == "FAILED"
    assert "provider_error" in result


def test_news_verifier_persists_ai_failure_and_preserves_source_id(tmp_path):
    make_news_project(tmp_path, [article(content="真实正文")])
    verifier = NewsVerifier()
    verifier.ai_client = FailedAIClient()

    result = verifier.run({"project_path": str(tmp_path)})

    assert result["status"] == "SUCCESS"
    verification = json.loads(
        (tmp_path / "02_事实核验" / "verification.json").read_text(encoding="utf-8")
    )
    ai_data = json.loads(
        (tmp_path / "02_事实核验" / "ai_verification.json").read_text(encoding="utf-8")
    )
    assert verification["articles"][0]["source_id"] == "source_reuters"
    assert verification["articles"][0]["content"] == "真实正文"
    assert verification["ai_verification_status"] == "AI_ANALYSIS_FAILED"
    assert verification["confidence"] == "LOW"
    assert ai_data["status"] == "AI_ANALYSIS_FAILED"
    assert ai_data["provider_error"] == "provider unavailable"


def test_news_discovery_creates_stable_source_id():
    agent = NewsDiscovery()
    agent._current_request = {"topic": "全球军事热点", "domain": "军事"}

    candidate = agent._normalize_candidate(
        article(source="Reuters"),
        [{"query": "q", "query_index": 1, "priority": 1}],
        "2026-08-22T10:00:00+00:00",
        1,
    )

    assert candidate["source_id"] == "source_reuters"


def test_news_agent_does_not_turn_missing_content_into_title():
    agent = NewsAgent()

    normalized = agent._normalize_article({
        "title": "真实标题",
        "source": "Reuters",
        "url": "https://example.com/news",
        "published_time": "2026-08-22T10:00:00+00:00",
        "content": None,
        "summary": None,
    }, 0)

    assert normalized["content"] is None
    assert normalized["summary"] is None
    assert normalized["content_available"] is False
    assert normalized["summary_available"] is False
    assert normalized["content"] != normalized["title"]
    assert normalized["summary"] != normalized["title"]


def test_source_ranker_preserves_source_id_and_maps_alias_category(tmp_path):
    verification_dir = tmp_path / "02_事实核验"
    verification_dir.mkdir(parents=True)
    verification = {
        "topic": "全球军事热点",
        "articles": [
            {"source_id": "source_reuters", "source": "Reuters"},
            {"source_id": "source_reuters", "source": "Reuters"},
        ],
    }
    (verification_dir / "verification.json").write_text(
        json.dumps(verification, ensure_ascii=False), encoding="utf-8"
    )

    result = SourceRanker(project_path=str(tmp_path)).run({})

    source = result["result"]["sources"][0]
    assert source["source_id"] == "source_reuters"
    assert source["source_type"] == "国际通讯社"
    assert source["source_credibility_score"] == 95
    assert source["cross_source_verification_score"] == 70
    assert source["source_credibility_score"] != source["cross_source_verification_score"]


def test_topic_scorer_marks_missing_content_and_failed_ai(tmp_path):
    make_news_project(tmp_path, [article(content=None, summary=None)])
    verification_dir = tmp_path / "02_事实核验"
    verification_dir.mkdir(exist_ok=True)
    (verification_dir / "verification.json").write_text(json.dumps({
        "topic": "全球军事热点",
        "articles": [{
            "source_id": "source_reuters",
            "source": "Reuters",
            "published_at": None,
            "content": None,
        }],
        "ai_verification_status": "AI_ANALYSIS_FAILED",
    }, ensure_ascii=False), encoding="utf-8")
    rank_dir = tmp_path / "03_来源评级"
    rank_dir.mkdir()
    (rank_dir / "source_rank.json").write_text(json.dumps({
        "topic": "全球军事热点",
        "sources": [{
            "source_id": "source_reuters",
            "source_type": "国际通讯社",
            "source_credibility_score": 95,
            "cross_source_verification_score": 50,
        }],
    }, ensure_ascii=False), encoding="utf-8")

    result = TopicScorer(project_path=str(tmp_path)).run({
        "project_path": str(tmp_path),
        "topic": "全球军事热点",
    })

    data = result["result"]
    assert data["data_quality"]["status"] == "DEGRADED"
    assert data["data_quality"]["ai_verification_failed"] is True
    assert data["data_quality"]["missing_content"] == 1
    assert "AI事实核验失败" in data["reason"]


def test_topic_selector_exposes_reject_production_decision(tmp_path):
    project_dir = tmp_path / "candidate"
    score_dir = project_dir / "04_热点评分"
    score_dir.mkdir(parents=True)
    (score_dir / "topic_score.json").write_text(json.dumps({
        "topic": "美国航母部署",
        "score": 52,
        "recommendation": "不制作",
        "breakdown": {},
    }, ensure_ascii=False), encoding="utf-8")

    result = TopicSelector().run({"project_path": str(tmp_path)})

    data = result["result"]
    assert data["selected_topic"] == "美国航母部署"
    assert data["production_decision"] == "REJECT"
    assert data["selection_score"] == 52


def test_topic_selector_excludes_unknown_topic_fallback(tmp_path):
    project_dir = tmp_path / "unknown_candidate"
    score_dir = project_dir / "04_热点评分"
    score_dir.mkdir(parents=True)
    (score_dir / "topic_score.json").write_text(json.dumps({
        "score": 99,
        "recommendation": "制作",
        "breakdown": {},
    }, ensure_ascii=False), encoding="utf-8")

    selector = TopicSelector()
    assert selector.collect_candidates(str(tmp_path)) == []
