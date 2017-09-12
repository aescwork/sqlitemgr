
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm

def prep_key_val():

	db_path = "../fixtures/key_val.db"

	open(db_path, "w").close()	# empty out the key_val.db

	### setup the table ###
	sm = sqm.SQLiteMgr(db_path)
	sm.create_db(db_path)
	sm.new_table("fruit_keys_and_values").add_table_column("fruit_key", "TEXT").add_table_column("fruit_val", "INT").create_table()
		
	sm.close_db()
	cursor = sm.get_cursor()

	### add some rows to the table ###
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('apple', 1)")
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('orange', 2)")
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('pear', 3)")
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('strawberry', 4)")
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('raspberry', 5)")
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('grape', 6)")
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('kiwi', 7)")
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('grapefruit', 8)")
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('pineapple', 9)")
	cursor.execute("INSERT INTO fruit_keys_and_values VALUES('cranberry', 10)")

	### delete some rows ###

	cursor.execute("DELETE FROM fruit_keys_and_values WHERE fruit_val = 2")
	cursor.execute("DELETE FROM fruit_keys_and_values WHERE fruit_val = 3")
	cursor.execute("DELETE FROM fruit_keys_and_values WHERE fruit_val = 6")
	cursor.execute("DELETE FROM fruit_keys_and_values WHERE fruit_val = 10")

	sm.conn.commit()


class ConsecutiveReindexTest(unittest.TestCase):
	"""
	consecutive_reindex()
	This method takes numbers in a numbered column of each row in a sqlite table and re-numbers them so that they are consecutive one after the other.
	This is primarily used for when some rows have been deleted.  For example, say there are 10 rows in a table, each with a consecutive number_column
	and whose values are 1,2,3,4,5,6,7,8,9,10.  Now rows 2, 5, 7, 8, 9 are deleted.  The remaining  5 rows -- 1, 3, 4, 6 and 10 -- are re-numbered so they
	have number_columns 1, 2, 3, 4, 5.
	
	Optionally returned is a dictionary for reference and comparison for use by the code which called the method.
	"""

	def setUp(self):

		prep_key_val()											# this function in prep_db.py handles the setup and INSERTing of values 
																# into the key_val.db separately.

		self.comp_dict = {1: 1, 4: 2, 5: 3, 7: 4, 8: 5, 9: 6}	# After all the deletions to and re-indexing of the database table, this
																# dictionary should be returned by consecutive_reindex

		self.reindexed_comp = [(u'apple', 1), (u'strawberry', 2), (u'raspberry', 3), (u'kiwi', 4), (u'grapefruit', 5), (u'pineapple', 6)]

		self.sm = sqm.SQLiteMgr("../fixtures/key_val.db")  
		self.sm.table = "fruit_keys_and_values"
		self.result = self.sm.consecutive_reindex("fruit_val")


		self.sm.cursor.execute("SELECT * FROM fruit_keys_and_values")
		self.reindexed = self.sm.cursor.fetchall()

	def test_consecutive_reindex(self):
		self.assertEqual(self.comp_dict, self.result)
		self.assertEqual(self.reindexed, self.reindexed_comp)


	def tearDown(self):

		self.sm.__del__()


		
if __name__ == '__main__':
	unittest.main()
