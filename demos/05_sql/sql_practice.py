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
cur.execute("""
SELECT * FROM students
            """)

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
# WHERE name=='张三'
#             """)
# conn.commit()

#5.删除 DELETE
# cur.execute("""
# DELETE FROM students
# WHERE name=='王五'    
#         """)
# conn.commit()
for row in cur.fetchall():
    print(row)


# 关闭连接
conn.close()