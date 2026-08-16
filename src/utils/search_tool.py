from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


# ==========================================
# 环球观察速递
# SearchTool 搜索工具 V1.0
# ==========================================


class SearchTool:

    # ==========================================
    # 初始化
    # ==========================================

    def __init__(self):

        self.name = "新闻搜索工具"

    # ==========================================
    # 搜索新闻
    # ==========================================

    def search(self, keyword, max_results=10):

        keyword = str(keyword).strip()

        if not keyword:

            raise ValueError(
                "搜索关键词不能为空"
            )

        print()
        print("==============================")
        print("新闻搜索工具 V1.0")
        print("==============================")

        print(
            f"正在搜索：{keyword}"
        )

        # ======================================
        # Google News RSS 搜索地址
        # ======================================

        encoded_keyword = quote(
            keyword
        )

        url = (
            "https://news.google.com/rss/search?"
            f"q={encoded_keyword}"
            "&hl=zh-CN"
            "&gl=CN"
            "&ceid=CN:zh-Hans"
        )

        # ======================================
        # 请求新闻搜索结果
        # ======================================

        request = Request(

            url,

            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        with urlopen(
            request,
            timeout=15
        ) as response:

            data = response.read()

        # ======================================
        # 解析RSS
        # ======================================

        root = ET.fromstring(
            data
        )

        results = []

        for item in root.findall(
            ".//item"
        ):

            title = item.findtext(
                "title",
                default=""
            )

            link = item.findtext(
                "link",
                default=""
            )

            pub_date = item.findtext(
                "pubDate",
                default=""
            )

            source_element = item.find(
                "source"
            )

            if source_element is not None:

                source = (
                    source_element.text
                    or ""
                )

            else:

                source = ""

            result = {

                "title": title.strip(),

                "source": source.strip(),

                "published_time":
                    pub_date.strip(),

                "url":
                    link.strip()

            }

            results.append(
                result
            )

            if len(results) >= max_results:

                break

        print()
        print(
            f"搜索完成，共找到 {len(results)} 条结果"
        )

        return results