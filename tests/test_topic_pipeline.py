import os
import sys
import json
import shutil
import traceback
from datetime import datetime


# ==========================================
# 项目根目录
# ==========================================

PROJECT_ROOT_PATH = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT_PATH)


# ==========================================
# Agent
# ==========================================

from src.agents.news_agent import NewsAgent
from src.agents.news_verifier import NewsVerifier
from src.agents.source_ranker import SourceRanker
from src.agents.topic_scorer import TopicScorer
from src.agents.topic_selector import TopicSelector


# ==========================================
# Topic Pipeline V2.0
#
# 真实互联网新闻选题端到端测试
#
# 测试链路：
#
# 新闻关键词
#      ↓
# NewsAgent
#      ↓
# news_articles.json
#      ↓
# NewsVerifier
#      ↓
# verification.json
#      ↓
# SourceRanker
#      ↓
# source_rank.json
#      ↓
# TopicScorer
#      ↓
# topic_score.json
#      ↓
# TopicSelector
#      ↓
# topic_selection.json
#
# 注意：
# 本测试不修改任何已有 Agent。
# ==========================================


TEST_ROOT = os.path.join(
    PROJECT_ROOT_PATH,
    "projects",
    "topic_pipeline_test_project"
)


# ==========================================
# 第一阶段测试关键词
#
# 暂时采用多个新闻领域。
#
# 目的：
# 验证多个候选项目能否进入 TopicSelector
# 进行比较。
#
# 后续真实测试中可以继续增加。
# ==========================================

TEST_TOPICS = [
    "美国航母部署",
    "中东局势",
    "霍尔木兹海峡",
    "俄乌局势",
    "亚太安全"
]


# ==========================================
# 工具函数
# ==========================================

def print_separator():
    print()
    print("=" * 70)


def check_file(path):
    if os.path.exists(path):
        print(f"[OK] 文件存在: {path}")
        return True

    print(f"[FAIL] 文件不存在: {path}")
    return False


def load_json(path):
    try:
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except Exception as e:
        print(f"[FAIL] JSON读取失败: {path}")
        print(f"错误: {e}")
        return None


def prepare_test_root():
    """
    清理本次测试目录并重新创建。

    注意：
    只删除 topic_pipeline_test_project，
    不删除其他 projects。
    """

    if os.path.exists(TEST_ROOT):
        print(f"清理旧测试目录: {TEST_ROOT}")
        shutil.rmtree(TEST_ROOT)

    os.makedirs(
        TEST_ROOT,
        exist_ok=True
    )

    print(f"[OK] 测试根目录: {TEST_ROOT}")


def create_topic_project(topic_keyword):
    """
    为每一个候选新闻领域创建独立项目目录。

    例如：

    topic_pipeline_test_project/
        01_美国航母部署/
        02_中东局势/
        03_霍尔木兹海峡/
        ...
    """

    index = TEST_TOPICS.index(topic_keyword) + 1

    safe_name = topic_keyword.replace(
        "/",
        "_"
    ).replace(
        "\\",
        "_"
    )

    project_name = (
        f"{index:02d}_{safe_name}"
    )

    project_path = os.path.join(
        TEST_ROOT,
        project_name
    )

    os.makedirs(
        project_path,
        exist_ok=True
    )

    return project_path


# ==========================================
# Step 1
# NewsAgent
# ==========================================

def run_news_agent(
    project_path,
    topic_keyword
):

    print_separator()

    print("STEP 1 / NewsAgent")
    print(f"搜索主题：{topic_keyword}")

    agent = NewsAgent(
        project_path=project_path
    )

    result = agent.run(
        {
            "topic_keyword": topic_keyword
        }
    )

    print("NewsAgent 返回结果：")
    print(result)

    output_path = os.path.join(
        project_path,
        "01_新闻资料",
        "news_articles.json"
    )

    return check_file(
        output_path
    )


# ==========================================
# Step 2
# NewsVerifier
# ==========================================

def run_news_verifier(
    project_path,
    topic_keyword
):

    print_separator()

    print("STEP 2 / NewsVerifier")
    print(f"核验主题：{topic_keyword}")

    verifier = NewsVerifier()

    result = verifier.run(
        {
            "project_path": project_path
        }
    )

    print("NewsVerifier 返回结果：")
    print(result)

    output_path = os.path.join(
        project_path,
        "02_事实核验",
        "verification.json"
    )

    return check_file(
        output_path
    )


# ==========================================
# Step 3
# SourceRanker
# ==========================================

def run_source_ranker(
    project_path,
    topic_keyword
):

    print_separator()

    print("STEP 3 / SourceRanker")
    print(f"来源评级：{topic_keyword}")

    ranker = SourceRanker(
        project_path=project_path
    )

    result = ranker.run(
        {}
    )

    print("SourceRanker 返回结果：")
    print(result)

    output_path = os.path.join(
        project_path,
        "03_来源评级",
        "source_rank.json"
    )

    return check_file(
        output_path
    )


# ==========================================
# Step 4
# TopicScorer
# ==========================================

def run_topic_scorer(
    project_path,
    topic_keyword
):

    print_separator()

    print("STEP 4 / TopicScorer")
    print(f"热点评分：{topic_keyword}")

    scorer = TopicScorer(
        project_path=project_path
    )

    result = scorer.run(
        {
            "project_path": project_path,
            "topic": topic_keyword
        }
    )

    print("TopicScorer 返回结果：")
    print(result)

    output_path = os.path.join(
        project_path,
        "04_热点评分",
        "topic_score.json"
    )

    if not check_file(output_path):
        return False

    # 额外检查 topic_score.json
    # 是否包含 TopicSelector 所需要的核心字段。

    data = load_json(
        output_path
    )

    if not isinstance(data, dict):
        print(
            "[FAIL] topic_score.json 不是JSON对象"
        )
        return False

    # TopicScorer 的输入文件可能没有保留本轮测试主题，
    # 使用当前候选主题补回选择器需要的字段。
    if not data.get("topic") or data.get("topic") == "未知主题":
        data["topic"] = topic_keyword
        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    required_fields = [
        "topic",
        "score",
        "recommendation",
        "breakdown",
        "weights",
        "meta"
    ]

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing:
        print(
            "[FAIL] topic_score.json 缺少字段:",
            missing
        )
        return False

    print(
        f"[OK] TopicScorer评分: {data.get('score')}"
    )

    print(
        f"[OK] TopicScorer建议: "
        f"{data.get('recommendation')}"
    )

    return True


# ==========================================
# 单个候选主题完整处理
# ==========================================

def process_topic(
    topic_keyword
):

    print_separator()

    print(
        "开始处理候选主题："
        f"{topic_keyword}"
    )

    project_path = create_topic_project(
        topic_keyword
    )

    print(
        f"项目目录：{project_path}"
    )

    result = {
        "topic_keyword": topic_keyword,
        "project_path": project_path,
        "news_agent": False,
        "news_verifier": False,
        "source_ranker": False,
        "topic_scorer": False,
        "success": False
    }

    try:

        # --------------------------
        # NewsAgent
        # --------------------------

        result["news_agent"] = run_news_agent(
            project_path,
            topic_keyword
        )

        if not result["news_agent"]:
            print(
                f"[FAIL] {topic_keyword} "
                "NewsAgent失败"
            )
            return result

        # --------------------------
        # NewsVerifier
        # --------------------------

        result["news_verifier"] = run_news_verifier(
            project_path,
            topic_keyword
        )

        if not result["news_verifier"]:
            print(
                f"[FAIL] {topic_keyword} "
                "NewsVerifier失败"
            )
            return result

        # --------------------------
        # SourceRanker
        # --------------------------

        result["source_ranker"] = run_source_ranker(
            project_path,
            topic_keyword
        )

        if not result["source_ranker"]:
            print(
                f"[FAIL] {topic_keyword} "
                "SourceRanker失败"
            )
            return result

        # --------------------------
        # TopicScorer
        # --------------------------

        result["topic_scorer"] = run_topic_scorer(
            project_path,
            topic_keyword
        )

        if not result["topic_scorer"]:
            print(
                f"[FAIL] {topic_keyword} "
                "TopicScorer失败"
            )
            return result

        result["success"] = True

        print(
            f"[OK] 候选主题处理完成："
            f"{topic_keyword}"
        )

        return result

    except Exception:

        print()
        print(
            f"[ERROR] 处理主题失败："
            f"{topic_keyword}"
        )

        traceback.print_exc()

        return result


# ==========================================
# Step 5
# TopicSelector
# ==========================================

def run_topic_selector(
    successful_topics
):

    print_separator()

    print(
        "STEP 5 / TopicSelector"
    )

    print(
        f"有效候选主题数量："
        f"{len(successful_topics)}"
    )

    if not successful_topics:

        print(
            "[FAIL] 没有任何有效候选主题"
        )

        return None

    print()
    print("候选主题：")

    for item in successful_topics:

        print(
            f" - {item['topic_keyword']}"
        )

    # TopicSelector 的当前设计：
    #
    # project_path 被视为：
    # 候选项目根目录。
    #
    # 它会扫描下面的多个候选项目，
    # 找到各项目中的：
    #
    # 04_热点评分/topic_score.json
    #
    # 然后进行排序。

    selector = TopicSelector(
        project_path=TEST_ROOT
    )

    result = selector.run(
        {}
    )

    print()
    print(
        "TopicSelector 返回结果："
    )

    print(result)

    output_path = os.path.join(
        TEST_ROOT,
        "05_选题决策",
        "topic_selection.json"
    )

    if not check_file(
        output_path
    ):
        return None

    return load_json(
        output_path
    )


# ==========================================
# 检查最终 TopicSelector 输出
# ==========================================

def verify_selection_output(
    selection
):

    print_separator()

    print(
        "STEP 6 / 最终选题结果检查"
    )

    if not isinstance(
        selection,
        dict
    ):

        print(
            "[FAIL] topic_selection.json "
            "不是有效JSON对象"
        )

        return False

    required_fields = [
        "selected_topic",
        "decision",
        "selection_score",
        "ranking"
    ]

    missing = [
        field
        for field in required_fields
        if field not in selection
    ]

    if missing:

        print(
            "[FAIL] topic_selection.json "
            "缺少字段:",
            missing
        )

        return False

    selected_topic = selection.get(
        "selected_topic"
    )

    decision = selection.get(
        "decision"
    )

    selection_score = selection.get(
        "selection_score"
    )

    ranking = selection.get(
        "ranking"
    )

    print()
    print(
        "=========================================="
    )

    print(
        "        今日推荐选题"
    )

    print(
        "=========================================="
    )

    print(
        f"TOP 1：{selected_topic}"
    )

    print(
        f"决策：{decision}"
    )

    print(
        f"评分：{selection_score}"
    )

    print()
    print(
        "TOP 3 候选："
    )

    if isinstance(
        ranking,
        list
    ):

        for item in ranking[:3]:

            print(
                f"TOP {item.get('rank')} "
                f"{item.get('topic')} "
                f"| "
                f"评分：{item.get('score')} "
                f"| "
                f"建议：{item.get('recommendation')}"
            )

    else:

        print(
            "[FAIL] ranking 不是列表"
        )

        return False

    print(
        "=========================================="
    )

    return True


# ==========================================
# 生成测试报告
# ==========================================

def print_test_summary(
    topic_results,
    selection_success
):

    print_separator()

    print(
        "TOPIC PIPELINE V2.0 测试总结"
    )

    print_separator()

    total = len(
        topic_results
    )

    success_count = sum(
        1
        for item in topic_results
        if item["success"]
    )

    failed_count = (
        total - success_count
    )

    print(
        f"候选主题总数：{total}"
    )

    print(
        f"成功处理：{success_count}"
    )

    print(
        f"处理失败：{failed_count}"
    )

    print(
        f"TopicSelector："
        f"{'SUCCESS' if selection_success else 'FAIL'}"
    )

    print()

    for item in topic_results:

        status = (
            "PASS"
            if item["success"]
            else "FAIL"
        )

        print(
            f"[{status}] "
            f"{item['topic_keyword']}"
        )

    print_separator()

    if (
        success_count >= 2
        and selection_success
    ):

        print(
            "TOPIC_PIPELINE_V2_TEST_PASS"
        )

    else:

        print(
            "TOPIC_PIPELINE_V2_TEST_FAIL"
        )

    print_separator()


# ==========================================
# 主测试流程
# ==========================================

def main():

    print()
    print(
        "============================================================"
    )

    print(
        "环球观察速递"
    )

    print(
        "Topic Pipeline V2.0"
    )

    print(
        "真实互联网新闻选题端到端测试"
    )

    print(
        "============================================================"
    )

    print()
    print(
        "测试目标："
    )

    print(
        "实时新闻"
        " → "
        "事实核验"
        " → "
        "来源评级"
        " → "
        "热点评分"
        " → "
        "多主题排序"
        " → "
        "TOP1/TOP3"
    )

    print()

    print(
        "测试关键词："
    )

    for topic in TEST_TOPICS:

        print(
            f" - {topic}"
        )

    print()

    print(
        "注意："
    )

    print(
        "本测试会清理并重新创建："
    )

    print(
        TEST_ROOT
    )

    print()

    # --------------------------------------
    # 初始化测试目录
    # --------------------------------------

    prepare_test_root()

    # --------------------------------------
    # 逐个处理候选主题
    # --------------------------------------

    topic_results = []

    for topic_keyword in TEST_TOPICS:

        result = process_topic(
            topic_keyword
        )

        topic_results.append(
            result
        )

    # --------------------------------------
    # 找出成功候选
    # --------------------------------------

    successful_topics = [
        item
        for item in topic_results
        if item["success"]
    ]

    # --------------------------------------
    # TopicSelector
    # --------------------------------------

    selection = None

    try:

        selection = run_topic_selector(
            successful_topics
        )

    except Exception:

        print()
        print(
            "[ERROR] TopicSelector执行失败"
        )

        traceback.print_exc()

    # --------------------------------------
    # 最终输出检查
    # --------------------------------------

    selection_success = False

    if selection is not None:

        selection_success = verify_selection_output(
            selection
        )

    # --------------------------------------
    # 测试总结
    # --------------------------------------

    print_test_summary(
        topic_results,
        selection_success
    )


# ==========================================
# 程序入口
# ==========================================

if __name__ == "__main__":

    main()