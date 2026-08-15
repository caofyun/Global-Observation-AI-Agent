import os
import json
from datetime import datetime


class ProjectManager:


    def __init__(self):

        # 获取项目根目录

        self.root_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )


        # 项目存放目录

        self.project_root = os.path.join(
            self.root_path,
            "projects"
        )


        os.makedirs(
            self.project_root,
            exist_ok=True
        )



    # ==========================
    # 创建视频项目
    # ==========================

    def create_project(self, title):


        # 创建时间

        date = datetime.now().strftime(
            "%Y%m%d"
        )


        # 项目名称

        project_name = (
            date
            +
            "_"
            +
            title.replace(" ","_")
        )


        project_path = os.path.join(
            self.project_root,
            project_name
        )


        # 项目目录

        folders = [

            "01_新闻资料",

            "02_脚本",

            "03_分镜",

            "04_素材",

            "05_制作",

            "06_审核",

            "07_发布"

        ]


        for folder in folders:

            os.makedirs(
                os.path.join(
                    project_path,
                    folder
                ),
                exist_ok=True
            )


        # 创建project.json


        project_data = {


            "project_id":
                project_name,


            "title":
                title,


            "status":
                "CREATED",


            "created_time":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),



            "agents_status":{


                "news_agent":
                    "waiting",


                "script_agent":
                    "waiting",


                "material_agent":
                    "waiting",


                "video_agent":
                    "waiting"


            }

        }



        json_path = os.path.join(
            project_path,
            "project.json"
        )


        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                project_data,
                f,
                ensure_ascii=False,
                indent=4
            )


        return project_path


