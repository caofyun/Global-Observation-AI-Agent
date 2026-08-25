import os
import sys
import json


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)


from src.agents.topic_scorer import TopicScorer


if __name__ == "__main__":

    print("==============================")
    print("测试 TopicScorer V2.0")
    print("==============================")


    project_path = r".\projects\test_v2_pipeline_project"


    agent = TopicScorer()


    result = agent.run(
        {
            "project_path": project_path
        }
    )


    print()
    print("测试结果：")
    print(result)


    output_file = os.path.join(
        project_path,
        "04_热点评分",
        "topic_score.json"
    )


    print()
    print("检查输出文件:")
    print(output_file)

    print(
        "存在:",
        os.path.exists(output_file)
    )


def test_topic_scorer_runs_and_outputs_file(tmp_path):
    """TopicScorer test must be self-contained and not depend on an absent repo fixture."""
    project_path = tmp_path / "topic_scorer_project"
    verification_dir = project_path / "02_事实核验"
    source_rank_dir = project_path / "03_来源评级"
    verification_dir.mkdir(parents=True)
    source_rank_dir.mkdir(parents=True)

    verification = {
        "topic": "测试主题",
        "articles": [
            {
                "title": "测试新闻",
                "source": "Reuters",
                "source_id": "source_reuters",
                "published_time": "Mon, 25 Aug 2026 10:00:00 GMT",
                "content": "测试正文",
            }
        ],
        "verification_status": "MULTIPLE_SOURCES_FOUND",
        "confidence": "HIGH",
    }

    source_rank = {
        "topic": "测试主题",
        "sources": [
            {
                "source_id": "source_reuters",
                "source_name": "Reuters",
                "source_credibility_score": 90,
                "cross_source_verification_score": 70,
                "credibility_score": 90,
                "verification_score": 70,
                "source_rank": "A",
            }
        ],
    }

    (verification_dir / "verification.json").write_text(
        json.dumps(verification, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )
    (source_rank_dir / "source_rank.json").write_text(
        json.dumps(source_rank, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )

    scorer = TopicScorer()
    result = scorer.run({"project_path": str(project_path)})

    assert result["status"] == "SUCCESS"

    output_path = project_path / "04_热点评分" / "topic_score.json"
    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))

    assert data["topic"] == "测试主题"
    assert "score" in data
    assert "recommendation" in data
    assert "breakdown" in data
    assert isinstance(data["breakdown"], dict)
