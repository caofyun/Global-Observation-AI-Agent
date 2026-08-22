from src.agents.base_agent import BaseAgent
from src.utils.search_tool import SearchTool

import json
import os


# ==========================================
# 环球观察速递
# NewsAgent 新闻发现与正文采集 Agent V2.0
#
# 功能：
# 1. 接收新闻主题关键词
# 2. 自动生成搜索关键词
# 3. 调用 SearchTool
# 4. 汇总搜索结果
# 5. 自动去重
# 6. 保存 search_results.json
# 7. 生成 news_articles.json
# ==========================================


class NewsAgent(BaseAgent):

    # ==========================================
    # 初始化
    # ==========================================

    def __init__(self, project_path=None):

        super().__init__(
            "NewsAgent",
            project_path
        )

        self.search_tool = SearchTool()

    # ==========================================
    # 生成搜索关键词
    # ==========================================

    def build_search_keywords(self, topic_keyword):

        topic_keyword = str(
            topic_keyword
        ).strip()

        if not topic_keyword:

            return []

        keywords = [
            topic_keyword,
            f"{topic_keyword} 最新消息",
            f"{topic_keyword} news"
        ]

        return keywords

    # ==========================================
    # 规范搜索结果字段
    # ==========================================

    def _normalize_search_result(self, result, index):

        return {
            "result_id": result.get("result_id") or f"result_{index + 1}",
            "title": str(result.get("title", "")).strip(),
            "url": str(result.get("url", "")).strip(),
            "source": str(result.get("source", "")).strip(),
            "published_time": str(result.get("published_time", "")).strip(),
            "snippet": str(result.get("snippet", "")).strip()
        }

    # ==========================================
    # 规范正文文章字段
    # ==========================================

    def _normalize_article(self, result, index):

        title = str(result.get("title", "")).strip()
        source = str(result.get("source", "")).strip()
        url = str(result.get("url", "")).strip()
        published_time = str(result.get("published_time", "")).strip()

        content = (
            str(result.get("content")).strip()
            if result.get("content") is not None else ""
        )
        summary = (
            str(result.get("summary")).strip()
            if result.get("summary") is not None else ""
        )
        if not summary:
            summary = (
                str(result.get("snippet")).strip()
                if result.get("snippet") is not None else ""
            )
        if not summary:
            summary = (
                str(result.get("description")).strip()
                if result.get("description") is not None else ""
            )

        return {
            "article_id": f"article_{index + 1}",
            "title": title,
            "source": source,
            "url": url,
            "published_time": published_time,
            "content": content or None,
            "summary": summary or None,
            "content_available": bool(content),
            "summary_available": bool(summary),
            "source_id": f"source_{source.lower()}" if source else None
        }

    # ==========================================
    # 新闻发现与正文采集执行逻辑
    # ==========================================

    def execute(self, input_data):

        # ======================================
        # 读取业务输入
        # ======================================

        if isinstance(input_data, dict):
            topic_keyword = str(
                input_data.get(
                    "topic_keyword",
                    ""
                )
            ).strip()
        else:
            topic_keyword = str(input_data).strip()

        project_path = getattr(self, "project_path", None)

        # ======================================
        # 检查主题关键词
        # ======================================

        if not topic_keyword:
            raise ValueError("topic_keyword 不能为空")

        # ======================================
        # 生成搜索关键词
        # ======================================

        keywords = self.build_search_keywords(topic_keyword)

        print()
        print("==============================")
        print("NewsAgent V2.0")
        print("==============================")

        print(f"研究主题：{topic_keyword}")

        print()
        print("自动生成搜索关键词：")

        for keyword in keywords:
            print(f" - {keyword}")

        # ======================================
        # 执行新闻搜索
        # ======================================

        all_results = []

        for keyword in keywords:
            print()
            print(f"正在搜索：{keyword}")

            results = self.search_tool.search(
                keyword,
                max_results=10
            )

            all_results.extend(results)

        # ======================================
        # 搜索结果去重
        # ======================================

        unique_results = []
        seen_urls = set()
        seen_titles = set()

        for result in all_results:
            url = str(result.get("url", "")).strip()
            title = str(result.get("title", "")).strip()

            if url and url in seen_urls:
                continue

            if not url and title in seen_titles:
                continue

            if url:
                seen_urls.add(url)

            if title:
                seen_titles.add(title)

            unique_results.append(
                self._normalize_search_result(result, len(unique_results))
            )

        # ======================================
        # 正文采集结果
        # ======================================

        articles = []

        for index, result in enumerate(unique_results):
            articles.append(
                self._normalize_article(result, index)
            )

        # ======================================
        # 保存结果文件
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

            search_results_path = os.path.join(
                news_folder,
                "search_results.json"
            )

            with open(
                search_results_path,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    unique_results,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            news_articles_path = os.path.join(
                news_folder,
                "news_articles.json"
            )

            with open(
                news_articles_path,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    {"articles": articles},
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            print()
            print("搜索结果已保存：")
            print(search_results_path)
            print()
            print("正文数据已保存：")
            print(news_articles_path)

        # ======================================
        # 输出统计
        # ======================================

        print()
        print("==============================")
        print("NewsAgent V2.0 搜索完成")
        print("==============================")

        print(f"搜索关键词：{len(keywords)} 个")
        print(f"原始结果：{len(all_results)} 条")
        print(f"去重后结果：{len(unique_results)} 条")
        print(f"正文文章：{len(articles)} 篇")

        return {
            "topic_keyword": topic_keyword,
            "search_keywords": keywords,
            "search_results": unique_results,
            "news_articles": articles
        }
