"""

..	currentmodule:: sqlitemgr
	:platform: Linux, Unix, Windows
	:synopsis: SQLite Manager class for managing databases, connections and tables.

.. moduleauthor:: Vollund Leysing aescwork@protonmail.com


"""
import os
import sqlite3 as lite


class SQLiteMgr:
	"""
		
		SQLite Manager class for managing databases, connections and tables.

	.. note::
		This is a note.

	"""


	def __init__(self, db=""):

		"""

		Args: 
			db (str): 		The name of the sqlite database the object is to access.

		"""

		self.status = "NONE"
		self.result = "NONE"
		self.db = db 
		self.table_statement = ""
		self.table_name = ""
		self.conn = None
		self.cursor = None
		self.method_compose_statement = False


	def __del__(self):
		if self.conn:
			self.conn.close()



	def close_db(self):
		""" 
		Close the connection to the database.
		""" 
	
		if self.conn:	
			self.conn.close()
			self.conn = None
			self.cursor = None



	def make_conn(self):
		""" 
		This method creates and returns a connection.
		"""
		if self.conn is not None:
			self.conn.close()

		try:
			self.conn = lite.connect(self.db)
			self._set_result_and_status("OK","In SQLiteMgr make_conn, created connection to db " + self.db)
		except Exception as e:
			self._set_result_and_status("FAIL", "In SQLiteMgr make_conn: " + self.db)
			self.conn = None	

		return self.conn


	def get_cursor(self):
		""" 
		This method creates and returns a cursor for executing SQL statements with the database connection. A connection must first have been created.
		Returns:
			cursor:	A cursor which can then be used by calling code elsewhere.
		"""
		if self.conn is None:
			self.make_conn()

		try:
			self.cursor = self.conn.cursor()
			self._set_result_and_status("OK", "In SQLiteMgr get_cursor: created cursor")
		except Exception as e:
			self._set_result_and_status("FAIL", "In SQLiteMgr get_cursor: " + str(e))
			self.cursor = None

		return self.cursor	


	### METHODS FOR COMPOSING AND EXECUTING AN SQL STATEMENT FOR CREATING A TABLE ###


	def new_table(self, table_name):

		""" 
			Start the process to create a new table in the database.  (The name of the database to add the table to is the one assigned to self.db.) 
			This method adds the beginning of an sql create statement to self.table_statement.  self.table_statement is the query that is executed 
			to actually create the table.  If self.table_statement is composed by calling the methods of this class, it always starts 
			with "CREATE TABLE IF NOT EXISTS table_name (. Note the double quote at the beginning of the table_statement: the table_statement 
			is always preceded and concluded by double quotes.

			Args:
				table_name (str): the name for the table
		
			Returns:
				self (for method chaining)

		"""
		self.table_name = table_name
		self.table_statement = "CREATE TABLE IF NOT EXISTS " + self.table_name + "("
	
		return self


	def add_table_column(self, column_name, column_data_type, column_table_constraint=""):
		""" 
		Composes a part of self.table_statement needed for creating a single column. The basic syntax for creating a column for sqlite is:
			column name datatype TABLE CONSTRAINT.  

		Args:
			column_name (str):				the name of the column
			column_data_type (str):			values: null, integer, real, text, blob
			column_table_constraint (str):	values: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT

		Returns:
			self (for method chaining)

		One or more calls to add_table_column (and create_table) methods can be chained one after the other:

		sqlmgrObject.add_table_column("id", "integer", "NOT NULL").add_table_column("some_name", text, "UNIQUE").add_table_column("owner", text).create_table()

		""" 
		self.method_compose_statement = True
		self.table_statement = self.table_statement + column_name + " " + column_data_type 
		if column_table_constraint is not "":
			self.table_statement = self.table_statement + " " + column_table_constraint + ", "
		else:
			self.table_statement = self.table_statement + ", "

		return self
	

	def create_table(self):
		""" 
		Create a table in the database.  This method executes the sql to create the table in the database.  
		It sets self.status to the error message thrown by the Exception if there was any problem.
		"""
		
		size_ts = len(self.table_statement)

		if self.table_statement[size_ts - 2:size_ts] == ", ":			# if self.table_statement has a ", " at the end of it, chop it off
			self.table_statement = self.table_statement[:size_ts - 2]
		
		if self.method_compose_statement:
			self.table_statement = self.table_statement + ')'	# append a '")' to the end of self.table_statement if method calls were used 
																# to compose the table_statement

		if self._conn_cursor_test_create():
			try:
				self.cursor.execute(self.table_statement) 						# execute self.table_statement
				self._set_result_and_status("OK", "In SQLiteMgr create_table: executed statement to create table" + self.table_name)
			except Exception as e:
				self._set_result_and_status("FAIL", "In SQLiteMgr create_table, ERROR: " +  str(e))

		else:
			self._set_result_and_status("FAIL", "In SQLiteMgr create_table: Unable to create connection or cursor for executing commands on the table.")

		

	### ###
		

	def set_table_statement(self, table_statement):
		""" 
		This method allows self.table_statement to be set directly rather than by method calls.  Follow this with
		a call to create_table to execute the sql and add the table to the database.

		Returns:
			self (for method chaining)
		""" 
		self.table_statement = table_statement
		return self



	def delete_table(self):
		""" 
		Delete a table in the database.  The names of the table which will be deleted and the database in which the 
		table resides are those stored in self.table and self.db.
		"""

		if self._conn_cursor_test_create():
			if self.table_name != "":
				try:
					statement = "DROP TABLE IF EXISTS " + self.table_name + ";"
					self.cursor.executescript(statement)
					self._set_result_and_status("OK", "In SQLiteMgr delete_table, deleted table " + self.table_name)
				except Exception as e:
					self._set_result_and_status("FAIL", "In SQLiteMgr delete_table, ERROR: " + str(e))
			else:
				self._set_result_and_status("FAIL", "In SQLiteMgr delete_table, unable to establish connection and/or get the cursor.")


	def create_db(self, db_name):
		"""
		Create a new database file.  The path/name of the database must first be assigned to self.db by the constructor or directly.

		Args:
			db_name (str):	The name of the database file to be created. (This should have a '.db' extension at the end of it.)
		"""

		if os.path.isfile(self.db) is False:
			try:
				open(db_name, "w").close()
				self._set_result_and_status("OK", "In SQLiteMgr create_db: Created " + db_name)
			except Exception as e:
				self._set_result_and_status("FAIL", "In SQLiteMgr create_db, ERROR: " + str(e))

		else:
			self._set_result_and_status("FAIL", "In SQLiteMgr Create db: database file " + self.db + " already exists.")
			
	

	def delete_db(self, db_name):
		""" 
		Delete a database file.  The path/name of the database must first be assigned to self.db either by the constructor or directly assigning 
		a value to the attribute.

		Args:
			db_name (str):	The name of the database file to be created. (This should have a '.db' extension at the end of it.)
		"""
		if db_name == self.db:
			self.close_db()
		if os.path.isfile(db_name):
			try:
				os.remove(db_name)
				self._set_result_and_status("OK", "In SQLiteMgr delete_db: Deleted " + db_name)
			except Exception as e:
				self._set_result_and_status("FAIL", "In SQLiteMgr delete_db, ERROR: " + str(e))

		else:
			self._set_result_and_status("FAIL", "In SQLiteMgr Create db: database file " + db_name + " already exists.")



	def get_number_tables_db(self):
		""" 
		Executes a query against the database sqlite_master to the names of all the tables in the database.
		Returns:
				 the total number of all tables in the object's database (resulting from calling len() on the structure returned by cursor.fetchall())..
	
		"""
		if self._conn_cursor_test_create():
			try:
				self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
				self._set_result_and_status("OK", "In SQLiteMgr get_number_tables_db: accessed db: " + self.db)
			except Exception as e:
				self._set_result_and_status("FAIL", "In SQLiteMgr get_number_tables_db, ERROR: " + str(e))
				return None
		else:
			self._set_result_and_status("FAIL", "In SQLiteMgr get_number_tables_db, unable to establish connection and/or get the cursor.")
			return None
		
		if self.result == "OK":
			return len(self.cursor.fetchall())


	def get_number_rows_in_table(self, table_name):
		""" 
		Return the number of rows in table_name, assuming table_name is actually in self.db.
	
		Args:
			table_name (str):	The name of the table whose rows are to be counted.
		
		Returns:
				None (NoneType):	(if there was a problem obtaining the connection or the cursor.)
		"""
		if self._conn_cursor_test_create():
			try:
				self.cursor.execute("SELECT Count(*) FROM " + table_name)
				self._set_result_and_status("OK", "In SQLiteMgr get_number_rows_in_table: accessed db: " + self.db + " table: " + table_name)
			except Exception as e:
				self._set_result_and_status("FAIL", "In SQLiteMgr get_number_rows_in_table, ERROR: " + str(e))

			return self.cursor.fetchone()[0]
		else:
			self._set_result_and_status("FAIL", "In SQLiteMgr delete_table, unable to establish connection and/or get the cursor.")
			return None


	def consecutive_reindex(self, renumber_column, return_all_reordered=False, start_number=1):
		""" 

		Re-index all of the numbers in a number column of a table after one or more row deletions so that they are all consecutives.
		Example: After deleting some rows from a table, we are left with rows whose numbers are 1, 3, 4, 7, 8, 10.  This method will
		re-number all of the numbers so that they are 1, 2, 3, 4, 5, 6.

		Uses the _ROWID_ column as a reference for updating the value in the renumber_column.   
		(Every sqlite database row is automatically given a _ROWID_.)

		Args:
			number_column 		 (string):  The name of the row that has the actual row number for each row.
			return_all_reordered (Boolean): If True, returns the dictionary used to keep track of old and new renumber_column numbers
			start_number		 (int):	    The number to start with when re-ordering the renumber_column.

		"""
		
		if self._conn_cursor_test_create():
			reordered_numbers = {}			# contains {<old renumber_column number:<new renumber_column number>}

			query = "SELECT _ROWID_, " + renumber_column + " FROM " + self.table_name			# select all values for _ROWID_ and number_column from self.table
			
			index = start_number
			try:
				self.cursor.execute("SELECT _ROWID_, fruit_val from fruit_keys_and_values")
				rows = self.cursor.fetchall()
			except Exception as e:
				self._set_result_and_status("FAIL", "In SQLiteMgr consecutive_reindex: ", str(e))
				return 

			query = "UPDATE " + self.table_name + " SET " + renumber_column + "=? WHERE _ROWID_=?"

			try:
				for row in rows:
					self.cursor.execute(query, (index, row[0]))
					reordered_numbers[row[1]] = index
					index = index + 1
				
				self.conn.commit()
				self._set_result_and_status("OK", "In SQLiteMgr consecutive_reindex: accessed " + self.table_name)
					
			except Exception as e:
				self._set_result_and_status("FAIL", "In SQLiteMgr consecutive_reindex: ", str(e))
					
		else:	
			self._set_result_and_status("FAIL", "In SQLiteMgr consecutive_reindex, unable to establish connection and/or get the cursor.")
			
		if return_all_reordered:
			return reordered_numbers


	def _conn_cursor_test_create(self):
		"""
		Many of the methods of this class need a connection to a database and a cursor for executing statements.  
		This method checks to make sure that both have been established.

		Returns:
				ret_val (boolean):		This will be either True if a connection and a cursor has been established, 
										or False if one or both do not obtain.
		"""
		ret_val = True
		if self.cursor is None:				# test if there is a cursor
			if self.conn is None:			# if no cursor, test if there is a conn
				self.make_conn()				# if no conn, try to create a conn
				if self.result == "FAIL":		# if we can't make a connection, return False.
					return False
			self.get_cursor()				# if we can't get a cursor, return False.
			if self.result == "FAIL":
				return False

		return ret_val


	def _set_result_and_status(self, result, status):
		"""
		Set self.result and self.status here to help DRY out the code in the above methods.
		
		Args:
			result (string):	the result of the operation performed by the calling method.
			status (string):	the status (description) of the outcome of the operation performed by the calling method.
		"""
		self.result = result
		self.status = status


