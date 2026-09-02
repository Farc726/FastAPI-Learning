# 昨天学的主要是将一个系统录入的信息保存 重启程序依然不会丢失 
# 所以需要数据库来存放保存的信息 
# 我现在用到的是sqlite数据库 相比于原生的SQL语言 我昨天学习了更简洁易读的ORM方法 与数据库进行交流
# 同时通过同步函数与FASTapi结合 这样来完成成绩管理系统的增删改查操作
# 今天复习我们来写宠物店vip管理系统

# 注意
# 1.关于什么时候engine做参数：
    #1.1建表的时候：Base.metadata.create_all(engine) 告诉SQLAIchemy向哪一个数据库建表
    #1.2建立每一个接口的时候 告诉Session用这个窗口去哪个数据库干活
#2.请求体一般关于提交内容也就是写-一般与post结合   --登录一般用post 因为密码不可以进URL且一般认为 get无副作用不改变任何状态 而 登陆成功后 按理说是要创建会话状态的 


# 导包
from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel,Field,EmailStr,ConfigDict
from sqlalchemy.orm import DeclarativeBase,Session
from sqlalchemy import Column,String,Integer,create_engine

#类一：会员基础的类
class MemberBase(BaseModel):
    username:str=Field(...,min_length=3,max_length=20)
    email:EmailStr
    
#类二：进行查询操作时候 返回的会员信息
class MemberOut(MemberBase):
    id:int
    model_config=ConfigDict(from_attributes=True)
    
#类三：进行创建操作的时候 输入的会员的信息
class MemberCreate(MemberBase):
    password:str=Field(...,min_length=6,max_length=20)
    
#类四：进行登录操作时，输入的会员信息
class LoginIn(BaseModel):
    username:str=Field(...,min_length=3,max_length=20)
    password:str=Field(...,min_length=6,max_length=20)

#ORM操作需要的基类
class Base(DeclarativeBase):
    pass
#存放于数据库中的会员信息
class Member(Base):
    __tablename__="member"
    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String)
    email = Column(String(255), nullable=False)
    password=Column(String)
    
# 创建引擎 与数据库建立连接
engine=create_engine("sqlite:///vip.db")
# 建表
Base.metadata.create_all(engine)

app=FastAPI()

# 操作一：
# 注册会员
@app.post("/members",response_model=MemberOut)
def create_member(member:MemberCreate):
    with Session(engine) as session:
        #添加查重操作
        exists=session.query(Member).filter(Member.username==member.username).first()
        if exists:
            raise HTTPException(400,detail="该用户名已存在~")
        new_member=Member(**member.model_dump())
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        return new_member

#操作二：
#查询全部会员
@app.get("/members/get",response_model=list[MemberOut])
def get_members():
    with Session(engine) as session:
        member_list=session.query(Member).all()
        if member_list:
            return member_list
    raise HTTPException(404,detail="列表中无任何用户，查询失败")

#操作三：
#查询单个人
@app.get("/members/get/{id}",response_model=MemberOut)
def get_member(id:int):
    with Session(engine) as session:
        member=session.query(Member).filter(Member.id==id).first()
        if member:
            return member
    raise HTTPException(404,detail="未找到此用户~")

#操作四：
#登录操作
class LoginInOut(BaseModel):
    msg:str
    member:MemberOut
    model_config=ConfigDict(from_attributes=True)
@app.post("/members/loginin",response_model=LoginInOut)
def member_login(member:LoginIn):
    with Session(engine) as session:
        member_list=session.query(Member).all()
        for m in member_list:
            if m.username==member.username and m.password==member.password:
                return {"msg":"登录成功~","member":m}
    
    raise HTTPException(404,detail="登录失败")

#操作五
#删除操作
class DeleteMember(BaseModel):
    username:str=Field(...)
    
@app.post("/members/delete")
def delete_member(member:DeleteMember):
    with Session(engine) as session:
        s=session.query(Member).filter(Member.username==member.username).first()
        if s:
            session.delete(s)
            session.commit()
            return {"msg":"删除成功","username":s.username}
    raise HTTPException(404,detail="删除失败 未找到此用户")
    


    