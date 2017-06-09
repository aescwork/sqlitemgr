
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm

class CreateTableTest(unittest.TestCase):

	"""
	The way the create_table function is being tested is to have the SQLiteMgr object compose and execute an SQL statement to create a table in fruit.db,
	then get the cursor from the object, execute a SELECT statement against the table, then get the name of the columns in the table (in a list),
	and compare with what should be the same list assigned to self.comp_names.  If they match, the object successfully created the nut table in fruit.db.
	"""

	def setUp(self):
		self.sm = sqm.SQLiteMgr("../fixtures/fruit.db")
		self.sm.new_table("nuts").add_table_column("Nmbr", "INT", "PRIMARY KEY").add_table_column("Called", "TEXT", "UNIQUE").add_table_column("Description", "TEXT").create_table()
		self.cursor = self.sm.get_cursor()
		self.cursor.execute("SELECT * FROM nuts")
		self.col_names = [description[0] for description in self.cursor.description]     # gets the column names from nuts table because self.sm.get_cursor().execute() is selecting from nuts table
		self.comp_names = ['Nmbr', 'Called', 'Description']


	def test_create_table(self):

		self.assertEqual(self.col_names, self.comp_names)	


	def test_result(self):

		self.assertEqual(self.sm.result, "OK")


	def tearDown(self):

		self.sm.__del__()


if __name__ == '__main__':
	unittest.main()


