from fastapi import FastAPI

app = FastAPI()

# 本文件是仓库入口（门面），保持最简
# 知识点练习都在 demos/ 目录，每个文件独立可运行：
#   cd demos
#   uvicorn demo_path_params:app --reload

@app.get("/")
async def root():
    return {"message": "Hello World", "tip": "打开 /docs 查看接口文档"}