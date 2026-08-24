"""
Pipeline Runner V1.1

负责统一编排新闻选题生产Pipeline。

职责：
1. 按固定顺序调用Agent
2. 统一传递project_path
3. 收集Pipeline执行状态
4. 为ProductionController提供执行能力
5. 未显式注入Agent时，自动组装V2.0核心选题Pipeline

V2.0 Baseline compatible
"""

from datetime import datetime

from src.agents.news_agent import NewsAgent
from src.agents.news_verifier import NewsVerifier
from src.agents.source_ranker import SourceRanker
from src.agents.topic_scorer import TopicScorer
from src.agents.topic_selector import TopicSelector


class PipelineRunner:
    """新闻选题生产Pipeline执行器 V1.1"""

    def __init__(self, agents=None):
        # 显式传入agents时保持原有依赖注入能力。
        # 未传入时，在run()阶段根据project_path创建本次Pipeline实例。
        self.agents = agents

    def add_agent(self, agent):
        if self.agents is None:
            self.agents = []
        self.agents.append(agent)

    def _build_default_agents(self, project_path):
        """组装ProductionController默认使用的V2.0核心Agent链。"""
        return [
            NewsAgent(project_path=project_path),
            NewsVerifier(),
            SourceRanker(project_path=project_path),
            TopicScorer(project_path=project_path),
            TopicSelector(project_path=project_path),
        ]

    def _build_agent_input(self, agent, context):
        """根据Agent职责提供统一且兼容现有接口的输入。"""
        agent_name = agent.__class__.__name__
        project_path = context.get("project_path")
        topic = context.get("topic", "")

        if agent_name == "NewsAgent":
            return {
                "topic_keyword": topic,
                "project_path": project_path,
                "options": context.get("options", {}),
            }

        if agent_name in {
            "NewsVerifier",
            "SourceRanker",
            "TopicScorer",
        }:
            return {
                "project_path": project_path,
                "topic": topic,
                "options": context.get("options", {}),
            }

        if agent_name == "TopicSelector":
            return {
                "project_path": project_path,
                "mode": "single",
                "top_n": 1,
            }

        # 对未来自定义Agent保留统一context传递能力。
        return context

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
            project_path = context.get("project_path") if isinstance(context, dict) else None

            if self.agents is None:
                self.agents = self._build_default_agents(project_path)

            if not self.agents:
                result["pipeline_status"] = "FAILED"
                result["error"] = "PipelineRunner未配置任何Agent"
                return result

            for agent in self.agents:
                agent_result = agent.run(
                    self._build_agent_input(agent, context)
                )

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
            result["failed_agent"] = (
                self.agents[-1].__class__.__name__
                if self.agents
                else None
            )
            result["error"] = str(exc)
            return result
