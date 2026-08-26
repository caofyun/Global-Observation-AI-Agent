import json
import os
from datetime import UTC, datetime

from src.agents.base_agent import BaseAgent


class MaterialAgent(BaseAgent):
    """Convert an approved storyboard into a traceable material plan."""

    MATERIAL_TYPES = {
        "news_footage", "photo", "map", "chart", "document",
        "generic_broll", "text_graphic",
    }

    def __init__(self, project_path=None, ai_client=None):
        super().__init__("MaterialAgent", project_path)
        self.ai_client = ai_client

    @staticmethod
    def _load_json(path):
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def _require_file(path):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"缺少storyboard.json: {path}")

    @classmethod
    def _validate_storyboard(cls, storyboard):
        if not isinstance(storyboard, dict):
            raise ValueError("storyboard.json 必须是对象")
        if storyboard.get("status") != "SUCCESS":
            raise ValueError("storyboard.json 状态不是SUCCESS")
        if not storyboard.get("topic"):
            raise ValueError("storyboard.json 缺少topic")
        scenes = storyboard.get("scenes")
        if not isinstance(scenes, list) or not scenes:
            raise ValueError("storyboard.json 缺少有效scenes")
        for index, scene in enumerate(scenes, start=1):
            if not isinstance(scene, dict):
                raise ValueError(f"scenes[{index}] 必须是对象")
            for field in ("scene_id", "script_segment_id", "duration_seconds", "visual"):
                if not scene.get(field):
                    raise ValueError(f"scenes[{index}] 缺少{field}")
            visual = scene["visual"]
            if not isinstance(visual, dict):
                raise ValueError(f"scenes[{index}].visual 必须是对象")
            if not visual.get("description"):
                raise ValueError(f"scenes[{index}].visual 缺少description")
            material_type = visual.get("material_type")
            if material_type not in cls.MATERIAL_TYPES:
                raise ValueError(f"scenes[{index}] 使用未定义素材类型: {material_type}")

    def _generate_requests(self, storyboard):
        if self.ai_client is None:
            return {}
        prompt = {
            "task": "将已确认分镜转换为结构化素材需求",
            "topic": storyboard["topic"],
            "scenes": storyboard["scenes"],
            "rules": [
                "不得新增新闻事实",
                "不得修改scene_id或script_segment_id",
                "不得虚构source、url或license",
                "只返回description、search_query和status等素材需求字段",
            ],
        }
        response = self.ai_client.generate(json.dumps(prompt, ensure_ascii=False))
        if not isinstance(response, dict):
            return {}
        requests = response.get("asset_requests", {})
        return requests if isinstance(requests, (dict, list)) else {}

    @staticmethod
    def _ai_request_for_scene(requests, scene_id):
        if isinstance(requests, dict):
            value = requests.get(scene_id, {})
            return value if isinstance(value, dict) else {}
        if isinstance(requests, list):
            for item in requests:
                if isinstance(item, dict) and item.get("scene_id") == scene_id:
                    return item
        return {}

    def _build_requests(self, storyboard, ai_requests):
        asset_requests = []
        for index, scene in enumerate(storyboard["scenes"], start=1):
            visual = scene["visual"]
            ai_item = self._ai_request_for_scene(ai_requests, scene["scene_id"])
            try:
                duration = float(scene["duration_seconds"])
            except (TypeError, ValueError):
                raise ValueError(f"scene {scene['scene_id']} 时间值无法解析")
            if duration <= 0:
                raise ValueError(f"scene {scene['scene_id']} 时长必须大于0")
            if duration.is_integer():
                duration = int(duration)
            references = scene.get("fact_references")
            if references is None:
                references = storyboard.get("fact_references", [])
            status = ai_item.get("status", "REQUESTED")
            if status not in {"REQUESTED", "READY", "UNRESOLVED", "FAILED"}:
                status = "REQUESTED"
            asset_requests.append({
                "asset_id": f"ASSET-{index:03d}",
                "scene_id": scene["scene_id"],
                "script_segment_id": scene["script_segment_id"],
                "asset_type": visual["material_type"],
                "description": ai_item.get("description") or visual["description"],
                "search_query": ai_item.get("search_query") or visual["description"],
                "duration_seconds": duration,
                "fact_references": references,
                "source": None,
                "url": None,
                "license": None,
                "status": status,
            })
        return asset_requests

    def execute(self, input_data=None):
        project_path = self.project_path
        if isinstance(input_data, dict):
            project_path = input_data.get("project_path") or project_path
        if not project_path:
            raise ValueError("缺少project_path")
        storyboard_path = os.path.join(project_path, "07_分镜", "storyboard.json")
        self._require_file(storyboard_path)
        storyboard = self._load_json(storyboard_path)
        self._validate_storyboard(storyboard)
        asset_requests = self._build_requests(storyboard, self._generate_requests(storyboard))
        result = {
            "schema_version": "material_plan.v2.0",
            "status": "SUCCESS",
            "project_id": os.path.basename(os.path.normpath(project_path)),
            "topic": storyboard["topic"],
            "source_storyboard": "storyboard.json",
            "statistics": {
                "scene_count": len(storyboard["scenes"]),
                "asset_request_count": len(asset_requests),
                "ready_count": sum(item["status"] == "READY" for item in asset_requests),
                "unresolved_count": sum(item["status"] == "UNRESOLVED" for item in asset_requests),
            },
            "asset_requests": asset_requests,
            "meta": {
                "generated_at": datetime.now(UTC).isoformat(),
                "agent": "MaterialAgent",
                "version": "2.0",
            },
        }
        output_dir = os.path.join(project_path, "08_素材")
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "material_plan.json"), "w", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
        return result
