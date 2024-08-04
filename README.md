# Migration_Access_MySQL

The repository stores an application who migrates data from an Access database to an MySQL database.

Everything is made in python(using PyCharm IDE) and the libraryes for connection:
- with Access databse - python library pyodbc;
- with MySQL database - python library mysql.connector

The short video demonstration is hosted in github pages: [video](https://florian98n.github.io/Migration_Access_MySQL/)

Detailed steps:
1. the path and name of the Access database is given as argument for migration.exe
2. the app will connect with Access database
3. all data regarding tables, columns and rows will be stored(all tables are stored as class objects inside an list:"stored_tables = []" ) 
4. The connection with Access database will be closed
5. the app will connect with MySQL database 
6. if database new_database exists it will be droped and create an new new_database who is empty 
7. the data regarding types of columns will be adapted for MySQL usage
8. each query will be executed(CREATE TABLE ... , INSERT INTO ...)
9. The connection with MySQL database will be closed