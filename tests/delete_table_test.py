
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm

class DeleteTableTest(unittest.TestCase):
	"""
	Test if delete_table was successful by checking if the name of the target table is in the 
	list returned by executing "SELECT name FROM sqlite_master WHERE type='table'" against the database.
	Then call fetchall on the cursor object, and if "nuts" does not appear in the returned list,
	the deletion of the table was successful.

	The database will only have one table: nuts
	"""

	def setUp(self):
		self.sm = sqm.SQLiteMgr("../fixtures/fruit.db")  
		self.sm.set_table_statement("CREATE TABLE IF NOT EXISTS nuts(Nmbr INT PRIMARY KEY, Called TEXT UNIQUE, Description TEXT)").create_table()
		self.sm.table_name = "nuts"
		self.table_exists= self.check_sqlite_master()		# should return True
		self.sm.delete_table()
		self.table_exists_after_delete= self.check_sqlite_master()		# should return False 

	def test_table_exists(self):
		self.assertEqual(self.table_exists, True)

	def test_delete_table(self):
		self.assertEqual(self.table_exists_after_delete, False)	

	def test_result(self):
		self.assertEqual(self.sm.result, "OK")
		self.assertEqual(self.sm.status, "In SQLiteMgr delete_table, deleted table nuts")

	def tearDown(self):

		self.sm.__del__()


	def check_sqlite_master(self):
		
		# the statement after return evaluates to either True or False
		return "nuts" in [item[0] for item in self.sm.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]

		
if __name__ == '__main__':
	unittest.main()
