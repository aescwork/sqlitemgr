sqlitemgr
=========

This package can be found at https://github.com/aescwork/sqlitemgr. 
 
In the github repository there is sphinx-generated documentation: the main page is docs/index.html. 



sqlitemgr -- the SQLite Manager module -- is a wrapper class for basic management of an sqlite database and its
tables.  It can be used to create and delete database files, tables, create and return a connection to a database file as 
well as a cursor which is used for executing statements against an sqlite database.  

It has two main purposes: 1. to encapsulate all of the basic database management actions in one class, and 2. to create
tables with the option of not having to directly enter the structured query language necessary.  Specific methods for
composing and executing sql statements can be chained together for creating tables (including specifying column names, data types
and constraints) in an sqlite database.  

There are also a few utility methods for managing data in and getting information about the tables.  These can get the
number of tables in a database, get the number of rows in a table, or re-index a column which is used for storing numbers.

This module was written as a companion to the sqliteminor module, whose functionality focuses on creating, reading, updating and deleting
data in sqlite database columns.  

NOTE:

This module requires sqlite3 to be installed prior to use.


After installation of this package is complete, trying to use the module might result in the following error: "ImportError: No module named sqlitemgr"
or some other error message.

This probably indicates that the Python interpreter may not be able to locate the module.  In this case,
the following is recommended:

	On Linux:

		Locate where the package was installed.  In the terminal, navigate to the root directory and execute the following command:

												sudo find . -name sqlitemgr.py


		This should give a path to the sqlitemgr.py file.  
		Create a file called "local_python.sh" and put the following text in it:

								PYTHONPATH="/usr/local/lib/python*.*/dist-packages/sqlitemgr/":"${PYTHONPATH}"
								export PYTHONPATH

		To make the module available to all users, place this file in /etc/profile.d.  Then place a line to execute this
		file somewhere in .bashrc or one of the other bash configuration files in the individual (non-root) user's terminal: 

										    . /etc/profile.d/local_python.sh

		This should cause the python interpreter to locate the sqlitemgr.py file in the module.   


	On MS Windows:
		
		The following was tested on a machine running Windows 10. 
		
		(This assumes that Python is installed on the machine.)

		Locate where the package was installed.  On Windows 10, Look for the Python folder.  Its usually right under the C: drive. 
		The name of the folder probably has the version number in it as well, like "Python27".  Look for the sqlitemgr folder: it should
		be in "Lib\" and then "site-packages\" folder.  

		Open up the System Properties Panel.  (You can find this by clicking on the "Settings" icon and entering "Environment Variables" in the 
		search bar.  When the panel comes up, Click the "Environment Variables" button.  Under "System variables", click "New" and type in the full path to
		the sqlitemgr folder.

		Test this by opening the command line application and starting the Python interpreter (type the command "python" and press enter).
		Now try to import the module and instantiate an sqlitemgr object.  Type the following:
	
		>>> import sqlitemgr
		>>> sg = sqlitemgr.SQLiteMinor()
		>>> sg.result

		If everything went well, 'None' should print out on the screen.  If there was an "ImportError" or any other error, try importing the
		module again and test as follows: 


		>>> import sqlitemgr.sqlitemgr as sqlitemgr
		>>> sg = sqlitemgr.SQLiteMgr()
		>>> sg.result



