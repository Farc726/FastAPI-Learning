import sqlite3

# 连接数据库 得到连接对象conn
conn=sqlite3.connect("school.db")
# 创建游标cur，用来执行sql
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    chinese INTEGER,
    math INTEGER,
    english INTEGER
)
            """)
# 1.增添数据
# cur.execute("""
# INSERT INTO students(name,chinese,math,english)
# VALUES('张三',99,88,77)
#             """)
# conn.commit()
# cur.execute("""
# INSERT INTO students(name,chinese,math,english)
# VALUES('李四',95,84,74)
#             """)
# conn.commit()
# cur.execute("""
# INSERT INTO students(name,chinese,math,english)
# VALUES('王五',94,98,67)
#             """)
# conn.commit()

# 2.查询数据
#2.1查询全部
# cur.execute("""
# SELECT * FROM students
#             """)

#2.2只查询某几列
# cur.execute("""
# SELECT name,chinese FROM students
#             """)
#2.3根据条件查询
# cur.execute("""
# SELECT name FROM students
# WHERE chinese>=95
#             """)
#2.4升降序查询(按语文成绩降序排)
# cur.execute("""
# SELECT * FROM students
# ORDER BY chinese DESC
#             """)

# 前面两个知识点结合
# cur.execute("""
# SELECT name,chinese + math + english AS total FROM students
# WHERE chinese>=95
# ORDER BY total DESC    
#         """)
#2.5只查询前n条
# cur.execute("""
# SELECT * FROM students
# LIMIT 2
# """)


# 3.给计算出来的列起名字
# cur.execute("""
# SELECT name, chinese + math + english AS total
# FROM students;
# """)

#4.修改 UPDATE
# cur.execute("""
# UPDATE students
# SET chinese=100
# WHERE name='张三'
#             """)
# conn.commit()

#5.删除 DELETE
# cur.execute("""
# DELETE FROM students
# WHERE name='王五'    
#         """)
## conn.commit()
# for row in cur.fetchall():
#     print(row)

# 6. 关于聚合函数
# COUNT(*)：统计一共有多少学生
res1=cur.execute("SELECT COUNT(*) FROM students;").fetchone()
print("学生总人数为：",res1)

# AVG：语文平均分
res2=cur.execute("SELECT AVG(chinese) FROM students;").fetchone()
print("语文平均分为：",res2)

# MAX：数学最高分
res3=cur.execute("SELECT MAX(math) FROM students;").fetchone()
print("数学最高分为：",res3)

# MIN：英语最低分
res4=cur.execute("SELECT MIN(english) FROM students;").fetchone()
print("英语最低分为：",res4)

# SUM：数学全部同学分数总和
res5 = cur.execute("SELECT SUM(math) FROM students;").fetchone()
print("数学总分总和", res5)

# 7.聚合函数+WHERE多条件版
# BETWEEN：数学分数在 80 ~ 90（包含两端）
r1 = cur.execute("""
SELECT name,math FROM students 
WHERE math BETWEEN 80 AND 90;
""").fetchall()
print("\n数学80~90：", r1)

# LIKE模糊查询：名字以"张"开头
r2 = cur.execute("SELECT name FROM students WHERE name LIKE '张%';").fetchall()
print("姓张的同学：", r2)

# AND 同时满足两个条件：语文>=85 并且 英语>=85
r3 = cur.execute("SELECT name FROM students WHERE chinese >=85 AND english >=85;").fetchall()
print("语文≥85且英语≥85：", r3)
# 关闭连接
conn.close()