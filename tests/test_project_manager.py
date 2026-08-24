import sys
import os
import json


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from src.core.project_manager import ProjectManager


def test_project_manager_creates_project_structure(tmp_path):
    manager = ProjectManager()
    manager.project_root = str(tmp_path)

    project_path = manager.create_project("测试项目")

    assert os.path.isdir(project_path)
    assert os.path.isfile(
        os.path.join(project_path, "project.json")
    )

    expected_folders = [
        "01_新闻资料",
        "02_脚本",
        "03_分镜",
        "04_素材",
        "05_制作",
        "06_审核",
        "07_发布",
    ]

    for folder in expected_folders:
        assert os.path.isdir(
            os.path.join(project_path, folder)
        )

    with open(
        os.path.join(project_path, "project.json"),
        "r",
        encoding="utf-8",
    ) as f:
        project_data = json.load(f)

    assert project_data["title"] == "测试项目"
    assert project_data["status"] == "CREATED"
