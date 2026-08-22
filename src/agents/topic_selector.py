import os
import json
from datetime import datetime

from src.agents.base_agent import BaseAgent


class TopicSelector(BaseAgent):

    def __init__(self, project_path=None):
        super().__init__("TopicSelector", project_path)

    def load_json(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def collect_candidates(self, projects_root):
        candidates = []

        if not os.path.isdir(projects_root):
            return candidates

        for name in os.listdir(projects_root):
            project_dir = os.path.join(projects_root, name)
            if not os.path.isdir(project_dir):
                continue

            score_path = os.path.join(project_dir, "04_热点评分", "topic_score.json")
            data = self.load_json(score_path)
            if not data:
                continue

            # basic normalization
            topic = data.get("topic")
            if not topic or topic == "未知主题":
                continue
            try:
                score = float(data.get("score", 0))
            except Exception:
                score = 0.0
            recommendation = data.get("recommendation", "不制作")
            breakdown = data.get("breakdown", {})

            candidates.append({
                "project": name,
                "topic": topic,
                "score": score,
                "recommendation": recommendation,
                "breakdown": breakdown,
                "raw": data
            })

        return candidates

    def rank_candidates(self, candidates):
        # recommendation priority: 制作(0) > 观望(1) > 不制作(2)
        prio = {"制作": 0, "观望": 1, "不制作": 2}

        def key_fn(c):
            return (-float(c.get("score", 0)), prio.get(c.get("recommendation"), 3))

        return sorted(candidates, key=key_fn)

    def derive_reasons(self, breakdown):
        reasons = []
        if not isinstance(breakdown, dict):
            return reasons
        if breakdown.get("international_influence", 0) >= 70:
            reasons.append("国际影响力较高")
        if breakdown.get("news_hotness", 0) >= 70:
            reasons.append("新闻热度持续")
        if breakdown.get("source_quality", 0) >= 70:
            reasons.append("来源可靠")
        if breakdown.get("video_potential", 0) >= 70:
            reasons.append("具有视频表达价值")
        return reasons

    def map_decision(self, score, recommendation):
        try:
            s = float(score)
        except Exception:
            s = 0.0

        if s >= 80 and recommendation == "制作":
            return "进入制作"
        if 60 <= s < 80:
            return "人工观察"
        return "不制作"

    def map_production_decision(self, decision):
        return {
            "进入制作": "APPROVE",
            "人工观察": "REVIEW",
            "不制作": "REJECT",
        }.get(decision, "REJECT")

    def execute(self, input_data=None):
        # input_data expected to provide the projects root directory
        if isinstance(input_data, dict):
            projects_root = input_data.get("project_path") or self.project_path
            mode = input_data.get("mode", "single")
            top_n = int(input_data.get("top_n", 1))
        else:
            projects_root = self.project_path if input_data is None else str(input_data).strip()
            mode = "single"
            top_n = 1

        if not projects_root:
            raise ValueError("缺少project_path")

        candidates = self.collect_candidates(projects_root)

        if not candidates:
            raise FileNotFoundError("No candidate topics")

        ranked = self.rank_candidates(candidates)

        ranking_list = []
        for idx, c in enumerate(ranked, start=1):
            ranking_list.append({
                "rank": idx,
                "topic": c.get("topic"),
                "score": int(round(c.get("score", 0))),
                "recommendation": c.get("recommendation")
            })

        # select top N topics depending on mode
        if mode == "multi":
            selected = ranked[:top_n]
            selected_topics = [s.get("topic") for s in selected]
            decision = [self.map_decision(s.get("score"), s.get("recommendation")) for s in selected]
            selection_score = [int(round(s.get("score", 0))) for s in selected]
        else:
            selected = ranked[0]
            selected_topics = selected.get("topic")
            decision = self.map_decision(selected.get("score"), selected.get("recommendation"))
            selection_score = int(round(selected.get("score", 0)))

        # derive reasons from top candidate breakdown
        top_breakdown = ranked[0].get("breakdown", {})
        reasons = self.derive_reasons(top_breakdown)

        result = {
            "selected_topic": selected_topics,
            "decision": decision,
            "production_decision": (
                [self.map_production_decision(item) for item in decision]
                if isinstance(decision, list)
                else self.map_production_decision(decision)
            ),
            "selection_score": selection_score,
            "ranking": ranking_list,
            "reason": reasons,
            "meta": {
                "candidate_count": len(ranked),
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "version": "TopicSelector v2.0"
            }
        }

        output_dir = os.path.join(projects_root, "05_选题决策")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "topic_selection.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print()
        print("==============================")
        print("TopicSelector V2.0 完成")
        print("==============================")
        print(f"候选数：{len(ranked)}")
        print(f"已选择：{result.get('selected_topic')}")

        return result
