# FirstPymysql.py
import pymysql

# 打開數據庫連接(connect)
db = pymysql.connect("localhost",
					 "root",
					 "a123456",
					 charset="utf8")
#    module.method("Host","User","Password",default character)
# 此時的charset=utf8 是指python內部執行器的默認字符集

# 創建一個游標(cursor)對象 
cur = db.cursor()

# 創建庫python  # exists 代表 存在
cur.execute("create database if not exists python;")
# 切換庫
cur.execute("use python;")
# 創建表t1 \為隱式換行
cur.execute("create table if not exists t1(\
			id int primary key,\
			name varchar(20),\
			score tinyint unsigned)default charset=utf8;")
# 在t1表中插入5條紀錄
cur.execute("insert into t1 values\
			(1,'Eric',80),(2,'Iris',90),\
			(3,'Aurora',94),(4,'Lily',75),\
			(5,'yuki',99);")

# 提交到數據庫
db.commit()
# 關閉游標
cur.close()
# 關閉數據庫連接
db.close()