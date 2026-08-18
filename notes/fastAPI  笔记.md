# FastAPI基础 
## 1.基础
## 运行项目
在终端中输入：
```
uvicorn 文件名：fastAPI实例名 --reload(更改代码后自动重启服务器)
```
## 访问FastAPI交互式文档
输入 http://127.0.0.1:8000/docs
## 2.路由
### 1.什么是路由
- 路由是[[HTTP基础#URL|URL]] 和 处理函数之间的映射关系，它决定了用户访问某个特定网址时，服务器应该执行哪段代码来返回结果
- FastAPI的路由定义基于python的装饰器模式
### 2.具体实现
```
# 使用@app.get装饰器创建一个处理（某路径）的路由
@app.get("某路径")

# 定义路由处理函数，返回...
async def read_root()：
	return{...}
```
## 2.参数
### 2.1 路径参数
- 位置：URL路径的一部分
- 作用：指向唯一的特定的资源
- 方法：GET
#### 2.1.1 路径参数--类型注解（Path）
导入Path
#### 2.1.2关于路由顺序
固定路径放在上面 参数路径放在下面
```
# 注意先后

@app.get("/user/password")
async def user_password():
    return {"password":"无权限不可随意查看"}
  
@app.get("/user/{id}")
async def get_user(id:int=Path(...,gt=0,le=100,description="请输入1~100之间的数字")):
    return {"id":id,"title":f"欢迎您第{id}号用户"}
```
**如果 @app.get("/user/{id}")放在了 @app.get("/user/password") 上面 由于FastAPI 处理请求严格按照从上到下的原则 一旦找到了匹配的路由，就直接执行 不再继续向下读 在这个例子中 成功匹配了/user/{id} 这条路由之后 再去访问/user/password的时候 会把password这个词以为是id的值 而上面又规定了id为int 所以会报422的错误**
==为什么反过来就好了呢？==
因为反过来
在访问/user/password 的时候第一个就与之匹配 执行完 完美结束
在访问/user/{id} 你会先键入一个整数如11 开始从上到下匹配 配到第一个路由/user/password 而 password不等于11，继续向下找 于是找到了正确的 /user/{id}

## 2.2 查询参数
声明的参数不是路径参数时，路径操作函数会把该参数自动解释为查询参数
- 位置：URL的？之后 k1=v1&k2=v2
- 作用：对资源集合进行过滤、排序、分页等操作
- 方法：GET
#### 2.2.1 查询参数--类型注解（Query）
导入Query （可以有默认值）

## 2.3 请求体参数

- 位置：HTTP请求的消息体中
- 作用：创建、更新资源 携带大量数据，eg：json
- 方法：POST PUT...
### 2.3.1 请求体参数--类型注解（Field）
从pydantic中导入Field（可以有默认值）
### 2.3.2 一些具体的理解 （v1-菜鸟版）
请求体参数所在的位置是body请求体 而 FastAPI 处理 body 请求体，**强制依赖 Pydantic 库**
`BaseModel`就是 Pydantic 提供的**基类**
`class Book(BaseModel):`这一步就是你自定义的类Book继承于BaseModel（它有的方法Book都有!）
发生了什么呢
 1. ==这个说法现在不太理解 后面再看看==  我们用 `@app.post("/library/new_book")` 定义好了这个 post 接口；运行服务之后，**外部向这个地址发送一段 JSON 请求体，后端收到这份数据**
2. FastAPI 处理 body 请求体 依赖 **Pydantic 库**
3. **Pydantic 库**又使用你自己定义的Book(BaseModel)这个模型把json中的数据解析成Book这个类的对象 （把其中的属性赋值）
4. 若有Field 要多加一步校验 不符号则422 
5. 校验通过 这个Book类就成功被实例化 为book 
6. `return book`：Pydantic 再把 Book 对象自动转换回 JSON，返回浏览器。