
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm

class DeleteDbTest(unittest.TestCase):
	"""
	Tests the delete_db method of the SQLiteMgr object.  The object is instantiated with a false path (path_to_none) to test the
	functionality of the delete_db method; that is, delete_db should be able to delete a database (on the fly) other than the one whose name has been
	assigned to the self.db object member.
	"""

	def setUp(self):
		self.path_to_db = "../fixtures/fruit.db"
		self.path_to_none = "../fixtures/flowers.db"
		self.db_is_present = False
		self.db_deleted = False
		if not os.path.isfile(self.path_to_db):
			try:
				open(self.path_to_db, "w").close()
				self.db_is_present = True
			except:
				pass
		else:
			self.db_is_present = True
			
		self.sm = sqm.SQLiteMgr(self.path_to_none)
		self.sm.delete_db(self.path_to_db)
		self.db_deleted = not os.path.isfile(self.path_to_db)	# evaluates to False if os.path.isfile returns True (and vice versa), 
																# meaning db was not deleted (i.e., it's False)

	def test_db_is_present(self):
		self.assertEqual(self.db_is_present, True)

	def test_delete_db(self):
		self.assertEqual(self.db_deleted, True)


	def test_result(self):
		self.assertEqual(self.sm.result, "OK")
		self.assertEqual(self.sm.status, "In SQLiteMgr delete_db: Deleted " + self.path_to_db)


	def tearDown(self):

		self.sm.__del__()


		
	
if __name__ == '__main__':
	unittest.main()
