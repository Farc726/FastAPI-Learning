from fastapi import FastAPI, Path

app = FastAPI()

# 路径参数：在请求路径 {} 中定义，处理函数写同名的形参并做类型注解
# 注意路由顺序：固定路径放在上面，参数路径放在下面（原因详见笔记）

@app.get("/user/password")
async def user_password():
    return {"password": "无权限不可随意查看"}

@app.get("/user/{id}")
async def get_user(id: int = Path(..., gt=0, le=100, description="请输入1~100之间的数字")):
    return {"id": id, "title": f"欢迎您第{id}号用户"}