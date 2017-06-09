
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm

class CreateDbTest(unittest.TestCase):
	"""
	Tests the create_db method of the SQLiteMgr object.  The object is instantiated with a false path (path_to_none) to test the
	functionality of the create_db method; that is, create_db should be able to create a database (on the fly) other than the one whose name has been
	assigned to the self.db object member.
	"""

	def setUp(self):
		self.path_to_db = "../fixtures/fruit.db"
		self.path_to_none = "../fixtures/flowers.db"
		self.db_not_present = False
		self.db_created = False
		if os.path.isfile(self.path_to_db):
			try:
				os.remove(self.path_to_db)
				self.db_not_present = True
			except:
				pass

		self.sm = sqm.SQLiteMgr(self.path_to_none)
		self.sm.create_db(self.path_to_db)
		self.db_created = os.path.isfile(self.path_to_db)

	def test_db_not_present(self):
		self.assertEqual(self.db_not_present, True)


	def test_create_db(self):
		self.assertEqual(self.db_created, True)


	def test_result(self):
		self.assertEqual(self.sm.result, "OK")
		self.assertEqual(self.sm.status, "In SQLiteMgr create_db: Created " + self.path_to_db)


	def tearDown(self):

		self.sm.__del__()


		
	
if __name__ == '__main__':
	unittest.main()
