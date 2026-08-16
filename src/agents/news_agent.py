from src.agents.base_agent import BaseAgent
import json


# ==========================================
# 环球观察速递
# NewsAgent 新闻研究智能体 V1.0
# ==========================================


class NewsAgent(BaseAgent):

    # ==========================================
    # 初始化
    # ==========================================

    def __init__(self):

        super().__init__(
            "新闻研究Agent"
        )

    # ==========================================
    # 新闻研究执行逻辑
    # ==========================================

    def execute(self, input_data):

        # 当前阶段暂时不连接互联网
        # 先建立统一的新闻数据结构

        topic = str(
            input_data
        ).strip()

        if not topic:

            raise ValueError(
                "新闻选题不能为空"
            )

        # ======================================
        # 创建新闻研究数据
        # ======================================

        news_data = {

            "topic": topic,

            "status": "DRAFT", 

            "facts": [],

            "sources": [],

            "statements": [],

            "uncertainties": [],

            "research_notes": []

        }

        print()
        print("新闻研究任务已创建")
        print(
            f"新闻选题：{topic}"
        )

        return news_data