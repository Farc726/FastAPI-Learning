# 导包
#FastAPI 路由必须以/开头    注意要避免同名路由的存在   HTTP报错的语义要严谨
from fastapi import FastAPI,HTTPException,UploadFile,Form,File
from pydantic import BaseModel,Field,EmailStr,ConfigDict
from sqlalchemy import create_engine,Integer,String,Column
from sqlalchemy.orm import DeclarativeBase,Session
import time,os
from datetime import datetime
# 用数据库加ORM的前置准备
#加载数据库
#用了两个数据库（members.db + pets.db）
#会员和宠物应该共用一个库，owner_id 才有意义。
# 一个引擎一个文件
engine=create_engine("sqlite:///vip.db")

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

# 建表 用的是Base所有继承Base的模型都登记在metadata名册中 用create_all方法就是按照整本名册建表 所以在这里就是建了两个表
Base.metadata.create_all(engine)

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
class MemberCreate(MemberBase):
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
    image_path:str
    model_config=ConfigDict(from_attributes=True)
    
# 功能实现
app=FastAPI()

#会员注册功能（添加 写入）
@app.post("/members/add",response_model=MemberOut)
def member_create(member:MemberCreate):
# engine -- session
    with Session(engine) as session:
# 先将这个类转为字典再解包
        new_member=Member(**member.model_dump())
        m=session.query(Member).filter(Member.username==member.username).first()
        if m:
            raise HTTPException(401,detail="系统中已有该用户名~")
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        return new_member
#查询全部会员
@app.get("/members/get",response_model=list[MemberOut])
def get_members():
    with Session(engine) as session:
        member_list=session.query(Member).all()
        if member_list:
            return member_list
    raise HTTPException(404,"系统中暂无注册会员~")
    
#会员登录功能
class LoginIn(BaseModel):
    username:str=Field(...)
    password:str=Field(...)
class LoginOut(BaseModel):
    msg:str
    username:str
    
@app.post("/members/login",response_model=LoginOut)
def member_login(member:LoginIn):
    with Session(engine) as session:
        member_list=session.query(Member).all()
        for m in member_list:
            if member.username==m.username and member.password==m.password:
                return {"msg":"登录成功~","username":m.username}
        raise HTTPException(404,detail="用户名或密码错误 未找到该用户~")
    
#添加宠物
UPLOAD_DIR = "uploads"
# 关键：先创建，不存在就建
os.makedirs(UPLOAD_DIR, exist_ok=True)  
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
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S%f')}_{photo.filename}"
    #生成文件路径
    save_path=os.path.join(UPLOAD_DIR,filename)
    with open (save_path,"wb") as f:
        f.write(photo.file.read())
        if not f:
            raise HTTPException(422,detail="图片上传失败")
#SQLAlchemy 模型不支持位置参数，必须关键字：
    new_pet=Pet(name=name,kind=kind,age=age,image_path=save_path,owner_id=owner_id)
    with Session(engine) as session:
        if session:
            session.add(new_pet)
            session.commit()
            session.refresh(new_pet)
            return new_pet
        raise HTTPException(422,detail="信息上传失败~")
            
     
    
#某位会员的所有宠物列表
@app.get("/members/get_pet/{member_id}",response_model=list[PetOut])
def get_pets(member_id:int):
    with Session(engine) as session:
        my_pet_list=session.query(Pet).filter(Pet.owner_id==member_id).all()
        if my_pet_list:
            return my_pet_list
    raise HTTPException(404,detail="该会员未注册或其名下暂无宠物~")
        
        
# 查询单个宠物
@app.get("/pets/get_pet/{pet_id}",response_model=PetOut)
def get_pet(pet_id:int):
    with Session(engine) as session:
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
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S%f')}_{photo.filename}"
    save_path=os.path.join(UPLOAD_DIR,filename)
    with open(save_path,"wb") as f:
        f.write(photo.file.read())
        if not f:
            raise HTTPException(422,detail="文件上传失败~")
    with Session(engine) as session:
        update_pet=session.query(Pet).filter(Pet.id==pet_id).first()
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
@app.post("/pets/delete/{pet_id}")
def pet_delete(pet_id:int):
    with Session(engine) as session:
        delete_pet=session.query(Pet).filter(Pet.id==pet_id).first()
        if delete_pet:
            session.delete(delete_pet)
            session.commit()
            return {"msg":"删除成功","name":delete_pet.name}
    raise HTTPException(422,detail="删除失败,请联系管理员进行处理~")
                
            