import pyodbc
import Table_objects_file


stored_tables = []


def copy_access_database(connection_string):
    conn = None
    tables_cursor = None
    column_cursor = None
    rows_from_table_cursor = None
    try:
        # Establishing a connection to the database
        conn = pyodbc.connect(connection_string)
        print("Access database connection is Open")
        print("Tables - Columns - Rows")

        # Create a cursor for fetching table names
        tables_cursor = conn.cursor().tables(tableType='TABLE')  # list with tables
        for table in tables_cursor:
            table_name = table.table_name

            stored_tables.append(Table_objects_file.TableObject(table_name))

            # Create a new cursor to fetch column details
            column_cursor = conn.cursor()
            column_cursor.execute(f"SELECT * FROM {table_name} WHERE 1=0")  # Reset cursor state

            columns = column_cursor.columns(table=table_name)
            for column in columns:
                stored_tables[-1].add_column([column.column_name, column.type_name, column.column_size,
                                              column.is_nullable, column.column_def])

            # Fetch all rows from the current table
            rows_from_table_cursor = conn.cursor()
            rows_from_table_cursor.execute(f"SELECT * FROM [{table_name}]")

            # Fetch and print all rows
            rows = rows_from_table_cursor.fetchall()
            for row in rows:
                stored_tables[-1].add_row(row)

        # Print stored data
        for table_index in stored_tables:
            print(table_index.table_name)
            for columns_index in table_index.columns:
                print(columns_index)
            for row_index in table_index.rows:
                print(row_index)
        conn.commit()

    except pyodbc.Error as e:
        print(f"Error: {e}")

    # Close the connection
    finally:
        # Clean-up code
        if conn:
            conn.close()
        try:
            tables_cursor.close()
        except:
            pass
        try:
            column_cursor.close()
        except:
            pass
        try:
            rows_from_table_cursor.close()
        except:
            pass
        print("Access database connection is closed")