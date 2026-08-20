import os
import sys
import json
import shutil
import traceback


# ==========================================
# 添加项目根目录到Python路径
# ==========================================

PROJECT_ROOT_PATH = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT_PATH
)


from src.agents.news_agent import NewsAgent
from src.agents.news_verifier import NewsVerifier
from src.agents.source_ranker import SourceRanker



# ==========================================
# Global Observation AI Agent V2.0
#
# Pipeline Integration Test
#
# 测试链路：
#
# NewsAgent
#      |
#      ↓
# news_articles.json
#
# NewsVerifier
#      |
#      ↓
# verification.json
#
# SourceRanker
#      |
#      ↓
# source_rank.json
#
# ==========================================


TEST_PROJECT_NAME = "test_v2_pipeline_project"


PROJECT_ROOT = os.path.join(
    "projects",
    TEST_PROJECT_NAME
)



# ==========================================
# 工具函数
# ==========================================


def check_file(path):

    if os.path.exists(path):

        print(
            f"[OK] 文件存在: {path}"
        )

        return True


    else:

        print(
            f"[FAIL] 文件不存在: {path}"
        )

        return False



def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



# ==========================================
# 清理旧测试目录
# ==========================================


def prepare_project():


    if os.path.exists(
        PROJECT_ROOT
    ):

        shutil.rmtree(
            PROJECT_ROOT
        )


    os.makedirs(
        PROJECT_ROOT,
        exist_ok=True
    )


    print(
        "测试项目初始化完成:"
    )

    print(
        PROJECT_ROOT
    )



# ==========================================
# 测试 NewsAgent
# ==========================================


def test_news_agent():


    print()

    print(
        "========== NewsAgent V2.0 =========="
    )


    agent = NewsAgent(
        project_path=PROJECT_ROOT
    )


    result = agent.run(

        {
            "topic_keyword":
            "美国航母部署"

        }

    )


    print(
        result
    )


    path = os.path.join(

        PROJECT_ROOT,

        "01_新闻资料",

        "news_articles.json"

    )


    return check_file(path)



# ==========================================
# 测试 NewsVerifier
# ==========================================


def test_news_verifier():


    print()

    print(
        "========== NewsVerifier V2.0 =========="
    )


    verifier = NewsVerifier(

        project_path=PROJECT_ROOT

    )


    result = verifier.run(

        {}

    )


    print(
        result
    )


    path = os.path.join(

        PROJECT_ROOT,

        "02_事实核验",

        "verification.json"

    )


    return check_file(path)



# ==========================================
# 测试 SourceRanker
# ==========================================


def test_source_ranker():


    print()

    print(
        "========== SourceRanker V2.0 =========="
    )


    ranker = SourceRanker(

        project_path=PROJECT_ROOT

    )


    result = ranker.run(

        {}

    )


    print(
        result
    )


    path = os.path.join(

        PROJECT_ROOT,

        "03_来源评级",

        "source_rank.json"

    )


    return check_file(path)



# ==========================================
# 验证JSON结构
# ==========================================


def verify_structure():


    print()

    print(
        "========== 数据结构检查 =========="
    )


    checks = []



    # news_articles

    article_path = os.path.join(

        PROJECT_ROOT,

        "01_新闻资料",

        "news_articles.json"

    )


    articles = load_json(

        article_path

    )


    if "articles" in articles:

        print(
            "[OK] news_articles.json"
        )

        checks.append(True)


    else:

        print(
            "[FAIL] news_articles.json结构错误"
        )

        checks.append(False)



    # verification


    verification_path = os.path.join(

        PROJECT_ROOT,

        "02_事实核验",

        "verification.json"

    )


    verification = load_json(

        verification_path

    )


    required_verification_fields = [

        "topic",

        "articles",

        "sources",

        "facts",

        "conflicts",

        "uncertainties",

        "verification_status",

        "confidence"

    ]


    missing = [

        x for x in required_verification_fields

        if x not in verification

    ]


    if not missing:

        print(

            "[OK] verification.json字段完整"

        )

        checks.append(True)


    else:

        print(

            "[FAIL] verification缺少:",
            missing

        )

        checks.append(False)



    # source_rank


    rank_path = os.path.join(

        PROJECT_ROOT,

        "03_来源评级",

        "source_rank.json"

    )


    rank = load_json(

        rank_path

    )


    if (

        "topic" in rank

        and

        "sources" in rank

    ):

        print(

            "[OK] source_rank.json结构正确"

        )

        checks.append(True)


    else:

        print(

            "[FAIL] source_rank结构错误"

        )

        checks.append(False)



    return all(checks)



# ==========================================
# 主测试流程
# ==========================================


def main():


    print()

    print(
        "================================"
    )

    print(
        "V2.0 Agent Pipeline Integration Test"
    )

    print(
        "================================"
    )


    try:


        prepare_project()


        result1 = test_news_agent()


        result2 = test_news_verifier()


        result3 = test_source_ranker()


        result4 = verify_structure()



        final = (

            result1

            and

            result2

            and

            result3

            and

            result4

        )


        print()

        print(
            "================================"
        )


        if final:

            print(
                "PIPELINE_TEST_PASS"
            )

        else:

            print(
                "PIPELINE_TEST_FAIL"
            )


        print(
            "================================"
        )



    except Exception:


        print()

        print(
            "测试异常"
        )

        traceback.print_exc()



if __name__ == "__main__":

    main()