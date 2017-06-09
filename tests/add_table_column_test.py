
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm

class AddTableColumnTest(unittest.TestCase):

	def setUp(self):
		self.sm = sqm.SQLiteMgr()  
		self.sm.new_table("nuts")
		self.final_statement = 'CREATE TABLE IF NOT EXISTS nuts(Nmbr INT PRIMARY KEY, Called TEXT UNIQUE, Description TEXT, '
		self.sm.add_table_column("Nmbr", "INT", "PRIMARY KEY").add_table_column("Called", "TEXT", "UNIQUE").add_table_column("Description", "TEXT")


	def test_add_table_column(self):

		self.assertEqual(self.sm.table_statement, self.final_statement)	


	def tearDown(self):

		self.sm.__del__()


if __name__ == '__main__':
	unittest.main()
