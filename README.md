# FastAPI-Learning

黑马程序员 FastAPI 课程学习仓库。

## 目录结构

- `main.py`：仓库入口，保持最简
- `demos/`：知识点练习，按主题分文件夹（01_params、02_upload...），每个文件独立可运行
- `notes/`：学习笔记（Obsidian，由 sync_notes.ps1 自动同步）
- `sync_notes.ps1`：笔记同步脚本

## 运行方法

1. 激活虚拟环境：`venv\Scripts\activate`
2. 进入某个练习目录：`cd demos\01_params`
3. 运行该目录下的练习：`uvicorn demo_path_params:app --reload`
4. 浏览器打开 http://127.0.0.1:8000/docs 测试接口