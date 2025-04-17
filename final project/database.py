# Databases we will use in this project.
import sqlite3
from sqlite3 import Error
import requests # type: ignore
client_id = "09wmqv5mqgpcxec5wazvja5y89p1fs"
client_secret = "pwr99bomrk9shnk1ren9hdogickwam"

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

#Extra Credit Database (Twitch API)
def create_twitch_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
def get_app_access_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    return response.json().get('access_token')
