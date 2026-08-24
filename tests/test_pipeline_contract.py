import json
from pathlib import Path


def test_pipeline_json_contract(tmp_path):
    project = Path(tmp_path)

    news_dir = project / "01_新闻资料"
    score_dir = project / "04_热点评分"
    selection_dir = project / "05_选题决策"
    news_dir.mkdir(parents=True)
    score_dir.mkdir(parents=True)
    selection_dir.mkdir(parents=True)

    (news_dir / "news_articles.json").write_text(
        json.dumps({"schema_version": "2.0", "topic": "测试主题", "articles": []}, ensure_ascii=False),
        encoding="utf-8",
    )
    (score_dir / "topic_score.json").write_text(
        json.dumps({"topic": "测试主题", "score": 8}, ensure_ascii=False),
        encoding="utf-8",
    )
    (selection_dir / "topic_selection.json").write_text(
        json.dumps({"selected_topic": "测试主题", "score": 8}, ensure_ascii=False),
        encoding="utf-8",
    )

    contracts = {
        "01_新闻资料/news_articles.json": ["topic", "articles"],
        "04_热点评分/topic_score.json": ["topic", "score"],
        "05_选题决策/topic_selection.json": ["selected_topic", "score"],
    }

    for relative_path, fields in contracts.items():
        data = json.loads((project / relative_path).read_text(encoding="utf-8"))
        for field in fields:
            assert field in data, f"{relative_path} missing field: {field}"
