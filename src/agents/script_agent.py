import json
import os
from datetime import UTC, datetime

from src.agents.base_agent import BaseAgent


class ScriptAgent(BaseAgent):
    """Generate a traceable video script from an approved topic selection."""

    def __init__(self, project_path=None, ai_client=None):
        super().__init__("ScriptAgent", project_path)
        self.ai_client = ai_client

    @staticmethod
    def _load_json(path):
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def _require_file(path, label):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"缺少{label}: {path}")

    def _generate_text(self, selected_topic, verification, source_rank, duration):
        if self.ai_client is None:
            return {
                "hook": f"今天关注：{selected_topic}",
                "body": f"围绕{selected_topic}，本期仅根据已经核验的信息进行客观梳理。",
                "ending": "以上为目前可确认的信息，后续进展继续关注权威来源。",
            }

        prompt = {
            "task": "生成客观中文军事资讯短视频脚本",
            "topic": selected_topic,
            "duration_target_seconds": duration,
            "verification": verification,
            "source_rank": source_rank,
            "rules": [
                "只使用输入中的事实，不补造事实",
                "客观克制，不使用煽动性表达",
                "无法确认的信息明确表达不确定性",
                "输出 hook、body、ending 三部分",
            ],
        }
        response = self.ai_client.generate(json.dumps(prompt, ensure_ascii=False))
        if isinstance(response, dict):
            text = response.get("content") or response.get("text")
        else:
            text = response
        if not text:
            raise RuntimeError("AI provider 未返回脚本内容")
        return {"hook": str(text), "body": "", "ending": ""}

    def execute(self, input_data=None):
        project_path = self.project_path
        duration = 90
        if isinstance(input_data, dict):
            project_path = input_data.get("project_path") or project_path
            duration = int(input_data.get("duration_target_seconds", 90))

        if not project_path:
            raise ValueError("缺少project_path")

        selection_path = os.path.join(project_path, "05_选题决策", "topic_selection.json")
        verification_path = os.path.join(project_path, "02_事实核验", "verification.json")
        source_rank_path = os.path.join(project_path, "03_来源评级", "source_rank.json")

        self._require_file(selection_path, "topic_selection.json")
        self._require_file(verification_path, "verification.json")
        self._require_file(source_rank_path, "source_rank.json")

        selection = self._load_json(selection_path)
        verification = self._load_json(verification_path)
        source_rank = self._load_json(source_rank_path)

        selected_topic = selection.get("selected_topic")
        decision = selection.get("decision")
        if not selected_topic:
            raise ValueError("topic_selection.json 缺少selected_topic")
        if isinstance(selected_topic, list):
            raise ValueError("ScriptAgent V2.0 single mode requires a single selected_topic")
        if decision != "进入制作":
            raise ValueError(f"选题决策不允许进入制作: {decision}")

        generated = self._generate_text(selected_topic, verification, source_rank, duration)
        sections = [
            {"section_id": "hook", "type": "HOOK", "text": generated.get("hook", "")},
            {"section_id": "body-01", "type": "BODY", "text": generated.get("body", "")},
            {"section_id": "ending", "type": "ENDING", "text": generated.get("ending", "")},
        ]
        fact_references = self._build_fact_references(verification, source_rank)
        script_segments = [
            {
                "script_segment_id": section["section_id"].replace("body-01", "SEG-001").replace("hook", "SEG-000").replace("ending", "SEG-999"),
                "text": section["text"],
                "fact_references": fact_references,
            }
            for section in sections
            if section["text"]
        ]

        result = {
            "schema_version": "script.v2.0",
            "status": "SUCCESS",
            "project_id": os.path.basename(os.path.normpath(project_path)),
            "selected_topic": selected_topic,
            "decision": decision,
            "title": selected_topic,
            "duration_target_seconds": duration,
            "language": "zh-CN",
            "tone": "objective",
            "sections": sections,
            "script_segments": script_segments,
            "fact_references": fact_references,
            "human_confirmation": {"status": "WAIT_USER_CONFIRM", "approved": False},
            "meta": {
                "generated_at": datetime.now(UTC).isoformat(),
                "agent": "ScriptAgent",
                "version": "2.0",
            },
        }

        output_dir = os.path.join(project_path, "06_脚本")
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "script.json"), "w", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)

        markdown = "# " + result["title"] + "\n\n"
        markdown += "## 开场\n\n" + sections[0]["text"] + "\n\n"
        markdown += "## 正文\n\n" + sections[1]["text"] + "\n\n"
        markdown += "## 结尾\n\n" + sections[2]["text"] + "\n"
        with open(os.path.join(output_dir, "script.md"), "w", encoding="utf-8") as handle:
            handle.write(markdown)

        return result

    @staticmethod
    def _build_fact_references(verification, source_rank):
        references = []
        sources = source_rank.get("sources", []) if isinstance(source_rank, dict) else []
        for index, source in enumerate(sources, start=1):
            source_id = source.get("source_id") or source.get("name") or f"source-{index}"
            references.append({
                "claim_id": f"claim-{index:03d}",
                "source_id": source_id,
                "verification_status": verification.get("verification_status", "UNKNOWN"),
            })
        return references
