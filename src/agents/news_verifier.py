import os
import json
from urllib.parse import urlparse

from src.agents.base_agent import BaseAgent


# ==========================================
# 环球观察速递
# NewsVerifier 新闻事实核验智能体 V1.0
#
# 当前版本功能：
# 1. 读取 search_results.json
# 2. 检查搜索结果基本完整性
# 3. 识别新闻来源
# 4. 对相同标题进行简单去重
# 5. 统计来源数量
# 6. 标记信息状态
# 7. 生成 verification.json
#
# 注意：
# V1.0 不判断新闻真假
# V1.0 不使用AI判断事实
# V1.0 只建立核验框架
# ==========================================


class NewsVerifier(BaseAgent):

    # ==========================================
    # 初始化
    # ==========================================

    def __init__(self):

        super().__init__(
            "新闻事实核验Agent"
        )

    # ==========================================
    # 来源识别
    # ==========================================

    def identify_source(self, result):

        source = str(
            result.get(
                "source",
                ""
            )
        ).strip()

        url = str(
            result.get(
                "url",
                ""
            )
        ).strip()

        # 优先使用搜索结果中的source
        if source:

            return source

        # 如果没有source
        # 尝试从URL中获取域名
        if url:

            try:

                domain = urlparse(
                    url
                ).netloc

                if domain:

                    return domain

            except Exception:

                pass

        return "未知来源"

    # ==========================================
    # 标准化标题
    # ==========================================

    def normalize_title(self, title):

        title = str(
            title
        ).strip().lower()

        # 去除常见标点
        remove_chars = [
            " ",
            "　",
            "，",
            "。",
            "！",
            "？",
            "：",
            "；",
            "、",
            ",",
            ".",
            "!",
            "?",
            ":",
            ";"
        ]

        for char in remove_chars:

            title = title.replace(
                char,
                ""
            )

        return title

    # ==========================================
    # 执行新闻核验
    # ==========================================

    def execute(self, input_data):

        # ======================================
        # 读取输入
        # ======================================

        if isinstance(
            input_data,
            dict
        ):

            project_path = input_data.get(
                "project_path"
            )

            search_results_path = input_data.get(
                "search_results_path"
            )

        else:

            project_path = str(
                input_data
            ).strip()

            search_results_path = None

        # ======================================
        # 自动寻找search_results.json
        # ======================================

        if not search_results_path:

            if not project_path:

                raise ValueError(
                    "必须提供project_path"
                )

            search_results_path = os.path.join(

                project_path,

                "01_新闻资料",

                "search_results.json"

            )

        # ======================================
        # 检查文件
        # ======================================

        if not os.path.exists(
            search_results_path
        ):

            raise FileNotFoundError(

                "找不到search_results.json："
                + search_results_path

            )

        print()
        print("==============================")
        print("NewsVerifier V1.0")
        print("==============================")

        print(
            "正在读取："
        )

        print(
            search_results_path
        )

        # ======================================
        # 读取JSON
        # ======================================

        with open(

            search_results_path,

            "r",

            encoding="utf-8"

        ) as f:

            news_data = json.load(
                f
            )

        topic = news_data.get(
            "topic",
            ""
        )

        search_results = news_data.get(
            "search_results",
            []
        )

        # ======================================
        # 基础检查
        # ======================================

        valid_results = []

        invalid_results = []

        for result in search_results:

            title = str(
                result.get(
                    "title",
                    ""
                )
            ).strip()

            url = str(
                result.get(
                    "url",
                    ""
                )
            ).strip()

            source = self.identify_source(
                result
            )

            if not title:

                invalid_results.append(
                    result
                )

                continue

            valid_results.append({

                "title": title,

                "source": source,

                "published_time":
                    result.get(
                        "published_time",
                        ""
                    ),

                "url": url

            })

        # ======================================
        # 标题去重
        # ======================================

        unique_results = []

        seen_titles = set()

        for result in valid_results:

            normalized_title = (
                self.normalize_title(
                    result["title"]
                )
            )

            if normalized_title in seen_titles:

                continue

            seen_titles.add(
                normalized_title
            )

            unique_results.append(
                result
            )

        # ======================================
        # 来源统计
        # ======================================

        source_counts = {}

        for result in unique_results:

            source = result[
                "source"
            ]

            if source not in source_counts:

                source_counts[source] = 0

            source_counts[source] += 1

        # ======================================
        # 根据来源数量给出基础状态
        #
        # 注意：
        # 这不是“真实性判断”
        # ======================================

        unique_source_count = len(
            source_counts
        )

        if unique_source_count >= 3:

            verification_status = (
                "MULTIPLE_SOURCES_FOUND"
            )

        elif unique_source_count == 2:

            verification_status = (
                "TWO_SOURCES_FOUND"
            )

        elif unique_source_count == 1:

            verification_status = (
                "SINGLE_SOURCE_FOUND"
            )

        else:

            verification_status = (
                "NO_VALID_SOURCE"
            )

        # ======================================
        # 创建核验结果
        # ======================================

        verification_data = {

            "topic": topic,

            "status":
                verification_status,

            "total_search_results":
                len(search_results),

            "valid_results":
                len(valid_results),

            "unique_results":
                len(unique_results),

            "source_count":
                unique_source_count,

            "source_counts":
                source_counts,

            "results":
                unique_results,

            "invalid_results":
                invalid_results,

            "facts": [],

            "claims": [],

            "conflicts": [],

            "uncertainties": [],

            "verification_notes": [

                "V1.0仅进行基础来源整理和去重",

                "V1.0不代表新闻事实已经确认",

                "V1.0未进行AI语义事实核验",

                "最终事实判断需要后续人工审核"

            ]

        }

        # ======================================
        # 保存verification.json
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

            verification_path = os.path.join(

                news_folder,

                "verification.json"

            )

            with open(

                verification_path,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(

                    verification_data,

                    f,

                    ensure_ascii=False,

                    indent=4

                )

            print()
            print(
                "核验结果已保存："
            )

            print(
                verification_path
            )

        # ======================================
        # 输出统计
        # ======================================

        print()
        print("==============================")
        print("NewsVerifier V1.0完成")
        print("==============================")

        print(
            f"原始搜索结果：{len(search_results)} 条"
        )

        print(
            f"有效结果：{len(valid_results)} 条"
        )

        print(
            f"去重后结果：{len(unique_results)} 条"
        )

        print(
            f"发现来源：{unique_source_count} 个"
        )

        print(
            f"基础状态：{verification_status}"
        )

        return verification_data