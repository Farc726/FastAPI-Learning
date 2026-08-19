from fastapi import FastAPI,Path,Query
from pydantic import BaseModel,Field

app=FastAPI()
pets=[]
next_id=1

@app.get("/")
async def hello():
    return {"welcome":"欢迎您使用此系统~"}
# 1.请求体参数--添加宠物
class Pet(BaseModel):
    name:str=Field(...,min_length=2,max_length=20,description="2~10个字符")
    kind:str=Field(...,min_length=2,max_length=10,description="2~10个字符(比如:'cat'、'dog')")
    age:int=Field(...,ge=0,le=30,description="0~30的整数")
    price:float=Field(default=0,ge=0,description="选填年龄大于等于0")
    
@app.post("/pet")
async def input_pet(pet:Pet):
    global next_id
    new_pet=pet.model_dump()
    new_pet["id"]=next_id
    pets.append(new_pet)
    next_id+=1
    return new_pet



# 2.路径参数--按编号查询宠物
@app.get("/pet/{pet_id}")
async def pet_id(pet_id:int=Path(ge=1,le=100)):
    for pet in pets:
        if pet["id"]==pet_id:
            return pet
    return {"msg":"未找到该宠物~"}    
        

#3.查询参数--按种类筛选宠物列表
@app.get("/pet")
async def pet_kind(kind:str=Query(default="全部",min_length=1,max_length=20)):
    if kind=="全部":
        return pets
#print(pet)  !!!只是打印到服务器控制台，不会返回给客户端
    result=[pet for pet in pets if pet["kind"]==kind]
    return result        
             

    