import os

from dotenv import load_dotenv


# ==========================================
# 环球观察速递
# AI配置模块 V1.0
#
# 功能：
# 1. 自动读取项目根目录.env
# 2. 获取AI服务商
# 3. 获取AI模型
# 4. 获取API Key
#
# 注意：
# 不在代码中直接保存API Key
# ==========================================


# ==========================================
# 加载.env
# ==========================================

load_dotenv()


# ==========================================
# AI配置
# ==========================================

AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    ""
)

AI_MODEL = os.getenv(
    "AI_MODEL",
    ""
)

AI_API_KEY = os.getenv(
    "AI_API_KEY",
    ""
)


# ==========================================
# 配置检查
# ==========================================

def check_ai_config():

    if not AI_PROVIDER:

        return False

    if not AI_MODEL:

        return False

    if not AI_API_KEY:

        return False

    return True