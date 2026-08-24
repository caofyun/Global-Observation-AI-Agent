"""
Pipeline Runner V1.0

负责统一编排新闻选题生产Pipeline。

职责：
1. 按固定顺序调用Agent
2. 统一传递project_path
3. 收集Pipeline执行状态
4. 为ProductionController提供执行能力

V2.0 Baseline compatible
"""

from datetime import datetime


class PipelineRunner:
    """新闻选题生产Pipeline执行器 V1.0"""

    def __init__(self, agents=None):
        self.agents = agents or []

    def add_agent(self, agent):
        self.agents.append(agent)

    def run(self, context):
        """执行Pipeline。

        context:
            {
                "project_path": "",
                "topic": "",
                "options": {}
            }
        """
        result = {
            "pipeline_status": "RUNNING",
            "started_at": datetime.now().isoformat(),
            "completed_agents": [],
            "failed_agent": None,
            "error": None,
        }

        try:
            for agent in self.agents:
                agent_result = agent.run(context)

                if not agent_result or agent_result.get("status") != "SUCCESS":
                    result["pipeline_status"] = "FAILED"
                    result["failed_agent"] = agent.__class__.__name__
                    result["error"] = agent_result
                    return result

                result["completed_agents"].append(agent.__class__.__name__)

            result["pipeline_status"] = "COMPLETED"
            result["finished_at"] = datetime.now().isoformat()
            return result

        except Exception as exc:
            result["pipeline_status"] = "FAILED"
            result["error"] = str(exc)
            return result
