# TextMysql.py
from MysqlPython import MysqlPython

# update
name = input("please input modify student name:")
score = int(input("please input the student new score:"))

sql = "update t1 set score='%s' where name='%s';"% (score,name)

sqlH = MysqlPython("localhost","root","a123456",
				   "python")

sqlH.exe(sql)
d = sqlH.all("select * from t1;")
for i in d:
	print(i)