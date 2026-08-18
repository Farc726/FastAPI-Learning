from fastapi import FastAPI,Path

# 创建FastAPI实例
app=FastAPI()

# 路径操作装饰器
#通过GET方法 访问根路径"/"
@app.get("/")

# 定义路径操作函数
#异步函数
async def root():
# 返回响应内容
    return {"message":"Hello World666"}

# 通过GET方法 访问"/hello"路径
@app.get("/hello")

async def my_hello():
    #相应内容
    return {"msg":"开启我的FastAPI之旅!"}

@app.get("/user/hello")
async def first():
    return {"msg":"我正在学习FastAPI！一定会成功的！"}




