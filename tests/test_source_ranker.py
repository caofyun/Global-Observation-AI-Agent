import sys
import os
import json


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from src.agents.source_ranker import SourceRanker


def test_source_ranker_normalizes_and_collects_sources():
    ranker = SourceRanker()

    data = {
        "sources": [
            {"source_name": "Reuters"},
            {"source": "AP"},
        ],
        "articles": [
            {"source": "Reuters"},
            {"source": "BBC", "source_id": "source_bbc"},
        ],
    }

    assert ranker.normalize_source(" Reuters ") == "Reuters"
    assert ranker.collect_source_names(data) == [
        "Reuters",
        "AP",
        "Reuters",
        "BBC",
    ]


def test_source_ranker_scoring_rules():
    ranker = SourceRanker()

    assert ranker.calculate_verification_score(1) == 50
    assert ranker.calculate_verification_score(2) == 70
    assert ranker.calculate_verification_score(3) == 85
    assert ranker.calculate_verification_score(5) == 100

    assert ranker.convert_rank(90) == "A"
    assert ranker.convert_rank(75) == "B"
    assert ranker.convert_rank(60) == "C"
    assert ranker.convert_rank(40) == "D"


def test_source_ranker_executes_without_interactive_input(tmp_path):
    project_path = tmp_path / "source_ranker_project"
    verification_dir = project_path / "02_事实核验"
    verification_dir.mkdir(parents=True)

    verification_path = verification_dir / "verification.json"
    verification_path.write_text(
        json.dumps(
            {
                "topic": "测试主题",
                "articles": [
                    {
                        "source": "Reuters",
                        "source_id": "source_reuters",
                    },
                    {
                        "source": "Reuters",
                        "source_id": "source_reuters",
                    },
                ],
                "sources": [],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    ranker = SourceRanker(project_path=str(project_path))
    result = ranker.run({})

    assert result["topic"] == "测试主题"
    assert len(result["sources"]) == 1
    assert result["sources"][0]["source_id"] == "source_reuters"
    assert (
        project_path
        / "03_来源评级"
        / "source_rank.json"
    ).exists()
