from fastapi import FastAPI,HTTPException,Path
from pydantic import BaseModel,Field,EmailStr,ConfigDict

app=FastAPI()

class MemberBase(BaseModel):
    username:str=Field(...,min_length=3,max_length=20)
    email:EmailStr
    full_name:str|None=None
    
class MenberCreate(MemberBase):
    password:str=Field(...,min_length=6,max_length=20)
    
class MemberOut(MemberBase):
    id:int
    model_config = ConfigDict(from_attributes=True)
# 类MemberOut实例化的时候可以直接以普通类为参数
    
class LoginIn(BaseModel):
    username:str=Field(...,min_length=3,max_length=20)
    password:str=Field(...,min_length=6,max_length=20)
    
class Member():
    def __init__(self,id,username,email,full_name,password):
        self.id=id
        self.username=username
        self.email=email
        self.full_name=full_name
        self.password=password
        
Member_List=[]
next_id=1

#注册
@app.post("/members")
async def create_member(member:MenberCreate):
# 声明全局对象next_id
    global next_id
#将MemberCreate对象转为字典
    new_member_dict=member.model_dump()
    for old_member in Member_List:
        if old_member.username==new_member_dict["username"]:
            raise HTTPException(400,detail="用户名已存在~")
#构造Member 对象存进列表
    new_member=Member(id=next_id,username=new_member_dict["username"],email=new_member_dict["email"],full_name=new_member_dict["full_name"],password=new_member_dict["password"])
    Member_List.append(new_member)
# 构建MemberOut类的对象 因为其中有model_config = ConfigDict(from_attributes=True)
# 直接传入类可以自动过滤
# 这个为什么不能直接在post中限定直接输出过滤后的new_member呢？
    memberout=MemberOut.model_validate(new_member)
    next_id+=1
    return memberout


# 查询单个
@app.get("/members/{member_id}",response_model=MemberOut)
async def get_member(member_id:int=Path(...,ge=1,le=1000)):
    for member in Member_List:
        if member.id==member_id:
            return member
    raise HTTPException(404,detail="会员不存在~")

# 会员列表
@app.get("/members")
async def get_all_members():
    result=[]
    for member in Member_List:
        memberout=MemberOut.model_validate(member)
        result.append(memberout)
    return result
# 继承BaseModel的类哪怕在列表内也可以自动转化后输出？？

# 登录
@app.post("/members/login")
async def login(login:LoginIn):
    for member in Member_List:
        if login.username==member.username and login.password==member.password:
            memberout=MemberOut.model_validate(member)
            return {"msg":"登录成功","member":memberout}
    raise HTTPException(401,detail="用户名或密码错误~")

    
            
    

        
    
