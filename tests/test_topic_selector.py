import os
import sys
import json
import tempfile


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)


from src.agents.topic_selector import TopicSelector


def make_project(root_dir, name, topic, score, recommendation, breakdown=None):
    project_dir = os.path.join(root_dir, name)
    os.makedirs(os.path.join(project_dir, "04_热点评分"), exist_ok=True)
    data = {
        "topic": topic,
        "score": score,
        "recommendation": recommendation,
        "breakdown": breakdown or {
            "international_influence": 80,
            "news_hotness": 85,
            "user_interest": 70,
            "video_potential": 75,
            "source_quality": 65
        }
    }
    path = os.path.join(project_dir, "04_热点评分", "topic_score.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return project_dir


def main():
    # create a temporary projects root
    with tempfile.TemporaryDirectory() as tmpdir:
        # Project A
        make_project(
            tmpdir,
            "20260821_美国航母部署",
            "美国航母部署动态",
            85,
            "制作"
        )

        # Project B
        make_project(
            tmpdir,
            "20260821_霍尔木兹风险",
            "霍尔木兹海峡风险",
            78,
            "观望"
        )

        selector = TopicSelector()
        res = selector.run({"project_path": tmpdir})

        assert res["status"] == "SUCCESS"

        out_path = os.path.join(tmpdir, "05_选题决策", "topic_selection.json")
        assert os.path.exists(out_path), "topic_selection.json not generated"

        with open(out_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # checks
        assert "ranking" in data and len(data["ranking"]) >= 2
        assert data["selected_topic"] == "美国航母部署动态"

        print("TopicSelector V2.0 Test Success")


if __name__ == "__main__":
    main()
