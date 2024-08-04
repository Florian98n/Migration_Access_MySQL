import mysql.connector
from mysql.connector import Error
from datetime import datetime, date


def create_mysql_database(stored_tables):
    connection = None
    cursor = None
    try:
        # Connect to the MySQL server
        connection = mysql.connector.connect(
            host='localhost',  # Change this to your MySQL server host
            user='root',  # Change this to your MySQL username
            password='MySQL80'  # Change this to your MySQL password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            print("Connected to MySQL Server")

            # Define the name of the database you want to create
            database_name = 'new_database'

            # Check if the database exists
            cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
            result = cursor.fetchone()

            if result:
                print(f"Database '{database_name}' exists. Dropping the database.")
                # Drop the database if it exists
                cursor.execute(f"DROP DATABASE {database_name}")
                print(f"Database '{database_name}' dropped successfully.")
            else:
                print(f"Database '{database_name}' does not exist.")

            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database {database_name} created successfully")

            cursor.execute(f"USE {database_name}")

            for table in stored_tables:
                # Define the SQL query to create a new table
                create_table_query = """CREATE TABLE """ + table.table_name + """ ("""
                for column in table.columns:
                    column_text = calculate_mysql_column_line(column)
                    create_table_query += column_text + ""","""
                # create_table_query += """PRIMARY KEY (""" + str(table.columns[0][0]) + """));"""
                # no primary key -> need feature
                create_table_query = create_table_query[:-1] + """);"""
                print("query table:  " + create_table_query)
                # Execute the query to create the table
                cursor.execute(create_table_query)

                add_rows_query = """INSERT INTO """ + table.table_name + """ ("""
                for column in table.columns:
                    add_rows_query += column[0] + ""","""  # name characteristic
                add_rows_query = add_rows_query[:-1]  # erase the last ","
                add_rows_query += """) VALUES """
                add_rows_query += calculate_mysql_row_line(table.rows)
                print("query rows:  " + add_rows_query)
                # Execute the query to add the rows
                cursor.execute(add_rows_query)
                connection.commit()

    except Error as e:
        print(f"Error: {e}")
        print(f"Most likely the naming, MySQL column names must follow stricter rules ")

    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def calculate_mysql_column_line(column):
    # Start building the MySQL column definition
    mysql_column = f"`{column[0]}` "
    # column.column_name 0
    # column.type_name 1
    # column.column_size 2
    # column.is_nullable 3
    # column.column_def 4
    # Map Access data types to MySQL data types
    if column[1] == 'COUNTER':   # COUNTER in Access results primary key in MySQL
        mysql_column += "INT AUTO_INCREMENT PRIMARY KEY"
    elif column[1] == 'INTEGER':
        mysql_column += "INT"
    elif column[1] == 'VARCHAR':
        mysql_column += f"VARCHAR({column[2]})" if column[2] else "VARCHAR(255)"
    elif column[1] == 'TEXT':
        mysql_column += "TEXT"
    elif column[1] == 'DATE':
        mysql_column += "DATE"
    elif column[1] == 'DATETIME':
        mysql_column += "DATETIME"
    elif column[1] == 'BOOLEAN':
        mysql_column += "BOOLEAN"
    elif column[1] == 'DOUBLE':
        mysql_column += "DOUBLE"
    elif column[1] == 'LONGCHAR':
        mysql_column += "LONGTEXT"
    elif column[1] == 'SMALLINT':
        mysql_column += "SMALLINT"

        # NOT NULL constraint
    if column[3] == "YES":
        mysql_column += " NULL"
    else:
        mysql_column += " NOT NULL"

        # Default value
    if column[4] is not None:
        mysql_column += f" DEFAULT '{column[4]}'" if isinstance(column[4], str) else f" DEFAULT {column[4]}"

    return mysql_column


def calculate_mysql_row_line(rows):
    mysql_row = ""
    for row in rows:
        mysql_string = """("""
        for item in row:
            if item is None:
                mysql_string += "NULL" + ","
            else:
                if isinstance(item, str) or isinstance(item, datetime) or isinstance(item, date):
                    mysql_string += "'" + str(item) + "',"
                else:
                    mysql_string += str(item) + ","
        mysql_string = mysql_string[:-1] + "),"
        mysql_row += mysql_string
    mysql_row = mysql_row[:-1] + ";"

    return mysql_row
