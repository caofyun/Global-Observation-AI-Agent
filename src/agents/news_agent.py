from src.agents.base_agent import BaseAgent
from src.utils.search_tool import SearchTool

import json
import os


# ==========================================
# 环球观察速递
# NewsAgent 新闻发现与正文采集 Agent V2.0
# ==========================================


class NewsAgent(BaseAgent):

    def __init__(self, project_path=None):
        super().__init__("NewsAgent", project_path)
        self.search_tool = SearchTool()

    def build_search_keywords(self, topic_keyword):
        topic_keyword = str(topic_keyword).strip()
        if not topic_keyword:
            return []
        return [
            topic_keyword,
            f"{topic_keyword} 最新消息",
            f"{topic_keyword} news",
        ]

    def _normalize_search_result(self, result, index):
        return {
            "result_id": result.get("result_id") or f"result_{index + 1}",
            "title": str(result.get("title", "")).strip(),
            "url": str(result.get("url", "")).strip(),
            "source": str(result.get("source", "")).strip(),
            "published_time": str(result.get("published_time", "")).strip(),
            "snippet": str(result.get("snippet", "")).strip(),
        }

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

        # 严格禁止用标题冒充摘要。
        if summary == title:
            summary = ""

        if not summary:
            snippet = str(result.get("snippet", "")).strip()
            if snippet and snippet != title:
                summary = snippet

        if not summary:
            description = str(result.get("description", "")).strip()
            if description and description != title:
                summary = description

        # 严格禁止用标题冒充正文。
        if content == title:
            content = ""

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
            "source_id": f"source_{source.lower()}" if source else None,
        }

    def execute(self, input_data):
        if isinstance(input_data, dict):
            topic_keyword = str(input_data.get("topic_keyword", "")).strip()
        else:
            topic_keyword = str(input_data).strip()

        project_path = getattr(self, "project_path", None)

        if not topic_keyword:
            raise ValueError("topic_keyword 不能为空")

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

        all_results = []

        for keyword in keywords:
            print()
            print(f"正在搜索：{keyword}")
            results = self.search_tool.search(keyword, max_results=10)
            all_results.extend(results or [])

        unique_results = []
        seen_urls = set()
        seen_titles = set()

        for result in all_results:
            url = str(result.get("url", "")).strip()
            title = str(result.get("title", "")).strip()

            if url and url in seen_urls:
                continue
            if not url and title and title in seen_titles:
                continue

            if url:
                seen_urls.add(url)
            if title:
                seen_titles.add(title)

            unique_results.append(
                self._normalize_search_result(result, len(unique_results))
            )

        articles = [
            self._normalize_article(result, index)
            for index, result in enumerate(unique_results)
        ]

        if project_path:
            news_folder = os.path.join(project_path, "01_新闻资料")
            os.makedirs(news_folder, exist_ok=True)

            search_results_path = os.path.join(
                news_folder, "search_results.json"
            )
            with open(search_results_path, "w", encoding="utf-8") as f:
                json.dump(
                    unique_results,
                    f,
                    ensure_ascii=False,
                    indent=4,
                )

            news_articles_path = os.path.join(
                news_folder, "news_articles.json"
            )
            with open(news_articles_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "schema_version": "2.0",
                        "topic": topic_keyword,
                        "articles": articles,
                    },
                    f,
                    ensure_ascii=False,
                    indent=4,
                )

            print()
            print("搜索结果已保存：")
            print(search_results_path)
            print()
            print("正文数据已保存：")
            print(news_articles_path)

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
            "news_articles": articles,
        }
