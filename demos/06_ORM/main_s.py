from fastapi import FastAPI
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
    name:str
    chinese:int
    math:int
    english:int
    model_config=ConfigDict(from_attributes=True)
    
Base.metadata.create_all(engine)

session=Session(engine)

# 接口一：查询全部：
@app.get("/students",response_model=list[StudentOut])
async def get_students():
    student_list=session.query(Student).all()
    return student_list
    
        
# 接口二：新增
class AddStudent(BaseModel):
    name:str=Field(...)
    chinese:int
    math:int
    english:int

        
@app.post("/students/add",response_model=StudentOut)
async def add_student(stu:AddStudent):
    s=Student(**stu.model_dump())
    session.add(s)
    session.commit()
    return s