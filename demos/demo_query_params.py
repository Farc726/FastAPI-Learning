from fastapi import FastAPI, Query

app = FastAPI()

# 查询参数：位于 URL 的 ? 之后（k1=v1&k2=v2）
# 判断条件：参数名不在路径 {} 中，且是普通类型（int/str/float/bool）
# 查询参数可以有默认值（写在 Query 第一个参数位置）

# 需求：设计接口查询图书，携带两个查询参数：图书分类和价格
# - 图书分类：默认值 "Python开发"，长度限制 5 ~ 255
# - 价格：限制大小范围 50 ~ 100
@app.get("/library/book")
async def get_book(
    category: str = Query("Python开发", min_length=5, max_length=255),
    price: float = Query(ge=50, le=100),
):
    return {"category": category, "price": price}