
import pymysql
import argparse
import Access_copy
import MySQL_generation


# Connection string
connection_string = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\store\test.accdb"  # it is modified by argument
)


def main():

    Access_copy.copy_access_database(connection_string)
    MySQL_generation.create_mysql_database(Access_copy.stored_tables)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transfer data from Access to MySQL.")
    parser.add_argument("access_path", help="Path to the Access .accdb file.")

    args = parser.parse_args()
    connection_string = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            r"DBQ=" + str(args.access_path)
    )
    main()
