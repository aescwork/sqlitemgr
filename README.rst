sqlitemgr
=========

sqlitemgr -- the SQLite Manager module -- is a wrapper class for basic management of an sqlite database and its
tables.  It can be used to create and delete database files tables, create a and return a connection to a database file as 
well as a cursor which is used for executing statements against an sqlite database.  

It has two main purposes: 1. to encapsulate all of the basic database management actions in one class, and 2. to create
tables with the option of not having to directly enter the structured query language necessary.  Specific methods for
composing and executing sql statements can be chained together for creating tables (including specifying column names, data types
and constraints) in an sqlite database.  

There are also a few utility methods for managing data in and getting information about the tables.  These can get the
number of tables in a database, get the number of rows in a table, or re-index a column which is used for storing numbers.

This module was written as a companion to the sqliteminor module, whose functionality focuses on creating, reading, updating and deleting
data in sqlite database columns.  
