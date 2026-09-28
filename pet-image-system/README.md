# 宠物图片管理系统（Pet Image System）

基于 **FastAPI + SQLAlchemy + SQLite** 的宠物信息管理后端：会员注册登录、宠物档案增删改查、宠物照片上传与存储。

> 当前进度：后端接口已全部实现并跑通；图片自动识别（MobileNet）与前端页面开发中。

## 功能

### 会员模块
- 注册：用户名/邮箱格式校验（`EmailStr`）、用户名查重
- 登录：用户名 + 密码校验
- 会员列表查询

### 宠物模块
- 添加宠物：表单 + 照片上传（`Form` + `UploadFile` 混合）
- 宠物列表、单个查询、按会员查询名下宠物
- 更新宠物信息（可替换照片）
- 删除宠物

### 数据与文件
- SQLite 持久化（重启服务数据不丢失）
- 上传图片按「时间戳_原名」命名，保存在 `uploads/`
- 数据库只保存图片路径（`image_path`），不存文件本体

## 技术栈

| 层次 | 技术 |
|---|---|
| Web 框架 | FastAPI |
| 数据校验 | Pydantic（`EmailStr`、`Field`、`from_attributes`） |
| ORM | SQLAlchemy 2.x（`DeclarativeBase`、`Session`） |
| 数据库 | SQLite |
| 文件上传 | `python-multipart` + `UploadFile` |
| 依赖注入 | `Depends(get_db)` 统一管理数据库会话 |

## 项目结构

    pet-image-system/
    ├── pet_vip_system.py    # 主程序：模型 + 校验 + 接口
    ├── vip.db               # SQLite 数据库
    └── uploads/             # 上传的图片（已在 .gitignore 中忽略）

## 运行方法

1. 安装依赖

       pip install fastapi uvicorn sqlalchemy "pydantic[email]" python-multipart

2. 启动服务（在本目录下）

       uvicorn pet_vip_system:app --reload

3. 打开交互式接口文档

       http://127.0.0.1:8000/docs

## 接口一览

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/members/add` | 会员注册 |
| POST | `/members/login` | 会员登录 |
| GET | `/members/get` | 会员列表 |
| POST | `/pets/add` | 添加宠物（含照片上传） |
| GET | `/pets/get_pet` | 宠物列表 |
| GET | `/pets/get_pet/{pet_id}` | 查询单个宠物 |
| GET | `/members/get_pet/{member_id}` | 查询某会员名下宠物 |
| PUT | `/pets/update_pet/{pet_id}` | 更新宠物信息 |
| POST | `/pets/delete/{pet_id}` | 删除宠物 |

## 截图

> 待补充：接口文档页、上传宠物照片、宠物列表

## 开发计划

- [ ] 接入 MobileNet 预训练模型：上传照片时自动识别宠物种类并存入数据库
- [ ] 前端页面：网页上传、识别结果展示、历史列表
- [ ] 结构重构：拆分 database / models / schemas / routers 分层
- [ ] 密码哈希存储（当前为学习阶段的明文存储，真实项目需加密）

## 说明

这是学习过程中完成的实践项目，目的是打通「FastAPI 接口 + ORM 数据库 + 文件上传」的完整链路，代码规范与结构仍在持续优化中。