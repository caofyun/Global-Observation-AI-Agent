# ==========================================
# 环球观察速递
# AIModelClient V2.0
#
# 功能：
# 1. 读取AI配置
# 2. 支持Gemini
# 3. 调用真实Gemini API
# 4. 返回AI文本结果
#
# V2.0暂时只接入Gemini
# 后续再扩展OpenAI / Claude
# ==========================================

from google import genai

from src.config.ai_config import (
    AI_PROVIDER,
    AI_MODEL,
    AI_API_KEY
)


class AIModelClient:

    # ==========================================
    # 初始化
    # ==========================================

    def __init__(self):

        self.name = "AI模型客户端"

        self.provider = AI_PROVIDER

        self.model = AI_MODEL

        self.api_key = AI_API_KEY

        # ======================================
        # 创建Gemini客户端
        # ======================================

        if self.provider == "gemini":

            if not self.api_key:

                raise ValueError(
                    "Gemini API Key不存在"
                )

            self.client = genai.Client(
                api_key=self.api_key
            )

        else:

            self.client = None

    # ==========================================
    # AI分析
    # ==========================================

    def analyze(self, prompt):

        prompt = str(
            prompt
        ).strip()

        if not prompt:

            raise ValueError(
                "AI分析内容不能为空"
            )

        # ======================================
        # Gemini
        # ======================================

        if self.provider == "gemini":

            response = self.client.models.generate_content(

                model=self.model,

                contents=prompt

            )

            return {

                "status": "SUCCESS",

                "provider": self.provider,

                "model": self.model,

                "content": response.text

            }

        # ======================================
        # 暂不支持其他模型
        # ======================================

        raise ValueError(

            f"暂不支持的AI服务商："
            f"{self.provider}"

        )