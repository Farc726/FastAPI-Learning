# FastAPI-Learning

Python 后端学习仓库：学习笔记 + 知识点练习 + 实践项目。

## 实践项目

### 🐾 [宠物图片管理系统](pet-image-system/)

FastAPI + SQLAlchemy + SQLite 实现的宠物信息管理后端：会员注册登录、宠物档案增删改查、照片上传。

→ [查看项目说明](pet-image-system/README.md)

## 目录结构

- `pet-image-system/`：实践项目（宠物图片管理系统）
- `demos/`：知识点练习，按主题分文件夹，每个文件可独立运行
- `notes/`：学习笔记（Obsidian，由 `sync_notes.ps1` 自动同步）
- `sync_notes.ps1`：笔记同步脚本

## 学习内容一览

| 主题 | 练习目录 |
|---|---|
| 路由与参数（Path / Query / Body） | `demos/01_params` |
| 响应模型（response_model） | `demos/02_response` |
| 表单数据（Form） | `demos/03_form_data` |
| 文件上传（UploadFile） | `demos/04_file_upload` |
| SQL 基础 | `demos/05_sql` |
| ORM（SQLAlchemy） | `demos/06_ORM` |
| 图片分类（MobileNet） | `demos/07_mobilenet` |

## 运行方法

1. 激活虚拟环境：`venv\Scripts\activate`
2. 进入某个练习目录：`cd demos\01_params`
3. 运行：`uvicorn demo_path_params:app --reload`
4. 浏览器打开 http://127.0.0.1:8000/docs