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


from src.agents.news_verifier import NewsVerifier


# ==========================================
# 输入项目路径
# ==========================================

project_path = input(
    "请输入需要核验的视频项目路径："
).strip()


# ==========================================
# 检查项目路径
# ==========================================

if not project_path:

    print(
        "项目路径不能为空"
    )

    sys.exit()


if not os.path.exists(
    project_path
):

    print(
        "项目路径不存在："
    )

    print(
        project_path
    )

    sys.exit()


# ==========================================
# 创建NewsVerifier
# ==========================================

verifier = NewsVerifier()


# ==========================================
# 执行新闻核验
# ==========================================

result = verifier.run({

    "project_path":
        project_path

})


# ==========================================
# 输出结果
# ==========================================

print()
print("==============================")
print("NewsVerifier测试结果")
print("==============================")


print(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=4
    )
)


# ==========================================
# 输出Agent状态
# ==========================================

print()
print("==============================")
print("Agent状态")
print("==============================")


print(
    verifier.get_status()
)