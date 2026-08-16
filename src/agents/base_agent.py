# 所有 Agent 必须遵守的“交通规则”
# 统一Agent的接口规范，方便后续扩展和维护from abc import ABC, abstractmethod


from abc import ABC, abstractmethod


class BaseAgent(ABC):

    # ==========================================
    # 所有 AI Agent 的统一基础接口
    # ==========================================

    def __init__(self, name):

        self.name = name

        # Agent 初始状态
        self.status = "IDLE"

        # 最后一次执行结果
        self.result = None

        # 错误信息
        self.error = None

    # ==========================================
    # Agent 执行入口
    # ==========================================

    def run(self, input_data):

        print()
        print("==============================")
        print(f"Agent：{self.name}")
        print("==============================")

        self.status = "RUNNING"
        self.error = None

        try:

            self.result = self.execute(
                input_data
            )

            self.status = "COMPLETED"

            print(
                f"{self.name} 执行完成"
            )

            return self.result

        except Exception as e:

            self.status = "ERROR"
            self.error = str(e)

            print(
                f"{self.name} 执行失败：{e}"
            )

            return None

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
            "name": self.name,
            "status": self.status,
            "result": self.result,
            "error": self.error
        }