from fastapi import FastAPI,Path,Query
from pydantic import BaseModel,Field

app=FastAPI()

@app.get("/")
async def get_app():
    return {"welcome":"欢迎进入路由知识点的学习"}

# 1.路径参数
# 在请求路径部分{}定义路径参数
# 在处理函数部分写同名的函数形参 并做好类型注解
# 在函数体的响应部分即可使用传入的路径参数

# 1.1类型注解（python 原生注解就是：int，若想额外加信息）
# 导入使用Path函数
# 原生注解基础之上“=”赋值为 Path函数  小括号里面写参数 description="添加描述"
@app.get("/user/{id}")
async def get_user(id:int=Path(...,gt=0,le=100,description="请输入1~100之间的数字")):
    return {"id":id,"title":f"欢迎您第{id}号用户"}

@app.get("/user/hello/{name}")
async def get_user_name(name:str=Path(...,min_length=2,max_length=10,description="请输入用户名2~10个字符~")):
    return {"name":name,"word":f"欢迎用户{name}使用本app"}


#2.查询参数
# 示例：需求：设计接口查询图书，要求携带两个查询参数：图书分类和价格
# 参数具体要求：
# 图书分类：默认值为 Python 开发，长度限制 5 ~ 255
# 价格：限制大小范围 50 ~ 100
@app.get("/library/book")
# 1.导入Query
# 原生注解基础之上“=”赋值为 Query函数  
# 可以有默认值 取代...的位置即可
async def get_book(category:str=Query("Python开发",min_length=5,max_length=255),price:float=Query(ge=50,le=100)):
    return {"类别:":category,"价格":price}


# 3.请求体参数
# 定义类型
# 类型注解
# 导入pydantic中的 Field函数--类型注解

# 需求：设计接口新增图书，图书信息包含：书名、作者、出版社、售价
# 具体要求如下：
# - 书名：不能为空；长度 2 ~ 20
# - 作者：长度 2 ~ 10
# - 出版社：默认值“黑马出版社”
# - 售价：不能为空；价格大于0元
class Book(BaseModel):
    name:str=Field(...,min_length=2,max_length=20,description="书名应在2~20个字符之间~")
    author:str=Field(...,min_length=2,max_length=10,description="作者名应在2~10个字符之间~")
    publisher:str=Field(default="黑马出版社")
    price:int=Field(...,gt=0)
    
@app.post("/library/new_book")
async def new_book(book:Book):
    return book

    
