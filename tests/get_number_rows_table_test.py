
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm

class CountNumberRowsInTableTest(unittest.TestCase):
	"""
	"""

	def setUp(self):
		self.table_name = "fruit"
		self.db_name = "../fixtures/fruit.db"
		open(self.db_name, "w").close()			# remove everything from the fruit.db file

		self.sm = sqm.SQLiteMgr(self.db_name)
		self.sm.new_table(self.table_name).set_table_statement('CREATE TABLE IF NOT EXISTS fruit(Id INT PRIMARY KEY, Name TEXT UNIQUE, Qualities TEXT)').create_table()
		self.cursor = self.sm.get_cursor()
		self.cursor.execute("INSERT INTO fruit VALUES(1,'cherry','tart, sweet, red, harvest from branch')")
		self.cursor.execute("INSERT INTO fruit VALUES(2,'strawberry','sweet, red, harvest from plant')")
		self.cursor.execute("INSERT INTO fruit VALUES(3,'orange','sweet, orange, harvest from branch')")
		self.cursor.execute("INSERT INTO fruit VALUES(4,'grape','sweet, red, harvest from vine')")
		self.table_count = self.sm.get_number_rows_in_table(self.table_name)


	def test_get_number_rows_in_table(self):
		self.assertEqual(self.table_count, 4)


	def test_result(self):
		self.assertEqual(self.sm.result, "OK")
		self.assertEqual(self.sm.status, "In SQLiteMgr get_number_rows_in_table: accessed db: " + self.db_name + " table: " + self.table_name)

	def tearDown(self):

		self.sm.__del__()

		
if __name__ == '__main__':
	unittest.main()
