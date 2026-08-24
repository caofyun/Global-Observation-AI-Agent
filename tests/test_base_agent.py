import sys
import os


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from src.agents.base_agent import BaseAgent


class DummyAgent(BaseAgent):
    def execute(self, input_data):
        return {
            "message": "测试执行成功",
            "input": input_data,
        }


def test_base_agent_run():
    agent = DummyAgent("测试Agent")

    result = agent.run("美国航母进入中东")

    assert result["message"] == "测试执行成功"
    assert result["input"] == "美国航母进入中东"
