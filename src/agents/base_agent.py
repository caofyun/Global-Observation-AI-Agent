# 所有 Agent 必须遵守的“交通规则”
# 统一Agent的接口规范，方便后续扩展和维护

from abc import ABC, abstractmethod


class BaseAgent(ABC):

    # ==========================================
    # 所有 AI Agent 的统一基础接口
    # ==========================================

    def __init__(self, agent_name=None, project_path=None):
        self.agent_name = agent_name or "BaseAgent"
        self.project_path = project_path

        # 兼容历史属性，避免影响当前子类的已有使用方式
        self.name = self.agent_name

        self.status = "CREATED"
        self.result = {}
        self.error = ""

    # ==========================================
    # Agent 执行入口
    # ==========================================

    def run(self, input_data):
        self.status = "CREATED"
        self.error = ""
        self.result = {}

        normalized_input = input_data

        if isinstance(input_data, dict):
            if input_data.get("agent_name"):
                self.agent_name = str(input_data.get("agent_name"))
                self.name = self.agent_name

            if input_data.get("project_path") is not None:
                self.project_path = input_data.get("project_path")

            normalized_input = input_data.get("input_data", input_data)

        print()
        print("==============================")
        print(f"Agent：{self.agent_name}")
        print("==============================")

        self.status = "RUNNING"

        try:
            execution_result = self.execute(normalized_input)

            if execution_result is None:
                execution_result = {}

            self.result = (
                execution_result
                if isinstance(execution_result, dict)
                else {"value": execution_result}
            )

            self.status = "SUCCESS"

            print(f"{self.agent_name} 执行完成")

            # 保留统一Envelope，同时向后兼容历史测试/调用方：
            # Agent.execute() 返回的业务字段直接暴露在顶层。
            response = {
                "agent_name": self.agent_name,
                "status": self.status,
                "result": self.result,
                "error": "",
            }
            response.update(self.result)
            return response

        except ValueError as e:
            # 输入契约错误也是 Agent 的标准失败结果，不能让异常穿透 run()。
            # 这样所有 Agent 都遵守统一的 SUCCESS / FAILED Envelope。
            self.status = "FAILED"
            self.result = {}
            self.error = str(e)

            print(f"{self.agent_name} 执行失败：{self.error}")

            return {
                "agent_name": self.agent_name,
                "status": self.status,
                "result": {},
                "error": self.error,
            }

        except Exception as e:
            self.status = "FAILED"
            self.result = {}
            self.error = str(e)

            print(f"{self.agent_name} 执行失败：{e}")

            return {
                "agent_name": self.agent_name,
                "status": self.status,
                "result": {},
                "error": self.error,
            }

    # ==========================================
    # Agent 实际执行逻辑
    # ==========================================

    @abstractmethod
    def execute(self, input_data):
        pass

    # ==========================================
    # 获取 Agent 状态
    # ==========================================

    def get_status(self):
        return {
            "agent_name": self.agent_name,
            "status": self.status,
            "result": self.result,
            "error": self.error,
        }
