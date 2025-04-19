# Databases we will use in this project.
import sqlite3
from sqlite3 import Error
import requests
from visuals import visualize_scatterplot
from robloxpy import Game, User 

# Twitch API credentials
client_id = "09wmqv5mqgpcxec5wazvja5y89p1fs"
client_secret = "pwr99bomrk9shnk1ren9hdogickwam"

def create_connection(db_file):
    """
    Create a database connection to a SQLite database.
    :param db_file: Path to the SQLite database file.
    :return: Connection object or None if an error occurs.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def close_connection(conn):
    """
    Close the database connection.
    :param conn: Connection object.
    """
    if conn:
        conn.close()
        print("Connection closed.")
    else:
        print("No connection to close.")

def get_app_access_token(client_id, client_secret):
    """
    Get an app access token from the Twitch API.
    :param client_id: Twitch API client ID.
    :param client_secret: Twitch API client secret.
    :return: Access token as a string or None if an error occurs.
    """
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        access_token = response.json().get('access_token')
        if access_token:
            print("Successfully retrieved access token.")
        else:
            print("Failed to retrieve access token.")
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error fetching access token: {e}")
        return None

def create_twitch_connection(db_file):
    """
    Create a database connection to a SQLite database for Twitch data.
    :param db_file: Path to the SQLite database file.
    :return: Connection object or None if an error occurs.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to Twitch database: {db_file}")
        return conn
    except Error as e:
        print(f"Error connecting to Twitch database: {e}")
    return conn

def initialize_twitch_database(db_file):
    """
    Initialize the Twitch database by creating the necessary tables.
    :param db_file: Path to the SQLite database file.
    """
    conn = create_twitch_connection(db_file)
    if conn:
        try:
            cur = conn.cursor()
            # Enable foreign key constraints
            cur.execute("PRAGMA foreign_keys = ON")
            # Create the TwitchGames table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS TwitchGames (
                    game_id INTEGER PRIMARY KEY,
                    name TEXT,
                    box_art_url TEXT
                )
            ''')
            conn.commit()
            print("Twitch database initialized successfully.")
        except Error as e:
            print(f"Error initializing Twitch database: {e}")
        finally:
            close_connection(conn)
    else:
        print("Failed to initialize Twitch database.")
def store_twitch_games(token, client_id):
    """
    Store Twitch games in the database using the Twitch API.
    :param token: Twitch API access token.
    :param client_id: Twitch API client ID.
    """
    url = 'https://api.twitch.tv/helix/games/top'
    headers = {
        'Authorization': f'Bearer {token}',
        'Client-Id': client_id
    }
    params = {'first': 100}  # Fetch up to 100 games
    conn = create_twitch_connection("twitch.db")
    if conn:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            games = response.json().get('data', [])
            cur = conn.cursor()
            for game in games:
                cur.execute('''
                    INSERT OR IGNORE INTO TwitchGames (game_id, name, box_art_url)
                    VALUES (?, ?, ?)
                ''', (game['id'], game['name'], game['box_art_url']))
            conn.commit()
            print("Twitch games stored successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Twitch games: {e}")
        except Error as e:
            print(f"Error storing Twitch games in database: {e}")
        finally:
            close_connection(conn)
    else:
        print("Failed to store Twitch games.")

# Get Twitch token and store Twitch games
token = get_app_access_token(client_id, client_secret)
if token:
    initialize_twitch_database("twitch.db")  # <- Added this line
    store_twitch_games(token, client_id)
    
