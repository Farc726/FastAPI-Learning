# 导包
from fastapi import FastAPI,HTTPException,UploadFile,Form,File
from pydantic import BaseModel,Field,EmailStr,ConfigDict
from sqlalchemy import create_engine,Integer,String,Column
from sqlalchemy.orm import DeclarativeBase,Session
import time,os
# 用数据库加ORM的前置准备
#加载数据库
engine_m=create_engine("sqlite:///members.db")
engine_p=create_engine("sqlite:///pets.db")

# 初始化好各类
#1.ORM相关
#1.1 ORM基类
class Base(DeclarativeBase):
    pass
#1.2member普通类
class Member(Base):
###!!!表头忘记写了 语法忘记了
    __tablename__="members"
    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)
    
#1.3pet普通类
class Pet(Base):
    __tablename__="pets"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    kind=Column(String)
    age=Column(Integer)
    image_path=Column(String)
    owner_id=Column(Integer)

# 建表
Member.metadata.create_all(engine_m)
Pet.metadata.create_all(engine_p)

#2.fastapi相关
#2.1member/pet基础类
class MemberBase(BaseModel):
    username:str=Field(...,min_length=3,max_length=20)
    email:EmailStr
class PetBase(BaseModel):
    name:str=Field(...)
    kind:str=Field(...)
    age:int
    
    
    
#2.2member/pet创建类
class MembetCreate(MemberBase):
    password:str=Field(...,min_length=6,max_length=20)
class PetCreate(PetBase):
    image_path:str
    owner_id:int=Field(...)
#2.3member/pet输出类
class MemberOut(BaseModel):
    id:int
    username:str=Field(...,min_length=3,max_length=20)
    model_config=ConfigDict(from_attributes=True)
class PetOut(BaseModel):
    id:int
    name:str=Field(...)
    kind:str=Field(...)
    age:int
    model_config=ConfigDict(from_attributes=True)
    
# 功能实现
app=FastAPI()

#会员注册功能（添加 写入）
@app.post("/members/add",response_model=MemberOut)
def member_create(member:MembetCreate):
    with Session(engine_m) as session:
        new_memebr=Member(**member)
        member_list=session.query(Member).all()
        for m in member_list:
            if(m.username==new_memebr.username):
                raise HTTPException(401,detail="系统中已有该用户名~")
            else:
                session.add(new_memebr)
                session.commit()
                session.refresh(new_memebr)
                return new_memebr
    
#会员登录功能
class LoginIn(BaseModel):
    username:str=Field(...)
    password:str=Field(...)
class LoginOut(BaseModel):
    msg:str
    username:str
    
@app.post("/members/login",response_model=LoginOut)
def member_login(member:LoginIn):
    with Session(engine_m) as session:
        member_list=session.query(Member).all()
        for m in member_list:
            if member.username==m.username and member.password==m.password:
                return {"msg":"登录成功~","username":m.username}
        raise HTTPException(404,detail="用户名或密码错误 未找到该用户~")
    
#添加宠物
UPLOAD_DIR="my_project"
@app.post("/pets/add",response_model=PetOut)
# 这个有意思 涉及表单 文件上传 文件路径 时间戳保存唯一文件名
def get_pet(
    name:str=Form(...),
    kind:str=Form(...),
    age:int=Form(...),
    owner_id:int=Form(...),
    photo:UploadFile=File(...)
):
    #文件名 保证唯一
    filename=f"{int(time.time())}_{photo.filename}"
    #生成文件路径
    save_path=os.path.join(UPLOAD_DIR,filename)
    with open (filename,"wb") as f:
        if not f:
            raise HTTPException(422,detail="图片上传失败")
    new_pet=Pet(name,kind,age,save_path,owner_id)
    with Session(engine_p) as session:
        if session:
            session.add(new_pet)
            session.commit()
            session.refresh(new_pet)
            return new_pet
        raise HTTPException(422,detail="信息上传失败~")
            
     
    
#宠物列表
@app.get("pets/get_pet",response_model=list[PetOut])
def get_pets():
    with Session(engine_p) as session:
        pet_list=session.query(Pet).all()
        if not pet_list:
            raise HTTPException(404,detail="列表中未找到任何宠物~")
        return pet_list
        
# 查询单个宠物
@app.get("pets/get_pet/{pet_id}",response_model=PetOut)
def get_pet(pet_id:int):
    with Session(Pet) as session:
        pet_list=session.query(Pet).all()
        for p in pet_list:
            if p.id==pet_id:
                return p
        raise HTTPException(404,detail="未找到您要查找的宠物")
    
#更新
@app.put("/pets/update_pet/{pet_id}",response_model=PetOut)
def update_pet(
    pet_id:int,
    name:str=Form(...),
    kind:str=Form(...),
    age:int=Form(...),
    owner_id:int=Form(...),
    photo:UploadFile=File(...)
):
# 为什么要用时间戳来保证不会相互覆盖？？？
    filename=f"{int(time.time())}_{photo.filename}"
    save_path=os.path.join(filename)
    with open(filename,"wb") as f:
        if not f:
            raise HTTPException(422,detail="文件上传失败~")
    with Session(engine_p) as session:
        update_pet=session.query(Pet).filter(Pet.id==pet_id)
        if update_pet:
            update_pet.name=name
            update_pet.kind=kind
            update_pet.age=age
            update_pet.image_path=save_path
            update_pet.owner_id=owner_id
            session.commit()
            session.refresh(update_pet)
            return update_pet
    raise HTTPException(422,detail="信息更新失败~")
            
        
                
#删除
@app.post("pets/delete/{pet_id}")
def pet_delete(pet_id:int):
    with Session(engine_p) as session:
        delete_pet=session.query(Pet).filter(Pet.id==pet_id).first()
        if delete_pet:
            session.delete(delete_pet)
            session.commit()
            return {"msg":"删除成功","name":delete_pet.name}
    raise HTTPException(422,detail="删除失败,请联系管理员进行处理~")
                
            