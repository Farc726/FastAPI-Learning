# 文件上传
#基础：引入File
#
from fastapi import FastAPI,File,UploadFile,Form
app=FastAPI()

#1.小文件------使用File 
# 注意 文件路径的写法！！！ 详情见笔记！！
# 这里你会产生的一个小疑问 -- 关于.png和.jpg
# 底层真相：wb只负责把字节一股脑写进磁盘，它根本不懂图片格式，不会校验、不会转换格式。（上传于后缀不匹配有可能显示不出）
@app.post("/files")
# 二次重写时写成了file: File错了------ File是一个声明函数 并非类型注解
# 类型是 bytes，File() 是默认值 --告诉FastAPI 这个参数来自 multipart/form‑data 请求体的文件表单，而不是 URL 查询参数
# 这又可以补充参数类型的判断方式 具体见笔记
async def upload_1(file:bytes=File(...)):
    with open("../file/01.png","wb") as f:
        f.write(file)

# file 是文件的原始字节数据
    return {"file_size":len(file)}



# 2. 较大文件---使用UploadFile
@app.post("/uploadfile1")
async def create_uploadfile1(file:UploadFile):
# 图片是二进制文件“wb”打开
# 可以用f{本身文件名}也可以自定义文件名
    with open(f"../file/{file.filename}","wb") as f:
#write（）只能接受字节 不可以直接扔UploadFile类型的file进去
        f.write(await file.read())
        

    return{
        "filename":file.filename,
        "content_type":file.content_type,
        "size":file.size
    }
    
# 可选文件上传
# 利用默认值None使文件的上传变为可选
@app.post("/uploadfile2")
async def create_uploadfile2(file:UploadFile|None=None):
    if not file:
        return {"msg":"没有上传文件~"}
    with open("../file/03.png","wb") as f:
        f.write(await file.read())
    return{
        "filename":file.filename,
        "content_type":file.content_type,
        "size":file.size
    }
    
# 多文件上传
# 使用列表接收多个文件
@app.post("/uploadfiles")
async def create_uploadfiles(file_list:list[UploadFile]=File(...)):
    for file in file_list:
        with open(f"../file/{file.filename}","wb") as f:
            f.write(await file.read())
    
    return {"filenames":[file.filename for file in file_list ]}

# 表单与文件混合上传
# 假如表单必填 文件选填
# 利用result来返回信息 用description来说明有无文件
@app.post("/items")
async def create_items(
    name:str=Form(...),
    description:str|None=Form(...),
    file:UploadFile|None=None
):
    result={"name":name,"description":description}
    if not file:
        return result
    with open(f"../file/{file.filename}","wb") as f:
        f.write(await file.read())
    result["filename"]=file.filename
    return result



      

    

    
