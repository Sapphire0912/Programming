# rollback.py
import pymysql as py

db = py.connect("localhost","root","a123456",
				"db3",port=3306,charset="utf8")

cur = db.cursor()
try:
	cur.execute("update CCB set money=95000 where name='轉錢';")
	cur.execute("update ICBC set money=7000 where name='借錢';")
	db.commit()
	print("ok")
except Exception as e:
	print(e)
	db.rollback()
finally:
	cur.close()
	db.close()