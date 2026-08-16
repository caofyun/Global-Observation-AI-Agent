import sys
import os


# ==========================================
# 添加项目根目录
# ==========================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


from src.config.ai_config import (
    AI_PROVIDER,
    AI_MODEL,
    AI_API_KEY,
    check_ai_config
)


# ==========================================
# 输出配置测试结果
# ==========================================

print()
print("==============================")
print("AI配置模块 V1.0测试")
print("==============================")


print(
    "AI服务商：",
    AI_PROVIDER
)


print(
    "AI模型：",
    AI_MODEL
)


# ==========================================
# 注意：
# 不直接打印完整API Key
# ==========================================

if AI_API_KEY:

    print(
        "API Key：已读取"
    )

else:

    print(
        "API Key：未读取"
    )


# ==========================================
# 检查配置
# ==========================================

if check_ai_config():

    print()
    print(
        "AI配置检查：成功"
    )

else:

    print()
    print(
        "AI配置检查：失败"
    )