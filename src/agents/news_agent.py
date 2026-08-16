from src.agents.base_agent import BaseAgent
from src.utils.search_tool import SearchTool

import json
import os


# ==========================================
# 环球观察速递
# NewsAgent 新闻研究智能体 V2.0
#
# 功能：
# 1. 接收新闻选题
# 2. 自动生成搜索关键词
# 3. 调用 SearchTool
# 4. 汇总搜索结果
# 5. 自动去重
# 6. 保存 search_results.json
# ==========================================


class NewsAgent(BaseAgent):

    # ==========================================
    # 初始化
    # ==========================================

    def __init__(self):

        super().__init__(
            "新闻研究Agent"
        )

        # 初始化搜索工具
        self.search_tool = SearchTool()

    # ==========================================
    # 生成搜索关键词
    # ==========================================

    def build_search_keywords(self, topic):

        keywords = [

            topic,

            f"{topic} 最新消息",

            f"{topic} news"

        ]

        return keywords

    # ==========================================
    # 新闻研究执行逻辑
    # ==========================================

    def execute(self, input_data):

        # ======================================
        # 读取输入
        # ======================================

        if isinstance(
            input_data,
            dict
        ):

            topic = str(
                input_data.get(
                    "topic",
                    ""
                )
            ).strip()

            project_path = input_data.get(
                "project_path"
            )

        else:

            topic = str(
                input_data
            ).strip()

            project_path = None

        # ======================================
        # 检查新闻选题
        # ======================================

        if not topic:

            raise ValueError(
                "新闻选题不能为空"
            )

        # ======================================
        # 生成搜索关键词
        # ======================================

        keywords = self.build_search_keywords(
            topic
        )

        print()
        print("==============================")
        print("NewsAgent V2.0")
        print("==============================")

        print(
            f"新闻选题：{topic}"
        )

        print()
        print("自动生成搜索关键词：")

        for keyword in keywords:

            print(
                f" - {keyword}"
            )

        # ======================================
        # 执行新闻搜索
        # ======================================

        all_results = []

        for keyword in keywords:

            print()
            print(
                f"正在搜索：{keyword}"
            )

            results = self.search_tool.search(
                keyword,
                max_results=10
            )

            all_results.extend(
                results
            )

        # ======================================
        # 搜索结果去重
        # ======================================

        unique_results = []

        seen_urls = set()

        seen_titles = set()

        for result in all_results:

            url = result.get(
                "url",
                ""
            ).strip()

            title = result.get(
                "title",
                ""
            ).strip()

            # 优先按照URL去重
            if url and url in seen_urls:

                continue

            # 没有URL时按照标题去重
            if not url and title in seen_titles:

                continue

            if url:

                seen_urls.add(
                    url
                )

            if title:

                seen_titles.add(
                    title
                )

            unique_results.append(
                result
            )

        # ======================================
        # 创建新闻研究数据
        # ======================================

        news_data = {

            "topic": topic,

            "status": "SEARCHED",

            "search_keywords": keywords,

            "search_results": unique_results,

            "facts": [],

            "sources": [],

            "statements": [],

            "uncertainties": [],

            "research_notes": []

        }

        # ======================================
        # 保存搜索结果
        # ======================================

        if project_path:

            news_folder = os.path.join(

                project_path,

                "01_新闻资料"

            )

            os.makedirs(

                news_folder,

                exist_ok=True

            )

            json_path = os.path.join(

                news_folder,

                "search_results.json"

            )

            with open(

                json_path,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(

                    news_data,

                    f,

                    ensure_ascii=False,

                    indent=4

                )

            print()
            print(
                "搜索结果已保存："
            )

            print(
                json_path
            )

        # ======================================
        # 输出统计
        # ======================================

        print()
        print("==============================")
        print("NewsAgent V2.0 搜索完成")
        print("==============================")

        print(
            f"搜索关键词：{len(keywords)} 个"
        )

        print(
            f"原始结果：{len(all_results)} 条"
        )

        print(
            f"去重后结果：{len(unique_results)} 条"
        )

        return news_data