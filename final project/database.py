import sqlite3
from sqlite3 import Error
def create_connection():
    """
    Create a database connection to the SQLite database for the final project.
    :return: Connection object or None if an error occurs.
    """
    db_file = "final_project_databases.db" 
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn