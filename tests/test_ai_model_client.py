import sys
import os
import json


# ==========================================
# 添加项目根目录
# ==========================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


import src.utils.ai_model_client


# ==========================================
# 创建AI客户端
# ==========================================

client = src.utils.ai_model_client.AIModelClient()


# ==========================================
# 测试问题
# ==========================================

prompt = """
请只回复：

Gemini API连接成功
"""


# ==========================================
# 调用真实AI
# ==========================================

print()
print("==============================")
print("AIModelClient V2.0")
print("Gemini真实API测试")
print("==============================")


result = client.analyze(
    prompt
)


# ==========================================
# 输出结果
# ==========================================

print()

print(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=4
    )
)