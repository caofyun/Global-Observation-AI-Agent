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


from src.agents.base_agent import BaseAgent


# ==========================================
# 创建测试 Agent
# ==========================================

class TestAgent(BaseAgent):

    def execute(self, input_data):

        print(
            f"收到输入：{input_data}"
        )

        return {
            "message": "测试执行成功",
            "input": input_data
        }


# ==========================================
# 测试
# ==========================================

agent = TestAgent(
    "测试Agent"
)


result = agent.run(
    "美国航母进入中东"
)


print()
print("==============================")
print("测试结果")
print("==============================")

print(result)

print()
print("Agent状态：")

print(
    agent.get_status()
)