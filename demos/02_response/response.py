from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel,ConfigDict

app=FastAPI()

#1.默认json 不再赘述
@app.get("/")
async def root():
    return {"message":"Hello word"}

# 2.接口--响应HTML代码
# 2.1.导入
# 2.2.在装饰器中明确响应类型
# 2.3.注意HTML的格式
@app.get("/html",response_class=HTMLResponse)
async def get_html():
    return "<h1>一级标题</h1>"

# 3.文件
# 接口--返回一张图片内容
# 3.1导入
# 3.2 return FileResponse(Path)
@app.get("/file")
async def get_file():
    Path="./demos./file./1.png"
    return FileResponse(Path)

#4.返回Pydantic模型
class Item(BaseModel):
    name:str
    age:int
    price:float
    
@app.get("/item")
async def get_item(item:Item):
    return item

# 5.返回自定义的类
class PetOut(BaseModel):
    name:str
    age:int   
# PetOut 想从 Pet 对象的属性（self.name、self.age）里取数据，必须告诉 Pydantic 允许读属性
#from_attributes=True 作用：允许 Pydantic 读取普通对象的属性，不止接收字典
    model_config=ConfigDict(from_attributes=True)

class Pet():
    def __init__(self,name,age,price):
        self.name=name
        self.age=age
        self.price=price

@app.get("/pet",response_model=PetOut)
async def get_pet():
    pet=Pet("欢欢",1,99)
    return pet
#过滤
    
#异常处理--使用HTTPException
# 1.导入
# 2.按照需求写判断条件
# 3.抛出异常--参数具体见笔记
# 需求：按id查询新闻（1~6）
@app.get("/news/{id}")
async def get_news(id:int):
    id_list=[1,2,3,4,5,6]
    if id not in id_list:
        raise HTTPException(status_code=404,detail="您查找的新闻不存在~")
    return {"id":id}