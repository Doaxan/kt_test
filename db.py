import os
import sqlite3


def create_table():
    try:
        sqlite_connection = sqlite3.connect(os.getenv('DB_CONN', 'rates.db'))
        sqlite_create_table_query = '''CREATE TABLE rates (
                                    id INTEGER PRIMARY KEY,
                                    created_at datetime,
                                    usd_price REAL,
                                    volume_24h REAL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("sqlite connection is closed")


def insert_data_table(created_at, usd_price, volume_24h):
    try:
        sqlite_connection = sqlite3.connect(os.getenv('DB_CONN', 'rates.db'))
        cursor = sqlite_connection.cursor()
        sqlite_insert_with_param = """INSERT INTO rates
                          (created_at, usd_price, volume_24h) 
                          VALUES (?, ?, ?);"""

        data_tuple = (created_at, usd_price, volume_24h)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def insert_api_to_table(api):
    insert_data_table(api['created_at'], api['usd_price'], api['volume_24h'])


def read_data_table(id_row=None):
    try:
        sqlite_connection = sqlite3.connect(os.getenv('DB_CONN', 'rates.db'))
        cursor = sqlite_connection.cursor()
        if id_row:
            sqlite_select_query = """SELECT created_at, usd_price, volume_24h from rates where id = ?"""
            cursor.execute(sqlite_select_query, (id_row,))
        else:
            sql_select_query = """SELECT created_at, usd_price, volume_24h from rates ORDER BY id DESC"""
            cursor.execute(sql_select_query)
        records = cursor.fetchall()

        result = []
        for row in records:
            result.append({'created_at': row[0], 'usd_price': row[1], 'volume_24h': row[2]})
        cursor.close()
        return result

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

# create_table()
# insert_to_table('2020-11-13T12:49:55.715Z', '16291.667201166987', '35899014250.54064')
