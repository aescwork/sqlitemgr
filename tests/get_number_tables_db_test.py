
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm

class GetNumberTablesTest(unittest.TestCase):
	"""
	"""

	def setUp(self):
		self.db_name = "../fixtures/fruit.db"
		open(self.db_name, "w").close()			# remove everything from the fruit.db file

		self.comp_assert = 4
		self.sm = sqm.SQLiteMgr(self.db_name)
		self.sm.new_table("fruit").set_table_statement('CREATE TABLE IF NOT EXISTS fruit (Id INT, Name TEXT, Qualities TEXT)').create_table()
		self.sm.new_table("nuts").set_table_statement('CREATE TABLE IF NOT EXISTS nuts(Id INT PRIMARY KEY, Name TEXT UNIQUE, Qualities TEXT)').create_table()
		self.sm.new_table("flowers").set_table_statement('CREATE TABLE IF NOT EXISTS flowers(Id INT PRIMARY KEY, Name TEXT UNIQUE, Qualities TEXT)').create_table()
		self.sm.new_table("seeds").set_table_statement('CREATE TABLE IF NOT EXISTS seeds(Id INT PRIMARY KEY, Name TEXT UNIQUE, Qualities TEXT)').create_table()
		self.tables_count = self.sm.get_number_tables_db()


	def test_get_number_tables_db(self):
		self.assertEqual(self.tables_count, self.comp_assert)


	def test_result(self):
		self.assertEqual(self.sm.result, "OK")


	def tearDown(self):

		self.sm.__del__()


		
if __name__ == '__main__':
	unittest.main()


