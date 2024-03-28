# Fetchone.py

import pymysql

db = pymysql.connect("localhost","root",
					 "a123456","python",charset="utf8")

cur = db.cursor()

sql_select = "select * from t1;"
cur.execute(sql_select)

# fetchone 取得表中的第一條紀錄 
data = cur.fetchone()
print("fetchone 的結果為:",data)

db.commit()
cur.close()
db.close()