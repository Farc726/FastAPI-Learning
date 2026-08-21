#表单数据
# 这个例子也暴露了你的一个误区：
#关于参数类型的确定 与get/post方法有无绝对性关系-----分析见笔记（参数标题下）

#1.导入Form
#2.普通零散参数---函数参数后直接=Form()
#3.若为BaseModel类：
    # 先导入：from typing import Annotated 
    # 再在函数参数位置=Annotated[类型，Form()]
    # 绝对不要把=Form() 写到BaseModel类里面！！

from fastapi import FastAPI,Form
from pydantic import BaseModel
from typing import Annotated
app=FastAPI()

class User(BaseModel):
    username:str
    password:str
    
    
@app.post("/login1")
async def login_1(user:User):
    return user

@app.post("/login2")
async def login_2(username:str,password:str):
    return {"username":username,"password":password}

@app.post("/login3")
async def login_3(username:str=Form(...),password:str=Form(...)):
    return {"username":username,"password":password}

@app.post("/login4")
async def login_4(user:Annotated[User,Form(...)]):
    return user

