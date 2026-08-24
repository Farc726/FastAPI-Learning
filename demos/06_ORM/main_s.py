from fastapi import FastAPI,HTTPException
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import DeclarativeBase,Session
from pydantic import BaseModel,Field,ConfigDict
app=FastAPI()
engine=create_engine("sqlite:///main_s.db")
class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__="students"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String, nullable=False)                       # 文本，不能空
    chinese = Column(Integer)
    math = Column(Integer)
    english = Column(Integer)
    
class StudentOut(BaseModel):
    id:int
    name:str
    chinese:int
    math:int
    english:int
    model_config=ConfigDict(from_attributes=True)
    
Base.metadata.create_all(engine)

# session=Session(engine)
# 全局只创建1个session，所有http请求共用这同一个session对象
# close()之后 
#如果你之后继续调用session.query()等
# 自动！向 engine 重新申请一条新连接继续干活（可以跑 但不推荐）

# 所以 采用一个任务一个session的方法好些

# 接口一：查询全部：
@app.get("/students",response_model=list[StudentOut])
def get_students():
    with Session(engine) as session:
        student_list=session.query(Student).all()
        session.close()
        return student_list
    
        
# 接口二：新增
class StudentIn(BaseModel):
    name:str=Field(...)
    chinese:int
    math:int
    english:int

        
@app.post("/students/add",response_model=StudentOut)
def add_student(stu:StudentIn):
    
# yeah! 我写出来了！！！
    with Session(engine) as session:
        s=Student(**stu.model_dump())
        session.add(s)
        session.commit()
    #AUTOINCREMENT 的自增 id 是数据库生成的,不是 Python 生成的
    #commit 之后数据库里那行已经有 id 了，但内存里的对象还停留在"id 未赋值"的状态。
    #refresh 就是"重新从数据库读一遍这一行"，把id填回对象。
        session.refresh(s)
        session.close()
        return s

# 接口三：更新
class UpdateStudent(BaseModel):
    id:int
    name:str=Field(...)
    chinese:int
    math:int
    english:int
    
@app.post("/student/update",response_model=StudentOut)
def update_student(stu:UpdateStudent):
    with Session(engine) as session:
        s=session.query(Student).filter(Student.id==stu.id).first()
        if s:
            s.chinese=stu.chinese
            s.math=stu.math
            s.english=stu.english
            session.commit()
            session.refresh(s)
            return s
        else:
            raise HTTPException(404, detail="学生不存在")
        
# 接口四 ：删除
class DeleteStudent(BaseModel):
    id:int
    
@app.post("/student/delete")
def delete_student(stu:DeleteStudent):
    with Session(engine) as session:
        s=session.query(Student).filter(Student.id==stu.id).first()
        if s:
            session.delete(s)
            session.commit()
            return {"msg":"删除成功~"}
        else:
            raise HTTPException(404, detail="学生不存在")
    
    