#1.导入方法
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import Session,DeclarativeBase
#2. 创建引擎（建立程序与数据库之间的连接）
engine=create_engine("sqlite:///school_orm.db")
# ORM方法核心
# 3.基类：创建继承于。。。的基类 这样后续的具体模型类才会被翻译为SQL语句
class Base(DeclarativeBase):
    pass
# 4.模型类：创建基于基类的模型类
class Student(Base):
    __tablename__="students"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String, nullable=False)                       # 文本，不能空
    chinese = Column(Integer)
    math = Column(Integer)
    english = Column(Integer)
    
# 5.建表：先在数据库中建表
Base.metadata.create_all(engine)
##6.方法实施：要进行各种方法地实施了
# 首先打开有着各种方法的窗口
session=Session(engine)
# 进行各种方法实施


# #1.添加操作
# s1 = Student(name="张三", chinese=90, math=85, english=88)
# s2 = Student(name="李四", chinese=75, math=95, english=80)
# session.add(s1)
# session.add(s2)
# # 对于某些方法 要提交
# session.commit()



#2.查询操作
# #2.1全部查询
students_list=session.query(Student).all()
for s in students_list:
    print(s.id,s.name,s.chinese,s.math,s.english)
# #2.2条件查询
# # filter写过滤条件，Student.id 是类的字段；first()拿到第一条结果，返回实例对象
# stu=session.query(Student).filter(Student.id==1).first()
# if stu:
#     print("查到：", stu.name, stu.math)


# #3.更新操作
# # 通过查询操作 拿到要改的实例对象--- 直接通过返回的实例修改对象属性---提交
# stu=session.query(Student).filter(Student.id==1).first()
# if stu:
#     stu.math=99
#     stu.english=100
#     session.commit()
# print("更改后：", stu.id,stu.name,stu.chinese,stu.math, stu.english)

#4.删除操作
#查询要删除的实例--- 执行删除操作---提交
#4.1 单个删除
# stu=session.query(Student).filter(Student.id==6).first()
# if stu:
#     session.delete(stu)
#     session.commit()

# s_list=session.query(Student).all()
# for s in s_list:
#     print(s.id,s.name,s.chinese,s.math,s.english)
#4.2 批量删除
# delete_list=session.query(Student).filter(Student.id>2).all()
# for s in delete_list:
#     session.delete(s)
    
# session.commit()
# for s in delete_list:
#     print(s.id,s.name,s.chinese,s.math,s.english)
# 关闭窗口
session.close()