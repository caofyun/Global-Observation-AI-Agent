from src.core.production_controller import ProductionController


# ==========================================
# 环球观察速递
# AI视频生产智能体 V1.0
# ==========================================


def main():

    print("================================")
    print(" 环球观察速递")
    print(" AI视频生产智能体 V1.0")
    print("================================")

    print()

    # 创建AI生产总控
    controller = ProductionController()

    # 输入新闻选题
    title = input(
        "请输入新闻选题："
    ).strip()

    # 检查输入
    if not title:

        print()
        print("新闻选题不能为空。")
        return

    # 创建视频项目
    controller.create_project(
        title
    )


if __name__ == "__main__":

    main()