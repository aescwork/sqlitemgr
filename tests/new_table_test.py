
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm

class NewTableTest(unittest.TestCase):

	def setUp(self):
		self.comp_statement = 'CREATE TABLE IF NOT EXISTS nuts('
		self.sm = sqm.SQLiteMgr()  
		self.sm.new_table("nuts")
	def test_new_table_statement(self):

		self.assertEqual(self.sm.table_statement, self.comp_statement)


	def tearDown(self):

		self.sm.__del__()


if __name__ == '__main__':
	unittest.main()
