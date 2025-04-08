# Databases we will use in this project.
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def close_connection(conn):
    """ close the database connection """
    if conn:
        conn.close()
        print("Connection closed.")
    else:
        print("No connection to close.")
    return None