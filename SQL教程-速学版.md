# SQL 速学教程（0 基础版 · 已实测）

> ✅ 本教程每一段代码都用 Python 实际运行验证过，放心照抄。
> 学习方法：每节 = 读概念 → 抄代码 → 运行 → 做挑战。
> 全程零安装：用 Python 自带的 sqlite3，不需要 MySQL。

---

## 第 0 节：动手前必须懂的 3 个概念（5 分钟）

**概念 1：数据库是什么**
- `school.db` 是一个文件，里面可以装很多张"表"
- 表像 Excel 表格：**列**=字段（name、chinese...），**行**=一条记录（一个学生）
- SQL 就是"指挥这个表格本"的语言

**概念 2：Python 操作数据库的固定三步**
1. 连接：`conn = sqlite3.connect("school.db")`
2. 执行：`cur.execute("...SQL...")`
3. 关闭：`conn.close()`

**概念 3：SQL 必须"住进引号里"（最重要！）**
- Python 文件里不能直接写英文句子，SQL 必须变成字符串再交给 `cur.execute()`
- ❌ 错误：在代码里直接裸写 `CREATE TABLE ...` → Python 报语法错误（你上次就卡在这）
- ✅ 正确：`cur.execute("""CREATE TABLE ...""")`
- 多行 SQL 用**三引号** `"""..."""`，Python 把三引号里的内容当成一整段文字
- 口诀：**SQL 住进引号，execute 负责执行**

## 第 1 节：第一个完整脚本（跑通就算成功）

新建 `demos/05_sql/sql_practice.py`，把下面代码完整复制进去：

```python
import sqlite3

# 第 1 步：连接数据库（school.db 不存在会自动创建）
conn = sqlite3.connect("school.db")

# 第 2 步：拿执行手柄
cur = conn.cursor()

# 第 3 步：执行 SQL —— 建一张学生表
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    chinese INTEGER,
    math INTEGER,
    english INTEGER
);
""")

# 第 4 步：建表属于结构变动，提交一下
conn.commit()

# 第 5 步：查询所有数据（现在表是空的）
cur.execute("SELECT * FROM students;")
for row in cur.fetchall():
    print(row)

# 第 6 步：关闭
conn.close()
```

运行（终端里，先激活 venv）：`python sql_practice.py`

**成功标志**：不报错、没有输出（或输出空）→ 表建好了。
几个词先混个脸熟：`TEXT`=文本、`INTEGER`=整数、`NOT NULL`=不能为空、`PRIMARY KEY AUTOINCREMENT`=id 自动从 1 递增，不用你写。

> 小知识：school.db 会生成在你运行命令的那个文件夹里（和 cwd 有关，不是 py 文件位置——你在 FastAPI 仓库里已经学过这个了）。

## 第 2 节：往表里放数据（INSERT）

把 sql_practice.py 的内容替换成：

```python
import sqlite3

conn = sqlite3.connect("school.db")
cur = conn.cursor()

# 插入一个学生（文本用单引号）
cur.execute("""
INSERT INTO students (name, chinese, math, english)
VALUES ('张三', 90, 85, 88);
""")

conn.commit()   # 增删改后要提交

# 查出来看看
cur.execute("SELECT * FROM students;")
for row in cur.fetchall():
    print(row)

conn.close()
```

**成功标志**：输出 `(1, '张三', 90, 85, 88)`，id 自动是 1。

**挑战**：把另外 4 个学生也插进去。在"查询"那行上面加 4 句：

```python
cur.execute("INSERT INTO students (name, chinese, math, english) VALUES ('李四', 75, 95, 80);")
cur.execute("INSERT INTO students (name, chinese, math, english) VALUES ('王五', 92, 70, 60);")
cur.execute("INSERT INTO students (name, chinese, math, english) VALUES ('赵六', 88, 90, 95);")
cur.execute("INSERT INTO students (name, chinese, math, english) VALUES ('孙七', 60, 65, 70);")
conn.commit()
```

再全查，应该看到 5 行，id 是 1~5。

## 第 3 节：查询（SELECT）——选你想看的列

```python
import sqlite3

conn = sqlite3.connect("school.db")
cur = conn.cursor()

# 查所有列
cur.execute("SELECT * FROM students;")
for row in cur.fetchall():
    print(row)

# 只查姓名和语文
cur.execute("SELECT name, chinese FROM students;")
for row in cur.fetchall():
    print(row)

# 查姓名和总分（AS 是给结果列起个名字）
cur.execute("""
SELECT name, chinese + math + english AS total
FROM students;
""")
for row in cur.fetchall():
    print(row)

conn.close()
```

**挑战**：只查所有学生的姓名和英语成绩。

## 第 4 节：条件查询 WHERE（重点）

```python
import sqlite3

conn = sqlite3.connect("school.db")
cur = conn.cursor()

# 语文 >= 90
cur.execute("SELECT name FROM students WHERE chinese >= 90;")
print("语文>=90：", cur.fetchall())

# 数学在 80~90 之间
cur.execute("SELECT name, math FROM students WHERE math BETWEEN 80 AND 90;")
print("数学80-90：", cur.fetchall())

# 姓张的（% 是通配符，表示任意字符）
cur.execute("SELECT name FROM students WHERE name LIKE '张%';")
print("姓张：", cur.fetchall())

# 两个条件同时满足（AND）
cur.execute("SELECT name FROM students WHERE chinese >= 90 AND math >= 80;")
print("语文>=90且数学>=80：", cur.fetchall())

conn.close()
```

**挑战**：查英语 < 80 的学生；查语文 ≥ 85 且英语 ≥ 85 的学生。

## 第 5 节：排序 ORDER BY（重点）

```python
import sqlite3

conn = sqlite3.connect("school.db")
cur = conn.cursor()

# 按总分从高到低（DESC=降序）
cur.execute("""
SELECT name, chinese + math + english AS total
FROM students
ORDER BY total DESC;
""")
for row in cur.fetchall():
    print(row)

conn.close()
```

**挑战**：按语文成绩从低到高排序（升序，写 `ASC` 或不写都行，默认就是升序）。

## 第 6 节：聚合函数（统计，重点）

```python
import sqlite3

conn = sqlite3.connect("school.db")
cur = conn.cursor()

print("人数：", cur.execute("SELECT COUNT(*) FROM students;").fetchone())
print("语文平均分：", cur.execute("SELECT AVG(chinese) FROM students;").fetchone())
print("数学最高分：", cur.execute("SELECT MAX(math) FROM students;").fetchone())
print("英语最低分：", cur.execute("SELECT MIN(english) FROM students;").fetchone())

conn.close()
```

**挑战**：算英语平均分（AVG）和数学总分（SUM）。

## 第 7 节：LIMIT 截取（了解即可）

```python
import sqlite3

conn = sqlite3.connect("school.db")
cur = conn.cursor()

# 只取前 2 条
cur.execute("SELECT * FROM students LIMIT 2;")
for row in cur.fetchall():
    print(row)

conn.close()
```

（GROUP BY 分组统计这周先不用学，用到再查。）

## 第 8 节：改和删（UPDATE / DELETE）——最危险的一节

```python
import sqlite3

conn = sqlite3.connect("school.db")
cur = conn.cursor()

# 修改：把孙七的语文改成 95（必须带 WHERE！）
cur.execute("""
UPDATE students SET chinese = 95 WHERE name = '孙七';
""")

# 删除：删掉赵六（必须带 WHERE！）
cur.execute("""
DELETE FROM students WHERE name = '赵六';
""")

conn.commit()

# 查出来确认
cur.execute("SELECT * FROM students;")
for row in cur.fetchall():
    print(row)

conn.close()
```

⚠️ **最重要的警告**：UPDATE 和 DELETE **忘写 WHERE = 全表遭殃**。规矩：先 `SELECT ... WHERE ...` 确认目标，再改/删。

**挑战**：把张三的数学改成 99；删除孙七；全查确认。

## 第 9 节：最终验收

现在**不看教程**，写出并运行这句查询：

> 查语文 ≥ 90 的学生的姓名和总分，按总分从高到低排序

写完后对照参考答案：

```python
cur.execute("""
SELECT name, chinese + math + english AS total
FROM students
WHERE chinese >= 90
ORDER BY total DESC;
""")
for row in cur.fetchall():
    print(row)
```

**预期结果**：如果你按教程做了第 8 节（孙七语文 95、删了赵六），输出是张三、孙七、王五（按总分排）。如果你没做第 8 节，是张三、王五。**以你自己的表为准，关键看 SQL 对不对。**

## 附加题（有余力再做）

1. 统计班级总人数
2. 三科各自的平均分
3. 数学最高分的学生姓名（提示：`ORDER BY math DESC LIMIT 1`）

---

## 结尾小抄（常回来翻）

- SQL 住进三引号，`cur.execute()` 执行，增删改后 `conn.commit()`
- 文本用单引号：`'张三'`
- SELECT 查 / INSERT 增 / UPDATE 改 / DELETE 删
- WHERE = 条件，ORDER BY = 排序（DESC 降序），LIMIT = 截取前 N 条
- UPDATE / DELETE 永远先 WHERE 确认