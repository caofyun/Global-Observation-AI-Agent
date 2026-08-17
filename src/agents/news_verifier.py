import os
import json
from urllib.parse import urlparse

from src.agents.base_agent import BaseAgent
from src.utils.ai_model_client import AIModelClient


# ==========================================
# 环球观察速递
# NewsVerifier 新闻事实核验智能体 V2.0
#
# V2.0功能：
# 1. 读取 search_results.json
# 2. 检查搜索结果基本完整性
# 3. 识别新闻来源
# 4. 对相同标题进行简单去重
# 5. 统计来源数量
# 6. 标记基础信息状态
# 7. 调用AI进行辅助事实分析
# 8. 提取事实主张
# 9. 分析多来源一致性
# 10. 识别冲突和不确定信息
# 11. 给出AI辅助可信度等级
# 12. 生成 verification.json
# 13. 生成 ai_verification.json
#
# V2.0增强：
# 14. 增强AI JSON解析
# 15. 支持```json代码块
# 16. 支持AI前后附带说明文字
# 17. 保存AI原始返回内容
# 18. 增加AI返回结构检查
#
# 注意：
# V2.0的AI分析属于辅助核验
# 不直接判定新闻“绝对真实”或“绝对虚假”
# 最终事实判断仍需要人工审核
# ==========================================


class NewsVerifier(BaseAgent):

    # ==========================================
    # 初始化
    # ==========================================

    def __init__(self):

        super().__init__(
            "新闻事实核验Agent V2.0"
        )

        # ======================================
        # 初始化AI模型客户端
        # ======================================

        self.ai_client = AIModelClient()

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
    # V2.0
    # 构造AI核验提示词
    # ==========================================

    def build_ai_prompt(
        self,
        verification_data
    ):

        topic = verification_data.get(
            "topic",
            ""
        )

        results = verification_data.get(
            "results",
            []
        )

        # ======================================
        # 整理新闻资料
        # ======================================

        news_items = []

        for index, result in enumerate(
            results,
            start=1
        ):

            news_items.append({

                "id": index,

                "title":
                    result.get(
                        "title",
                        ""
                    ),

                "source":
                    result.get(
                        "source",
                        ""
                    ),

                "published_time":
                    result.get(
                        "published_time",
                        ""
                    ),

                "url":
                    result.get(
                        "url",
                        ""
                    )

            })

        # ======================================
        # AI任务说明
        # ======================================

        prompt = f"""
你是一名严格、客观的新闻事实核验辅助分析助手。

你的任务不是直接判定新闻真假，
而是根据提供的多个新闻来源，
分析这些来源对同一事件的描述情况。

新闻主题：
{topic}

新闻来源资料：
{json.dumps(
    news_items,
    ensure_ascii=False,
    indent=4
)}

请完成以下任务：

1. 提取主要事实主张（claims）
2. 判断不同来源是否描述了相同事件
3. 找出不同来源之间可能存在的冲突
4. 找出目前无法确认的信息
5. 根据现有来源支持程度给出可信度等级
6. 提出需要人工进一步核验的事项
7. 给出简洁客观的总结

可信度等级只能使用：

HIGH
MEDIUM
LOW

重要要求：

- 不要把“多个来源报道”直接等同于“事实已经确认”
- 不要编造新闻来源没有提供的信息
- 不要补充没有证据支持的事实
- 不要进行战争预测
- 不要进行政治立场判断
- 不要使用煽动性或恐慌性语言
- 如果资料不足，应明确说明“不确定”
- 最终事实判断必须保留人工审核

必须严格返回JSON。

不要返回Markdown。
不要使用```json代码块。
不要在JSON前后添加任何解释文字。

JSON格式：

{{
    "confidence": "HIGH/MEDIUM/LOW",
    "claims": [],
    "supporting_evidence": [],
    "conflicts": [],
    "uncertainties": [],
    "risk_notes": [],
    "ai_summary": "",
    "human_review_required": true
}}
"""

        return prompt

    # ==========================================
    # V2.0增强
    # 从AI文本中提取JSON
    # ==========================================

    def extract_json_from_text(
        self,
        text
    ):

        if not text:

            return None

        text = str(
            text
        ).strip()

        # ======================================
        # 方法1：
        # 直接解析
        # ======================================

        try:

            return json.loads(
                text
            )

        except Exception:

            pass

        # ======================================
        # 方法2：
        # 去除Markdown代码块
        #
        # 例如：
        #
        # ```json
        # {
        #     ...
        # }
        # ```
        # ======================================

        cleaned_text = text

        if "```json" in cleaned_text:

            cleaned_text = cleaned_text.replace(
                "```json",
                ""
            )

            cleaned_text = cleaned_text.replace(
                "```",
                ""
            )

            cleaned_text = cleaned_text.strip()

            try:

                return json.loads(
                    cleaned_text
                )

            except Exception:

                pass

        # ======================================
        # 普通代码块
        # ======================================

        if "```" in cleaned_text:

            cleaned_text = cleaned_text.replace(
                "```",
                ""
            ).strip()

            try:

                return json.loads(
                    cleaned_text
                )

            except Exception:

                pass

        # ======================================
        # 方法3：
        # 从文本中寻找第一个完整JSON对象
        #
        # 例如：
        #
        # 以下是分析结果：
        #
        # {
        #     "confidence": "HIGH"
        # }
        # ======================================

        start_index = cleaned_text.find(
            "{"
        )

        if start_index == -1:

            return None

        # ======================================
        # 使用大括号深度寻找JSON结束位置
        # ======================================

        brace_count = 0

        in_string = False

        escape_next = False

        for index in range(
            start_index,
            len(cleaned_text)
        ):

            char = cleaned_text[
                index
            ]

            # ==================================
            # 处理字符串状态
            # ==================================

            if escape_next:

                escape_next = False

                continue

            if char == "\\":

                escape_next = True

                continue

            if char == '"':

                in_string = not in_string

                continue

            # ==================================
            # JSON大括号计数
            # ==================================

            if not in_string:

                if char == "{":

                    brace_count += 1

                elif char == "}":

                    brace_count -= 1

                    if brace_count == 0:

                        json_text = (
                            cleaned_text[
                                start_index:index + 1
                            ]
                        )

                        try:

                            return json.loads(
                                json_text
                            )

                        except Exception:

                            return None

        return None

    # ==========================================
    # V2.0增强
    # 检查AI JSON结构
    # ==========================================

    def validate_ai_result(
        self,
        parsed_result
    ):

        # ======================================
        # 必须是JSON对象
        # ======================================

        if not isinstance(
            parsed_result,
            dict
        ):

            return False

        # ======================================
        # 必要字段
        # ======================================

        required_fields = [

            "confidence",

            "claims",

            "supporting_evidence",

            "conflicts",

            "uncertainties",

            "risk_notes",

            "ai_summary",

            "human_review_required"

        ]

        for field in required_fields:

            if field not in parsed_result:

                return False

        # ======================================
        # confidence必须合法
        # ======================================

        if parsed_result.get(
            "confidence"
        ) not in [

            "HIGH",
            "MEDIUM",
            "LOW"

        ]:

            return False

        # ======================================
        # 数组字段检查
        # ======================================

        list_fields = [

            "claims",

            "supporting_evidence",

            "conflicts",

            "uncertainties",

            "risk_notes"

        ]

        for field in list_fields:

            if not isinstance(
                parsed_result.get(field),
                list
            ):

                return False

        # ======================================
        # summary必须是字符串
        # ======================================

        if not isinstance(
            parsed_result.get(
                "ai_summary"
            ),
            str
        ):

            return False

        # ======================================
        # human_review_required
        # ======================================

        if not isinstance(
            parsed_result.get(
                "human_review_required"
            ),
            bool
        ):

            return False

        return True

    # ==========================================
    # V2.0
    # AI事实分析
    # ==========================================

    def analyze_with_ai(
        self,
        verification_data
    ):

        print()
        print(
            "=============================="
        )
        print(
            "AI事实分析开始"
        )
        print(
            "=============================="
        )

        # ======================================
        # 构造提示词
        # ======================================

        prompt = self.build_ai_prompt(
            verification_data
        )

        try:

            # ==================================
            # 调用统一AI客户端
            # ==================================

            ai_result = self.ai_client.analyze(
                prompt
            )

        except Exception as e:

            print()
            print(
                "AI分析调用失败："
            )

            print(
                str(e)
            )

            return {

                "status":
                    "AI_API_ERROR",

                "ai_model":
                    getattr(
                        self.ai_client,
                        "model",
                        ""
                    ),

                "confidence":
                    "LOW",

                "claims": [],

                "supporting_evidence": [],

                "conflicts": [],

                "uncertainties": [

                    "AI API调用失败"

                ],

                "risk_notes": [

                    str(e)

                ],

                "ai_summary":
                    "AI事实分析未完成",

                "human_review_required":
                    True

            }

        # ======================================
        # 检查AI调用状态
        # ======================================

        if not isinstance(
            ai_result,
            dict
        ):

            return {

                "status":
                    "INVALID_AI_RESPONSE",

                "confidence":
                    "LOW",

                "claims": [],

                "supporting_evidence": [],

                "conflicts": [],

                "uncertainties": [

                    "AI返回格式异常"

                ],

                "risk_notes": [],

                "ai_summary":
                    "AI返回结果无法解析",

                "human_review_required":
                    True

            }

        if ai_result.get(
            "status"
        ) != "SUCCESS":

            return {

                "status":
                    "AI_ANALYSIS_FAILED",

                "ai_model":
                    ai_result.get(
                        "model",
                        ""
                    ),

                "confidence":
                    "LOW",

                "claims": [],

                "supporting_evidence": [],

                "conflicts": [],

                "uncertainties": [

                    "AI分析未成功"

                ],

                "risk_notes": [

                    ai_result.get(
                        "content",
                        ""
                    )

                ],

                "ai_summary":
                    "AI分析未成功完成",

                "human_review_required":
                    True

            }

        # ======================================
        # 获取AI文本
        # ======================================

        ai_content = str(
            ai_result.get(
                "content",
                ""
            )
        ).strip()

        # ======================================
        # 新增：
        # 打印AI原始返回内容
        #
        # 以后如果JSON解析失败，
        # 可以直接看到Gemini到底返回了什么
        # ======================================

        print()
        print(
            "AI原始返回内容："
        )

        print(
            "------------------------------"
        )

        print(
            ai_content
        )

        print(
            "------------------------------"
        )

        # ======================================
        # 检查空返回
        # ======================================

        if not ai_content:

            print()
            print(
                "AI返回内容为空"
            )

            return {

                "status":
                    "AI_EMPTY_RESPONSE",

                "ai_model":
                    ai_result.get(
                        "model",
                        ""
                    ),

                "confidence":
                    "LOW",

                "claims": [],

                "supporting_evidence": [],

                "conflicts": [],

                "uncertainties": [

                    "AI没有返回任何内容"

                ],

                "risk_notes": [

                    "建议检查AIModelClient"

                ],

                "ai_summary":
                    "AI没有返回有效内容",

                "human_review_required":
                    True,

                "raw_ai_content":
                    ""

            }

        # ======================================
        # 增强JSON解析
        # ======================================

        parsed_result = (
            self.extract_json_from_text(
                ai_content
            )
        )

        # ======================================
        # JSON解析失败
        # ======================================

        if parsed_result is None:

            print()
            print(
                "AI返回内容不是有效JSON"
            )

            return {

                "status":
                    "AI_RESPONSE_PARSE_ERROR",

                "ai_model":
                    ai_result.get(
                        "model",
                        ""
                    ),

                "confidence":
                    "LOW",

                "claims": [],

                "supporting_evidence": [],

                "conflicts": [],

                "uncertainties": [

                    "AI返回内容无法解析为JSON"

                ],

                "risk_notes": [

                    "建议人工检查AI原始返回内容"

                ],

                "ai_summary":
                    ai_content,

                "human_review_required":
                    True,

                "raw_ai_content":
                    ai_content

            }

        # ======================================
        # JSON结构检查
        # ======================================

        if not self.validate_ai_result(
            parsed_result
        ):

            print()
            print(
                "AI返回JSON结构不完整"
            )

            return {

                "status":
                    "AI_JSON_STRUCTURE_ERROR",

                "ai_model":
                    ai_result.get(
                        "model",
                        ""
                    ),

                "confidence":
                    "LOW",

                "claims": [],

                "supporting_evidence": [],

                "conflicts": [],

                "uncertainties": [

                    "AI返回JSON缺少必要字段或字段类型错误"

                ],

                "risk_notes": [

                    "建议人工检查AI原始返回内容"

                ],

                "ai_summary":
                    str(parsed_result),

                "human_review_required":
                    True,

                "raw_ai_content":
                    ai_content

            }

        # ======================================
        # 强制系统字段
        # ======================================

        parsed_result["status"] = (
            "SUCCESS"
        )

        parsed_result["ai_model"] = (
            ai_result.get(
                "model",
                ""
            )
        )

        # ======================================
        # 保存AI原始响应
        #
        # 便于后续调试
        # ======================================

        parsed_result[
            "raw_ai_content"
        ] = ai_content

        print()
        print(
            "AI事实分析完成"
        )

        print(
            "AI JSON解析成功"
        )

        print(
            "AI可信度："
            + str(
                parsed_result.get(
                    "confidence"
                )
            )
        )

        return parsed_result

    # ==========================================
    # V2.0
    # 保存AI核验结果
    # ==========================================

    def save_ai_verification(
        self,
        project_path,
        ai_verification_data
    ):

        if not project_path:

            return None

        news_folder = os.path.join(

            project_path,

            "01_新闻资料"

        )

        os.makedirs(

            news_folder,

            exist_ok=True

        )

        ai_verification_path = os.path.join(

            news_folder,

            "ai_verification.json"

        )

        with open(

            ai_verification_path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                ai_verification_data,

                f,

                ensure_ascii=False,

                indent=4

            )

        print()
        print(
            "AI核验结果已保存："
        )

        print(
            ai_verification_path
        )

        return ai_verification_path

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
        print("NewsVerifier V2.0")
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
        # 创建基础核验结果
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

                "V2.0进行基础来源整理和去重",

                "V2.0增加AI辅助事实分析",

                "AI分析不代表新闻事实已经确认",

                "最终事实判断需要人工审核"

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
        # V2.0 AI事实分析
        # ======================================

        ai_verification_data = (
            self.analyze_with_ai(
                verification_data
            )
        )

        # ======================================
        # 给AI结果补充主题
        # ======================================

        ai_verification_data["topic"] = (
            topic
        )

        # ======================================
        # 保存ai_verification.json
        # ======================================

        self.save_ai_verification(

            project_path,

            ai_verification_data

        )

        # ======================================
        # 输出统计
        # ======================================

        print()
        print("==============================")
        print("NewsVerifier V2.0完成")
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

        print(
            "AI核验结果："
        )

        print(
            ai_verification_data.get(
                "status",
                ""
            )
        )

        return verification_data