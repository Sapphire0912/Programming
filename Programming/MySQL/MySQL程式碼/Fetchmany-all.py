# Fetchmany-all.py

import pymysql

db = pymysql.connect("localhost","root",
					 "a123456","python",port=3306,charset="utf8")

# pymysql.connect(keyword argument)
#(Host,User,password[,purpose database][,port],charset)

cur = db.cursor()

sql_select = "select * from t1;"
cur.execute(sql_select)
print("select 語句查出的紀錄個數為:",cur.rowcount)

# fetchmany(n) 取得結果集到第 n 條紀錄
data = cur.fetchmany(2)
print("fetchmany 的結果為:")
for i in data:
	print(i)

data_all = cur.fetchall()
print("\nfetchall 的結果為:")
for i in data_all:
	print(i)

db.commit()
cur.close()
db.close()