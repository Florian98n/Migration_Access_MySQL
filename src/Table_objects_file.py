import pymysql


class TableObject:
    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []
        self.rows = []

    def add_column(self, list_characteristics):
        self.columns.append(list_characteristics)

    def add_row(self, entire_row):
        self.rows.append(list(entire_row))
