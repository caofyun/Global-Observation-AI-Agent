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
    # Use the existing sample project in the repo
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    project_path = os.path.join(repo_root, "projects", "test_v2_pipeline_project")

    scorer = TopicScorer()

    result = scorer.run({"project_path": project_path})

    assert result["status"] == "SUCCESS"

    output_path = os.path.join(project_path, "04_热点评分", "topic_score.json")
    assert os.path.exists(output_path)

    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # basic schema checks
    assert "score" in data
    assert "recommendation" in data
    assert "breakdown" in data
    assert isinstance(data["breakdown"], dict)
