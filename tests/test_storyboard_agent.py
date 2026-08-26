import json

from src.agents.storyboard_agent import StoryboardAgent


def _write_script(project, **overrides):
    script = {
        "schema_version": "script.v2.0",
        "status": "SUCCESS",
        "selected_topic": "测试主题",
        "title": "测试主题",
        "duration_target_seconds": 90,
        "script_segments": [
            {
                "script_segment_id": "SEG-001",
                "text": "第一段旁白",
                "duration_seconds": 8,
                "visual_description": "新闻现场",
                "material_type": "news_footage",
                "subtitle": "第一段旁白",
                "fact_references": [{"claim_id": "claim-001"}],
            },
            {
                "script_segment_id": "SEG-002",
                "text": "第二段旁白",
                "duration_seconds": 7,
            },
        ],
        "fact_references": [{"claim_id": "claim-001", "source_id": "source-001"}],
        "human_confirmation": {"approved": True},
    }
    script.update(overrides)
    output = project / "06_脚本" / "script.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(script, ensure_ascii=False), encoding="utf-8")


def test_generates_storyboard(tmp_path):
    _write_script(tmp_path)
    result = StoryboardAgent(project_path=str(tmp_path)).run({})
    assert result["status"] == "SUCCESS"
    assert result["total_duration_seconds"] == 15
    assert result["scenes"][0]["script_segment_id"] == "SEG-001"
    assert (tmp_path / "07_分镜" / "storyboard.json").is_file()


def test_missing_script_fails(tmp_path):
    result = StoryboardAgent(project_path=str(tmp_path)).run({})
    assert result["status"] == "FAILED"


def test_upstream_failed_fails(tmp_path):
    _write_script(tmp_path, status="FAILED")
    result = StoryboardAgent(project_path=str(tmp_path)).run({})
    assert result["status"] == "FAILED"


def test_unconfirmed_script_fails(tmp_path):
    _write_script(tmp_path, human_confirmation={"approved": False})
    result = StoryboardAgent(project_path=str(tmp_path)).run({})
    assert result["status"] == "FAILED"


def test_missing_segments_fails(tmp_path):
    _write_script(tmp_path, script_segments=[])
    result = StoryboardAgent(project_path=str(tmp_path)).run({})
    assert result["status"] == "FAILED"


def test_timeline_matches_scene_sum(tmp_path):
    _write_script(tmp_path)
    result = StoryboardAgent(project_path=str(tmp_path)).run({})
    assert result["total_duration_seconds"] == sum(
        scene["duration_seconds"] for scene in result["scenes"]
    )


def test_ai_provider_failure_is_failed(tmp_path):
    _write_script(tmp_path)

    class BrokenAI:
        def generate(self, prompt):
            raise RuntimeError("provider unavailable")

    result = StoryboardAgent(project_path=str(tmp_path), ai_client=BrokenAI()).run({})
    assert result["status"] == "FAILED"
    assert "provider unavailable" in result["error"]
    assert not (tmp_path / "07_分镜" / "storyboard.json").exists()


def test_no_zero_duration_scene(tmp_path):
    _write_script(tmp_path)
    script_path = tmp_path / "06_脚本" / "script.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    script["script_segments"][0]["duration_seconds"] = 0
    script_path.write_text(json.dumps(script, ensure_ascii=False), encoding="utf-8")
    result = StoryboardAgent(project_path=str(tmp_path)).run({})
    assert result["status"] == "FAILED"
