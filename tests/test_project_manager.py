#from src.core.project_manager import ProjectManager
import sys
import os

# 将项目根目录添加到 sys.path 中，以便导入模块
sys.path.append(os.path.dirname
                (os.path.dirname(os.path.abspath(__file__)
                                 )
                )
)
from src.core.project_manager import ProjectManager

manager = ProjectManager()



title = input(
    "请输入视频标题："
)



path = manager.create_project(
    title
)



print()

print("====================")

print("项目创建成功")

print(path)

print("====================")