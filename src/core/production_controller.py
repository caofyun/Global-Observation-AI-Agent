from src.core.project_manager import ProjectManager


class ProductionController:

    # ==========================================
    # AI视频生产总控 V1.0
    # ==========================================

    def __init__(self):

        # 初始化项目管理器
        self.project_manager = ProjectManager()

        # 当前项目
        self.current_project = None

    # ==========================================
    # 创建视频项目
    # ==========================================

    def create_project(self, title):

        print()
        print("正在创建视频项目……")

        project_path = self.project_manager.create_project(
            title
        )

        self.current_project = project_path

        print()
        print("项目创建成功！")
        print()
        print("项目路径：")
        print(project_path)

        print()
        print("当前状态：")
        print("CREATED")

        print()
        print("下一阶段：")
        print("新闻分析")

        return project_path