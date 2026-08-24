from src.core.project_manager import ProjectManager
from src.core.pipeline_runner import PipelineRunner


class ProductionController:

    # ==========================================
    # AI视频生产总控 V2.0
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
        print("Pipeline执行")

        return project_path

    # ==========================================
    # 执行生产Pipeline
    # ==========================================

    def run_pipeline(self, request):
        """
        执行AI视频生产Pipeline。

        request:
        {
            "title": "新闻主题",
            "topic": "主题",
            "options": {}
        }
        """

        title = request.get("title") or request.get("topic")

        if not title:
            return {
                "status": "FAILED",
                "error": "missing title/topic"
            }

        project_path = self.create_project(title)

        pipeline_input = {
            "project_path": project_path,
            "topic": request.get("topic", title),
            "options": request.get("options", {})
        }

        runner = PipelineRunner()

        result = runner.run(pipeline_input)

        return {
            "status": result.get("pipeline_status", "UNKNOWN"),
            "project_path": project_path,
            "pipeline_result": result
        }
