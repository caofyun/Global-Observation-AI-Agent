import json
from pathlib import Path


def test_pipeline_json_contract(tmp_path):
    project = Path(tmp_path)

    news_dir = project / "01_新闻资料"
    verification_dir = project / "02_事实核验"
    rank_dir = project / "03_来源评级"
    score_dir = project / "04_热点评分"
    selection_dir = project / "05_选题决策"

    for directory in (
        news_dir,
        verification_dir,
        rank_dir,
        score_dir,
        selection_dir,
    ):
        directory.mkdir(parents=True)

    (news_dir / "news_articles.json").write_text(
        json.dumps(
            {"schema_version": "2.0", "topic": "测试主题", "articles": []},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (verification_dir / "verification.json").write_text(
        json.dumps(
            {
                "topic": "测试主题",
                "articles": [],
                "sources": [],
                "facts": [],
                "conflicts": [],
                "uncertainties": [],
                "verification_status": "NO_VALID_SOURCE",
                "confidence": "LOW",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (rank_dir / "source_rank.json").write_text(
        json.dumps(
            {"topic": "测试主题", "sources": []},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (score_dir / "topic_score.json").write_text(
        json.dumps({"topic": "测试主题", "score": 8}, ensure_ascii=False),
        encoding="utf-8",
    )
    (selection_dir / "topic_selection.json").write_text(
        json.dumps(
            {"selected_topic": "测试主题", "score": 8},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    contracts = {
        "01_新闻资料/news_articles.json": ["topic", "articles"],
        "02_事实核验/verification.json": [
            "topic",
            "articles",
            "sources",
            "facts",
            "conflicts",
            "uncertainties",
            "verification_status",
            "confidence",
        ],
        "03_来源评级/source_rank.json": ["topic", "sources"],
        "04_热点评分/topic_score.json": ["topic", "score"],
        "05_选题决策/topic_selection.json": ["selected_topic", "score"],
    }

    for relative_path, fields in contracts.items():
        data = json.loads((project / relative_path).read_text(encoding="utf-8"))
        for field in fields:
            assert field in data, f"{relative_path} missing field: {field}"


def test_topic_score_to_selection_data_flow(tmp_path):
    project = Path(tmp_path)
    verification_dir = project / "02_事实核验"
    rank_dir = project / "03_来源评级"
    verification_dir.mkdir(parents=True)
    rank_dir.mkdir(parents=True)

    (verification_dir / "verification.json").write_text(
        json.dumps(
            {
                "topic": "测试主题",
                "articles": [
                    {
                        "source": "Reuters",
                        "source_id": "source_reuters",
                        "content": "测试正文",
                    }
                ],
                "sources": [],
                "facts": [],
                "conflicts": [],
                "uncertainties": [],
                "verification_status": "SINGLE_SOURCE",
                "confidence": "MEDIUM",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (rank_dir / "source_rank.json").write_text(
        json.dumps(
            {
                "topic": "测试主题",
                "sources": [
                    {
                        "source_id": "source_reuters",
                        "source_name": "Reuters",
                        "source_credibility_score": 90,
                        "cross_source_verification_score": 50,
                        "credibility_score": 90,
                        "verification_score": 50,
                        "source_rank": "A",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    from src.agents.topic_scorer import TopicScorer
    from src.agents.topic_selector import TopicSelector

    scorer = TopicScorer(project_path=str(project))
    score_result = scorer.run({"project_path": str(project), "topic": "测试主题"})

    assert score_result["status"] == "SUCCESS"
    score_data = json.loads(
        (project / "04_热点评分" / "topic_score.json").read_text(encoding="utf-8")
    )
    assert score_data["topic"] == "测试主题"
    assert isinstance(score_data["score"], int)

    selector = TopicSelector(project_path=str(project))
    selection_result = selector.run({"project_path": str(project), "mode": "single", "top_n": 1})

    assert selection_result["status"] == "SUCCESS"
    selection_data = json.loads(
        (project / "05_选题决策" / "topic_selection.json").read_text(encoding="utf-8")
    )
    assert selection_data["selected_topic"] == "测试主题"
    assert selection_data["score"] == score_data["score"]
