
from pathlib import Path


# ==========================================
# AI视频生产智能体
# Phase 1 第一步
# 创建项目基础代码结构
# ==========================================

# 获取当前脚本所在的项目根目录
project_root = Path(__file__).resolve().parent


# ==========================================
# 需要创建的目录
# ==========================================

folders = [
    "src",
    "src/agents",
    "src/core",
    "src/data",
    "src/utils",
    "projects",
    "tests",
    "config",
]


# ==========================================
# 创建目录
# ==========================================

print("==============================")
print(" AI视频生产智能体")
print(" 项目结构创建程序 V1.0")
print("==============================")
print()

for folder in folders:

    folder_path = project_root / folder

    folder_path.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"已创建/确认：{folder}")


# ==========================================
# 创建基础程序文件
# ==========================================

files = [
    "main.py",
]


for file in files:

    file_path = project_root / file

    if not file_path.exists():

        file_path.touch()

        print(f"已创建文件：{file}")


# ==========================================
# 完成
# ==========================================

print()
print("==============================")
print(" 项目代码结构创建完成")
print("==============================")
