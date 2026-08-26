import json

from src.agents.script_agent import ScriptAgent


def _project(tmp_path, selected_topic="美国航母最新部署", decision="进入制作"):
    paths = [
        tmp_path / "05_选题决策",
        tmp_path / "02_事实核验",
        tmp_path / "03_来源评级",
    ]
    for path in paths:
        path.mkdir()

    (paths[0] / "topic_selection.json").write_text(
        json.dumps({
            "selected_topic": selected_topic,
            "decision": decision,
            "selection_score": 88,
            "reason": ["来源可靠"],
        }, ensure_ascii=False),
        encoding="utf-8",
    )
    (paths[1] / "verification.json").write_text(
        json.dumps({"verification_status": "VERIFIED"}, ensure_ascii=False),
        encoding="utf-8",
    )
    (paths[2] / "source_rank.json").write_text(
        json.dumps({"sources": [{"source_id": "src-001", "name": "Reuters"}]}, ensure_ascii=False),
        encoding="utf-8",
    )


def test_script_agent_success(tmp_path):
    _project(tmp_path)
    response = ScriptAgent(project_path=str(tmp_path)).run({})

    assert response["status"] == "SUCCESS"
    assert response["schema_version"] == "script.v2.0"
    assert response["selected_topic"] == "美国航母最新部署"
    assert (tmp_path / "06_脚本" / "script.json").exists()
    assert (tmp_path / "06_脚本" / "script.md").exists()


def test_missing_selection_fails(tmp_path):
    _project(tmp_path)
    (tmp_path / "05_选题决策" / "topic_selection.json").unlink()
    response = ScriptAgent(project_path=str(tmp_path)).run({})
    assert response["status"] == "FAILED"


def test_missing_selected_topic_fails(tmp_path):
    _project(tmp_path)
    (tmp_path / "05_选题决策" / "topic_selection.json").write_text(
        json.dumps({"decision": "进入制作"}), encoding="utf-8"
    )
    response = ScriptAgent(project_path=str(tmp_path)).run({})
    assert response["status"] == "FAILED"


def test_rejected_decision_fails(tmp_path):
    _project(tmp_path, decision="不制作")
    response = ScriptAgent(project_path=str(tmp_path)).run({})
    assert response["status"] == "FAILED"


def test_multi_selection_fails(tmp_path):
    _project(tmp_path)
    (tmp_path / "05_选题决策" / "topic_selection.json").write_text(
        json.dumps({"selected_topic": ["A", "B"], "decision": "进入制作"}), encoding="utf-8"
    )
    response = ScriptAgent(project_path=str(tmp_path)).run({})
    assert response["status"] == "FAILED"


def test_missing_verification_fails(tmp_path):
    _project(tmp_path)
    (tmp_path / "02_事实核验" / "verification.json").unlink()
    response = ScriptAgent(project_path=str(tmp_path)).run({})
    assert response["status"] == "FAILED"


def test_missing_source_rank_fails(tmp_path):
    _project(tmp_path)
    (tmp_path / "03_来源评级" / "source_rank.json").unlink()
    response = ScriptAgent(project_path=str(tmp_path)).run({})
    assert response["status"] == "FAILED"


def test_ai_provider_failure_is_failed(tmp_path):
    _project(tmp_path)

    class FailingAIClient:
        def generate(self, prompt):
            raise RuntimeError("provider unavailable")

    response = ScriptAgent(
        project_path=str(tmp_path),
        ai_client=FailingAIClient(),
    ).run({})

    assert response["status"] == "FAILED"
    assert "provider unavailable" in response["error"]
    assert not (tmp_path / "06_脚本" / "script.json").exists()


def test_fact_references_are_written(tmp_path):
    _project(tmp_path)
    response = ScriptAgent(project_path=str(tmp_path)).run({})
    assert response["fact_references"]
    assert response["fact_references"][0]["source_id"] == "src-001"


def test_title_is_not_body(tmp_path):
    _project(tmp_path)
    response = ScriptAgent(project_path=str(tmp_path)).run({})
    body = next(item["text"] for item in response["sections"] if item["type"] == "BODY")
    assert body != response["title"]


def test_output_can_feed_storyboard_contract(tmp_path):
    _project(tmp_path)
    response = ScriptAgent(project_path=str(tmp_path)).run({})
    assert all("section_id" in section and "type" in section and "text" in section for section in response["sections"])
