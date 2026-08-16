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


from src.agents.news_agent import NewsAgent


# ==========================================
# 创建NewsAgent
# ==========================================

agent = NewsAgent()


# ==========================================
# 测试新闻选题
# ==========================================

topic = input(
    "请输入新闻选题："
).strip()


# ==========================================
# 执行NewsAgent
# ==========================================

result = agent.run(
    topic
)


# ==========================================
# 输出结果
# ==========================================

print()
print("==============================")
print("NewsAgent测试结果")
print("==============================")


print(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=4
    )
)


print()
print("==============================")
print("Agent状态")
print("==============================")


print(
    agent.get_status()
)