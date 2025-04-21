import sqlite3
from sqlite3 import Error
def create_connection():
    """
    Create a database connection to the SQLite database for the final project.
    
    Returns:
        Connection object or None: The connection object to the SQLite database if successful, 
        or None if an error occurs.
    """
    db_file = "final_project_databases.db"  # Specify the path to the database file
    conn = None  # Initialize the connection variable to None
    try:
        # Attempt to create a connection to the SQLite database
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")  # Informative message upon successful connection
        return conn  # Return the connection object if connection is successful
    except Error as e:
        # Capture and print any errors that occur during the connection attempt
        print(f"Error connecting to database: {e}")
    return conn  # Return None if connection was unsuccessful due to an error
