import json
import os

from src.agents.news_verifier import NewsVerifier
from src.agents.source_ranker import SourceRanker
from src.agents.topic_scorer import TopicScorer
from src.agents.topic_selector import TopicSelector


class DiscoveryPipelineAdapter:
    """Connects a V2.1 Discovery output to the existing V2.0 pipeline."""

    def __init__(self, news_verifier=None, source_ranker=None, topic_scorer=None, topic_selector=None):
        self.news_verifier = news_verifier
        self.source_ranker = source_ranker
        self.topic_scorer = topic_scorer
        self.topic_selector = topic_selector

    @staticmethod
    def _load_discovery_output(project_path):
        output_path = os.path.join(project_path, "01_新闻资料", "news_articles.json")
        if not os.path.exists(output_path):
            raise FileNotFoundError("未找到news_articles.json：" + output_path)
        with open(output_path, "r", encoding="utf-8") as output_file:
            data = json.load(output_file)
        if not isinstance(data, dict):
            raise ValueError("news_articles.json 必须为对象结构")
        if data.get("status") != "SUCCESS":
            raise ValueError("Discovery 未成功，不能进入 Topic Pipeline")
        topic = data.get("topic")
        if not isinstance(topic, str) or not topic.strip() or topic.strip() == "未知主题":
            raise ValueError("news_articles.json 缺少合法topic")
        if not isinstance(data.get("articles"), list):
            raise ValueError("news_articles.json 的 articles 必须为数组")
        return data, topic.strip()

    @staticmethod
    def _stage_succeeded(stage_result):
        return isinstance(stage_result, dict) and stage_result.get("status") == "SUCCESS"

    @staticmethod
    def _stage_error(stage_result):
        if isinstance(stage_result, dict):
            return stage_result.get("error") or "V2.0 Agent 执行失败"
        return "V2.0 Agent 返回了无效结果"

    def _get_agents(self, project_path):
        return (
            self.news_verifier or NewsVerifier(),
            self.source_ranker or SourceRanker(project_path=project_path),
            self.topic_scorer or TopicScorer(project_path=project_path),
            # TopicSelector scans a projects root, unlike the other stages.
            self.topic_selector or TopicSelector(project_path=os.path.dirname(project_path)),
        )

    def run(self, project_path):
        project_path = str(project_path).strip() if project_path else ""
        if not project_path:
            return {"status": "FAILED", "project_path": project_path, "error": "缺少project_path"}
        try:
            discovery_data, topic = self._load_discovery_output(project_path)
            result = {"status": "SUCCESS", "project_path": project_path, "topic": topic, "stages": {}}
            if not discovery_data["articles"]:
                result["skipped"] = True
                result["reason"] = "Discovery 成功但没有候选新闻"
                return result

            verifier, ranker, scorer, selector = self._get_agents(project_path)
            stages = [
                ("news_verifier", verifier, {"project_path": project_path, "topic_keyword": topic}),
                ("source_ranker", ranker, {"project_path": project_path}),
                ("topic_scorer", scorer, {"project_path": project_path, "topic": topic}),
                ("topic_selector", selector, {}),
            ]
            for stage_name, agent, input_data in stages:
                stage_result = agent.run(input_data)
                result["stages"][stage_name] = stage_result
                if not self._stage_succeeded(stage_result):
                    return {
                        **result,
                        "status": "FAILED",
                        "failed_stage": stage_name,
                        "error": self._stage_error(stage_result),
                    }
            return result
        except Exception as error:
            return {"status": "FAILED", "project_path": project_path, "error": str(error)}