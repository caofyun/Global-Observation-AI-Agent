import json
import os
from datetime import UTC, datetime

from src.agents.base_agent import BaseAgent


class StoryboardAgent(BaseAgent):
    """Convert an approved ScriptAgent output into a traceable storyboard."""

    def __init__(self, project_path=None, ai_client=None):
        super().__init__("StoryboardAgent", project_path)
        self.ai_client = ai_client

    @staticmethod
    def _load_json(path):
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def _require_file(path, label):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"缺少{label}: {path}")

    @staticmethod
    def _validate_script(script):
        if not isinstance(script, dict):
            raise ValueError("script.json 必须是对象")
        if script.get("status") != "SUCCESS":
            raise ValueError("script.json 状态不是SUCCESS")
        if not script.get("selected_topic"):
            raise ValueError("script.json 缺少selected_topic")
        if not script.get("title"):
            raise ValueError("script.json 缺少title")
        segments = script.get("script_segments")
        if not isinstance(segments, list) or not segments:
            raise ValueError("script.json 缺少有效script_segments")
        confirmation = script.get("human_confirmation")
        if not isinstance(confirmation, dict) or confirmation.get("approved") is not True:
            raise ValueError("脚本尚未人工确认允许制作")
        for index, segment in enumerate(segments, start=1):
            if not isinstance(segment, dict):
                raise ValueError(f"script_segments[{index}] 必须是对象")
            if not segment.get("script_segment_id"):
                raise ValueError(f"script_segments[{index}] 缺少script_segment_id")
            if not segment.get("text"):
                raise ValueError(f"script_segments[{index}] 缺少text")

    def _build_scenes(self, script):
        scenes = []
        segments = script["script_segments"]
        references = script.get("fact_references") or []
        default_duration = max(1, round(float(script.get("duration_target_seconds", 90)) / len(segments)))

        for index, segment in enumerate(segments, start=1):
            duration = segment.get("duration_seconds", default_duration)
            try:
                duration = float(duration)
            except (TypeError, ValueError):
                raise ValueError(f"script segment {segment['script_segment_id']} 时间值无法解析")
            if duration <= 0:
                raise ValueError(f"script segment {segment['script_segment_id']} 时长必须大于0")
            if duration.is_integer():
                duration = int(duration)

            segment_refs = segment.get("fact_references")
            if segment_refs is None:
                segment_refs = references

            narration = str(segment["text"])
            scenes.append({
                "scene_id": f"SCENE-{index:03d}",
                "script_segment_id": segment["script_segment_id"],
                "duration_seconds": duration,
                "narration": narration,
                "visual": {
                    "description": segment.get("visual_description") or f"呈现与旁白对应的新闻画面：{script['title']}",
                    "material_type": segment.get("material_type") or "news_footage",
                },
                "subtitle": segment.get("subtitle") or narration,
                "sound_effect": segment.get("sound_effect"),
                "fact_references": segment_refs,
            })
        return scenes

    def execute(self, input_data=None):
        project_path = self.project_path
        if isinstance(input_data, dict):
            project_path = input_data.get("project_path") or project_path

        if not project_path:
            raise ValueError("缺少project_path")

        script_path = os.path.join(project_path, "06_脚本", "script.json")
        self._require_file(script_path, "script.json")
        script = self._load_json(script_path)
        self._validate_script(script)

        scenes = self._build_scenes(script)
        total_duration = sum(scene["duration_seconds"] for scene in scenes)
        if total_duration <= 0:
            raise ValueError("无法构建有效时间轴")

        result = {
            "schema_version": "storyboard.v2.0",
            "status": "SUCCESS",
            "project_id": os.path.basename(os.path.normpath(project_path)),
            "topic": script["selected_topic"],
            "title": script["title"],
            "total_duration_seconds": total_duration,
            "scenes": scenes,
            "fact_references": script.get("fact_references", []),
            "meta": {
                "generated_at": datetime.now(UTC).isoformat(),
                "agent": "StoryboardAgent",
                "version": "2.0",
            },
        }

        output_dir = os.path.join(project_path, "07_分镜")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "storyboard.json")
        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)

        return result
