# 创建数据库引擎
# 使用create_async_engine创建异步引擎
from fastapi import FastAPI,Depends
app=FastAPI()
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker, AsyncSession
import sqlalchemy
import datetime
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import select

#SQLite 异步连接串写法：sqlit+aiosqlite（SQLite的异步驱动包）:数据库文件名
ASYNC_DATABASE_URL="sqlite+aiosqlite:///test1.db"

#1.创建异步引擎
async_engine=create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,# 输出SQL日志
    pool_size=10,#设置连接池中保持的持久连接数
    max_overflow=20 #设置连接池允许创建的额外连接数
    
)

#2.定义模型类（基类+表对应的模型类）
#2.1 基类：继承DeclarativeBase 创建时间+更新时间
class Base(DeclarativeBase):
    create_time:Mapped[datetime.datetime]=mapped_column(
        sqlalchemy.DateTime,
        insert_default=sqlalchemy.func.now(),
        default=sqlalchemy.func.now())
    
    update_time:Mapped[datetime.datetime]=mapped_column(
        sqlalchemy.DateTime,
        insert_default=sqlalchemy.func.now(),
        default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now())
#2.2 定义数据库对应的模型类--具体的东西（书籍表：id 书名 作者 价格 出版社）
# 对映射思想的理解
class Book(Base):
    __tablename__="book"
    id:Mapped[int]=mapped_column(primary_key=True)
    bookname:Mapped[str]=mapped_column()
    author:Mapped[str]=mapped_column()
    price:Mapped[float]=mapped_column()
    publisher:Mapped[str]=mapped_column()
    
#3.建表： 定义函数建表-> fastapi启动的时候调用建表的函数
async def create_tables():
    # 获取异步引擎，创建事务 建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) #Base 模型类的原数据创建

@app.on_event("startup")
async def startup_event():
    await create_tables()
    
@app.get("/")
async def root():
    return {"message":"welcome!"}

#需求：查询功能的接口，查询图书 依赖注入：创建依赖项获取数据库会话+Depends 注入路由处理函数
AsyncSessionLocal=async_sessionmaker(
    bind=async_engine,#绑定数据库引擎
    class_=AsyncSession,#指定会话类
    expire_on_commit=False#提交后会话不过期 不会重新查询数据库
)

# 依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

            
@app.get("/book/books")
async def get_book_list(db:AsyncSession=Depends(get_db)):
    #查询：
    result=await db.execute(sqlalchemy.select(Book))
    book=result.scalars().all()
    return book