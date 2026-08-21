import os
import json
from datetime import datetime

from src.agents.base_agent import BaseAgent


# ==========================================
# 环球观察速递
# TopicScorer V2.0
#
# 说明：读取 SourceRanker 输出的 source_rank.json
# 输出：04_热点评分/topic_score.json
# 遵循 BaseAgent 的 run/execute 约定
# ==========================================


class TopicScorer(BaseAgent):

    def __init__(self, project_path=None):

        super().__init__("TopicScorer", project_path)

    def load_json(self, path):

        if not os.path.exists(path):
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def normalize_score(self, v, lo=0, hi=100):
        try:
            v = float(v)
        except Exception:
            return 0
        if v < lo:
            return lo
        if v > hi:
            return hi
        return v

    def aggregate_source_quality(self, sources):
        if not isinstance(sources, list) or len(sources) == 0:
            return 0

        scores = []
        for s in sources:
            try:
                c = int(s.get("credibility_score", 50))
            except Exception:
                c = 50
            try:
                v = int(s.get("verification_score", 50))
            except Exception:
                v = 50

            scores.append((c + v) / 2)

        if not scores:
            return 0

        return round(sum(scores) / len(scores))

    def compute_breakdown(self, source_rank, verification_data):

        sources = source_rank.get("sources", []) if source_rank else []
        unique_source_count = len(sources)

        # source_quality: mean of (credibility_score, verification_score)
        source_quality = self.aggregate_source_quality(sources)

        # news_hotness: proxy by unique source count (simple linear mapping)
        news_hotness = min(100, unique_source_count * 5)

        # international_influence: proxy by unique source count (conservative)
        international_influence = min(100, unique_source_count * 4)

        # video_potential: base 50 + small bonus per source
        video_potential = min(100, 50 + unique_source_count * 3)

        # user_interest: V2 proxy (mix of hotness and source quality)
        user_interest = round((news_hotness * 0.7 + source_quality * 0.3))

        # If verification_data provides signals, slightly adjust hotness
        if verification_data and isinstance(verification_data.get("articles"), list):
            article_count = len(verification_data.get("articles", []))
            # boost hotness proportional to article density (capped)
            boost = min(20, article_count * 2)
            news_hotness = min(100, int((news_hotness * 0.8) + (boost * 0.2)))

        breakdown = {
            "international_influence": int(international_influence),
            "news_hotness": int(news_hotness),
            "user_interest": int(user_interest),
            "video_potential": int(video_potential),
            "source_quality": int(source_quality)
        }

        meta = {
            "unique_source_count": unique_source_count,
            "earliest_published": None,
            "latest_published": None,
            "top_sources": [s.get("source_name") for s in sources[:5]],
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version": "TopicScorer v2.0"
        }

        # fill earliest/latest from verification_data if available
        if verification_data and isinstance(verification_data.get("articles"), list):
            times = []
            for a in verification_data.get("articles", []):
                t = a.get("published_time")
                if not t:
                    continue
                times.append(t)
            if times:
                try:
                    # prefer ISO strings; fall back to raw min/max
                    meta["earliest_published"] = min(times)
                    meta["latest_published"] = max(times)
                except Exception:
                    meta["earliest_published"] = times[0]
                    meta["latest_published"] = times[-1]

        return breakdown, meta

    def decide_recommendation(self, score, source_quality, verification_data):

        verification_status = None
        verification_confidence = None
        if verification_data:
            verification_status = verification_data.get("verification_status")
            verification_confidence = verification_data.get("confidence")

        if score >= 80 and (source_quality >= 50 or verification_status == "MULTIPLE_SOURCES_FOUND"):
            recommendation = "制作"
        elif (60 <= score < 80) or (score >= 80 and source_quality < 50):
            recommendation = "观望"
        else:
            recommendation = "不制作"

        # If verification confidence is LOW, demote recommendation one step
        if verification_confidence and str(verification_confidence).upper() == "LOW":
            if recommendation == "制作":
                recommendation = "观望"
            elif recommendation == "观望":
                recommendation = "不制作"

        return recommendation

    def execute(self, input_data=None):

        if isinstance(input_data, dict):
            project_path = input_data.get("project_path") or self.project_path
        else:
            project_path = self.project_path if input_data is None else str(input_data).strip()

        if not project_path:
            raise ValueError("缺少project_path")

        source_rank_path = os.path.join(project_path, "03_来源评级", "source_rank.json")

        source_rank = self.load_json(source_rank_path)

        if source_rank is None:
            raise FileNotFoundError("未找到 source_rank.json: " + source_rank_path)

        verification_path = os.path.join(project_path, "02_事实核验", "verification.json")
        verification_data = self.load_json(verification_path)

        breakdown, meta = self.compute_breakdown(source_rank, verification_data)

        # weights per design
        weights = {
            "international_influence": 0.25,
            "news_hotness": 0.30,
            "user_interest": 0.20,
            "video_potential": 0.15,
            "source_quality": 0.10
        }

        # compute final score
        total = 0.0
        for k, w in weights.items():
            s = breakdown.get(k, 0)
            total += w * float(s)

        final_score = int(round(total))

        source_quality = breakdown.get("source_quality", 0)

        recommendation = self.decide_recommendation(final_score, source_quality, verification_data)

        result = {
            "topic": source_rank.get("topic", ""),
            "score": final_score,
            "recommendation": recommendation,
            "breakdown": breakdown,
            "weights": weights,
            "meta": meta
        }

        output_dir = os.path.join(project_path, "04_热点评分")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "topic_score.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print()
        print("==============================")
        print("TopicScorer V2.0 完成")
        print("==============================")
        print(f"主题：{result.get('topic')}")
        print(f"总分：{final_score}")

        return result
