#8.20 重写的时候 一个很大的问题是 return的是哪一个对象 一定要注意 一般不是请求体中的对象 你先看逻辑再看可否过滤
from fastapi import FastAPI,HTTPException,Path
from pydantic import BaseModel,Field,EmailStr,ConfigDict

app=FastAPI()

class MemberBase(BaseModel):
    username:str=Field(...,min_length=3,max_length=20)
    email:EmailStr
    full_name:str|None=None
    
class MemberCreate(MemberBase):
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
@app.post("/members",response_model=MemberOut)
async def create_member(member:MemberCreate):
# 声明全局对象next_id
    global next_id
#将MemberCreate对象转为字典(这里其实不用转字典 直接按类访问就可以--类似于后面登录校验时)
    new_member_dict=member.model_dump()
    for old_member in Member_List:
        if old_member.username==new_member_dict["username"]:
            raise HTTPException(400,detail="用户名已存在~")
#构造Member 对象存进列表
    new_member=Member(id=next_id,username=new_member_dict["username"],email=new_member_dict["email"],full_name=new_member_dict["full_name"],password=new_member_dict["password"])
    Member_List.append(new_member)
    next_id += 1  
# 构建MemberOut类的对象 因为其中有model_config = ConfigDict(from_attributes=True)
# 直接传入类可以自动过滤
# 这个为什么不能直接在post中限定直接输出过滤后的new_member呢？
# 完全可以！！！
    return new_member


# 查询单个
@app.get("/members/{member_id}",response_model=MemberOut)
async def get_member(member_id:int=Path(...,ge=1,le=1000)):
    for member in Member_List:
        if member.id==member_id:
            return member
    raise HTTPException(404,detail="会员不存在~")

# 会员列表
@app.get("/members",response_model=list[MemberOut])
async def get_all_members():
    return Member_List
# 继承BaseModel的类哪怕在列表内也可以自动转化后输出？？
# 解答：
# 1.如果列表里存的是 Pydantic 模型实例（比如 MemberOut 对象）——不写 response_model 也能自动序列化输出。
# 2.如果列表里存的是自定义类对象（Member_List 就是这种情况）——只要声明响应模型，FastAPI 会逐个元素做转换
# 所以 上面代码还可以优化！

# 登录
# 再修改 --涉及自定义响应类型知识点
# 定义登录响应的输出模型
class LoginOut(BaseModel):
    msg:str
    member:MemberOut

@app.post("/members/login",response_model=LoginOut)
async def login(login:LoginIn):
    for member in Member_List:
        if login.username==member.username and login.password==member.password:
            return {"msg":"登录成功","member":member}
    raise HTTPException(401,detail="用户名或密码错误~")

    
            
    

        
    
