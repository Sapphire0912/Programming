# MysqlPython.py
from pymysql import *

class MysqlPython:
	def __init__(self,host,user,password,db,
				 port=3306,charset='utf8'):
		self.host = host
		self.user = user
		self.password = password
		self.db = db
		self.port = port
		self.charset = charset

	def open(self):
		self.con = connect(host=self.host,user=self.user,
						   password=self.password,db=self.db,
						   port=self.port,charset=self.charset)

		self.cursor = self.con.cursor()

	def close(self):
		self.cursor.close()
		self.con.close()

	def exe(self,sql):
		self.open()
		self.cursor.execute(sql)
		self.con.commit()
		self.close()

	def all(self,sql):
		try:
			self.open()
			self.cursor.execute(sql)
			data = self.cursor.fetchall()
			return data
		except Exception as e:
			print(e)
		finally:
			self.close()


