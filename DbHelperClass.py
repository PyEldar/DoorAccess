import sqlite3

class DB:
	"""Helper class for communicating with DB"""

	def __init__(self, dbname):
		self.dbname = dbname
		self.status = "initialized"


	def connect(self):
		self.con = sqlite3.connect(self.dbname, check_same_thread=False)
		self.status = "connected"


	def createLog(self, UserID, Created, Access, LockID):
		"""Method for creating Record in DB with data passed as arguments"""
		log = [
			(UserID, Created, Access, LockID)
		]
		self.con.executemany("INSERT INTO LOGS(UserID, Created, Access, LockID) VALUES(?, ?, ?, ?)", log)
		self.con.commit()


	def retrieveTable(self, table):
		"""Returns list of tuples every tuple is a row in DB"""
		cur = self.con.cursor()
		cur.execute("SELECT * FROM " + table)
		rows = cur.fetchall()
		return rows

	def close(self):
		self.con.close()


	def __str__(self):
		return self.dbname, self.status

