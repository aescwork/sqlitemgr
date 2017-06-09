
import unittest
import os
import sys
sys.path.append("../sqlitemgr/")
import sqlitemgr as sqm


class InstantiationTest(unittest.TestCase):

	def setUp(self):
		self.smgr = sqm.SQLiteMgr("test.db")


	def testMemberResult(self):
		self.assertEqual(self.smgr.result, "NONE")
			

	def testMemberStatus(self):
		self.assertEqual(self.smgr.status, "NONE")



	def testMemberDb(self):
		self.assertEqual(self.smgr.db, "test.db")
		
	
	def tearDown(self):
		self.smgr.__del__()

if __name__ == '__main__':
	unittest.main()
