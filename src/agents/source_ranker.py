import os
import json

from src.agents.base_agent import BaseAgent


# ==========================================
# 环球观察速递
# SourceRanker V2.0
#
# 新闻来源评级 Agent
#
# V2.0冻结实现：
#
# 输入：
# project_path/02_事实核验/verification.json
#
# 输出：
# project_path/03_来源评级/source_rank.json
#
# 职责：
# 新闻来源质量评级
#
# ==========================================


class SourceRanker(BaseAgent):

    # ======================================
    # 初始化
    # ======================================

    def __init__(self, project_path=None):

        super().__init__(
            "SourceRanker",
            project_path
        )

        self.source_database = self.load_source_database()

    # ======================================
    # 加载来源数据库
    # ======================================

    def load_source_database(self):

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        config_path = os.path.join(
            project_root,
            "src",
            "config",
            "source_database.json"
        )

        if not os.path.exists(config_path):
            return {}

        try:
            with open(
                config_path,
                "r",
                encoding="utf-8"
            ) as f:
                return json.load(f)
        except Exception:
            return {}

    # ======================================
    # 来源名称标准化
    # ======================================

    def normalize_source(self, source):

        return str(source).strip()

    # ======================================
    # 获取来源信息
    # ======================================

    def get_source_info(self, source):

        source = self.normalize_source(source)

        if source in self.source_database:
            return self.source_database[source]

        for name, info in self.source_database.items():
            aliases = info.get("aliases", [])
            if name.lower() in source.lower() or any(
                str(alias).lower() in source.lower() for alias in aliases
            ):
                return info

        return {
            "level": "D",
            "score": 40,
            "type": "未知来源"
        }

    # ======================================
    # 统一来源提取
    # ======================================

    def collect_source_names(self, verification_data):

        source_names = []

        for item in verification_data.get("sources", []):
            if isinstance(item, dict):
                source_name = item.get("source_name") or item.get("source") or item.get("name") or ""
            else:
                source_name = str(item)

            source_name = self.normalize_source(source_name)
            if source_name:
                source_names.append(source_name)

        for article in verification_data.get("articles", []):
            if not isinstance(article, dict):
                continue

            source_name = self.normalize_source(article.get("source", ""))
            if source_name:
                source_names.append(source_name)

        return source_names

    # ======================================
    # 来源去重
    # ======================================

    def analyze_sources(self, source_names):

        source_map = {}

        for source_name in source_names:
            if not source_name:
                continue

            if source_name not in source_map:
                source_map[source_name] = {
                    "source_name": source_name,
                    "count": 1
                }
            else:
                source_map[source_name]["count"] += 1

        return list(source_map.values())

    def collect_source_records(self, verification_data):
        source_map = {}
        for article in verification_data.get("articles", []):
            if not isinstance(article, dict):
                continue
            source_name = self.normalize_source(article.get("source", ""))
            if not source_name:
                continue
            source_id = self.normalize_source(article.get("source_id", ""))
            if not source_id:
                source_id = "source_" + source_name.lower().replace(" ", "_")
            if source_id not in source_map:
                source_map[source_id] = {
                    "source_id": source_id,
                    "source_name": source_name,
                    "count": 0
                }
            source_map[source_id]["count"] += 1
        return list(source_map.values())

    # ======================================
    # 计算验证评分
    # ======================================

    def calculate_verification_score(self, count):

        if count >= 5:
            return 100
        elif count >= 3:
            return 85
        elif count >= 2:
            return 70
        else:
            return 50

    # ======================================
    # 来源等级转换
    # ======================================

    def convert_rank(self, credibility_score):

        if credibility_score >= 85:
            return "A"
        elif credibility_score >= 70:
            return "B"
        elif credibility_score >= 50:
            return "C"
        else:
            return "D"

    # ======================================
    # 生成评级原因
    # ======================================

    def build_reason(self, source_info, verification_score):

        reasons = []
        level = source_info.get("level", "D")

        if level in ["A", "B"]:
            reasons.append("来源历史可信度较高")
        else:
            reasons.append("来源可信度有限")

        if verification_score >= 70:
            reasons.append("存在多来源交叉信息")
        else:
            reasons.append("交叉验证不足")

        return "；".join(reasons)

    # ======================================
    # 执行Agent
    # ======================================

    def execute(self, input_data=None):

        if isinstance(input_data, dict):
            project_path = input_data.get("project_path") or self.project_path
        else:
            project_path = self.project_path if input_data is None else str(input_data).strip()

        if not project_path:
            raise ValueError("缺少project_path")

        verification_path = os.path.join(
            project_path,
            "02_事实核验",
            "verification.json"
        )

        if not os.path.exists(verification_path):
            raise FileNotFoundError("未找到verification.json")

        with open(
            verification_path,
            "r",
            encoding="utf-8"
        ) as f:
            verification_data = json.load(f)

        topic = verification_data.get("topic", "")
        unique_sources = self.collect_source_records(verification_data)

        source_results = []
        for item in unique_sources:
            source_id = item["source_id"]
            source_name = item["source_name"]
            info = self.get_source_info(source_name)
            credibility_score = int(info.get("score", 40))
            verification_score = self.calculate_verification_score(item["count"])
            rank = self.convert_rank(credibility_score)

            source_results.append({
                "source_id": source_id,
                "source_name": source_name,
                "source_type": info.get("category", info.get("type", "未知来源")),
                "source_credibility_score": credibility_score,
                "cross_source_verification_score": verification_score,
                "credibility_score": credibility_score,
                "verification_score": verification_score,
                "source_rank": rank,
                "reason": self.build_reason(info, verification_score)
            })

        output_dir = os.path.join(project_path, "03_来源评级")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "source_rank.json")

        result = {
            "topic": topic,
            "sources": source_results
        }

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print()
        print("==============================")
        print("SourceRanker V2.0完成")
        print("==============================")
        print(f"评级来源数量：{len(source_results)}")
        print("source_rank.json生成成功")

        return result