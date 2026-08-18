from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# 请求体参数：位于 HTTP 请求的消息体中（POST/PUT），携带大量数据（如 JSON）
# FastAPI 依赖 Pydantic：定义 BaseModel 子类，自动完成 解析 -> 校验 -> 转回 JSON

# 需求：设计接口新增图书，图书信息包含：书名、作者、出版社、售价
# - 书名：不能为空；长度 2 ~ 20
# - 作者：长度 2 ~ 10
# - 出版社：默认值 "黑马出版社"
# - 售价：不能为空；价格大于 0
class Book(BaseModel):
    name: str = Field(..., min_length=2, max_length=20, description="书名应在2~20个字符之间~")
    author: str = Field(..., min_length=2, max_length=10, description="作者名应在2~10个字符之间~")
    publisher: str = Field(default="黑马出版社")
    price: int = Field(..., gt=0)

@app.post("/library/new_book")
async def new_book(book: Book):
    return book