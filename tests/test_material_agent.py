import json
from src.agents.material_agent import MaterialAgent

def _write_storyboard(project, **overrides):
    data={"schema_version":"storyboard.v2.0","status":"SUCCESS","topic":"测试主题","scenes":[{"scene_id":"SCENE-001","script_segment_id":"SEG-001","duration_seconds":8,"visual":{"description":"新闻现场","material_type":"news_footage"},"fact_references":[{"claim_id":"claim-001"}]},{"scene_id":"SCENE-002","script_segment_id":"SEG-002","duration_seconds":7,"visual":{"description":"地图位置","material_type":"map"}}],"fact_references":[{"claim_id":"claim-001","source_id":"source-001"}]}
    data.update(overrides); p=project/"07_分镜"/"storyboard.json"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")

def test_generates_material_plan(tmp_path):
    _write_storyboard(tmp_path); r=MaterialAgent(project_path=str(tmp_path)).run({}); assert r["status"]=="SUCCESS"; assert r["statistics"]["asset_request_count"]==2; assert (tmp_path/"08_素材"/"material_plan.json").is_file()

def test_missing_storyboard_fails(tmp_path): assert MaterialAgent(project_path=str(tmp_path)).run({})["status"]=="FAILED"

def test_upstream_failed_fails(tmp_path):
    _write_storyboard(tmp_path,status="FAILED"); assert MaterialAgent(project_path=str(tmp_path)).run({})["status"]=="FAILED"

def test_missing_scenes_fails(tmp_path):
    _write_storyboard(tmp_path,scenes=[]); assert MaterialAgent(project_path=str(tmp_path)).run({})["status"]=="FAILED"

def test_unknown_material_type_fails(tmp_path):
    _write_storyboard(tmp_path); p=tmp_path/"07_分镜"/"storyboard.json"; d=json.loads(p.read_text()); d["scenes"][0]["visual"]["material_type"]="unknown"; p.write_text(json.dumps(d),encoding="utf-8"); assert MaterialAgent(project_path=str(tmp_path)).run({})["status"]=="FAILED"

def test_traceability_is_preserved(tmp_path):
    _write_storyboard(tmp_path); a=MaterialAgent(project_path=str(tmp_path)).run({})["asset_requests"][0]; assert a["scene_id"]=="SCENE-001" and a["script_segment_id"]=="SEG-001" and a["fact_references"]==[{"claim_id":"claim-001"}]

def test_source_url_license_are_not_invented(tmp_path):
    _write_storyboard(tmp_path); r=MaterialAgent(project_path=str(tmp_path)).run({}); assert all(a["source"] is None and a["url"] is None and a["license"] is None for a in r["asset_requests"])

def test_ai_provider_failure_is_failed(tmp_path):
    _write_storyboard(tmp_path)
    class BrokenAI:
        def generate(self,prompt): raise RuntimeError("provider unavailable")
    r=MaterialAgent(project_path=str(tmp_path),ai_client=BrokenAI()).run({}); assert r["status"]=="FAILED" and "provider unavailable" in r["error"] and not (tmp_path/"08_素材"/"material_plan.json").exists()

def test_unresolved_is_not_agent_failure(tmp_path):
    _write_storyboard(tmp_path); r=MaterialAgent(project_path=str(tmp_path)).run({}); r["asset_requests"][0]["status"]="UNRESOLVED"; assert r["status"]=="SUCCESS"
