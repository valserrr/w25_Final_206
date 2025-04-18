# Final Project: Databases
# This code is part of a final project for a course on databases.
# The project involves scraping data from Roblox, storing it in a SQLite database, and performing some analysis.
import sqlite3
import requests
import bs4 as bsoup  
from robloxpy import Game, User  

def create_tables():
    """Create the database and tables if they don't exist."""
    conn = sqlite3.connect('roblox.db')
    c = conn.cursor()
    # Enable foreign key constraints
    c.execute("PRAGMA foreign_keys = ON")
    # Create the Creators table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Creators (
            creator_id INTEGER PRIMARY KEY,
            username TEXT,
            followers INTEGER,
            account_age INTEGER
        )
    ''')
    # Create the Games table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Games (
            game_id INTEGER PRIMARY KEY,
            title TEXT,
            visits INTEGER,
            creator_id INTEGER,
            FOREIGN KEY (creator_id) REFERENCES Creators (creator_id)
        )
    ''')
    # Create the TwitchGames table
    c.execute('''
        CREATE TABLE IF NOT EXISTS TwitchGames (
            game_id INTEGER PRIMARY KEY,
            name TEXT,
            box_art_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def scrape_game_ids(limit: int = 25) -> list[int]:
    """Scrape Roblox game IDs from the discover page."""
    url = 'https://www.roblox.com/discover'
    response = requests.get(url)
    soup = bsoup.BeautifulSoup(response.text, 'html.parser')
    game_links = soup.find_all('a', class_='game-card-link')
    game_ids = set()
    for link in game_links:
        href = link.get('href')
        if '/games/' in href:
            try:
                game_id = int(href.split('/games/')[1].split('/')[0])
                game_ids.add(game_id)
            except ValueError:
                continue
        if len(game_ids) >= limit:
            break
    return list(game_ids)

def scrape_game_creator_info(game_id):
    """Scrape game creator info from the Roblox API."""
    try:
        game = Game.Game(game_id)
        creator_username = game.Creator()
        visits = game.Visits()
        title = game.Title()

        creator = User.User(creator_username)
        creator_id = creator.Id
        followers = creator.FollowersCount()
        account_age = creator.AccountAge()
        return {
            'game_id': game_id,
            'title': title,
            'visits': visits,
            'creator_id': creator_id,
            'creator_username': creator_username,
            'followers': followers,
            'account_age': account_age,
        }
    except Exception as e:
        print(f"Failed scraping game creator info for game {game_id}: {e}")
        return None

def store_data(limit=100):
    """Store data in the database."""
    create_tables()
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    game_ids = scrape_game_ids(limit)
    inserted = 0
    for game_id in game_ids:
        data = scrape_game_creator_info(game_id)
        if data:
            cur.execute('''
                INSERT OR IGNORE INTO Creators (creator_id, username, followers, account_age)
                VALUES (?, ?, ?, ?)
            ''', (data['creator_id'], data['creator_username'], data['followers'], data['account_age']))
            cur.execute('''
                INSERT OR IGNORE INTO Games (game_id, title, visits, creator_id)
                VALUES (?, ?, ?, ?)
            ''', (data['game_id'], data['title'], data['visits'], data['creator_id']))
            inserted += 1
            if inserted >= limit:
                break
        conn.commit()
    conn.close()
    print(f"Inserted {inserted} rows into the database.")

def fetch_top_games(token, client_id, limit=100):
    """Fetch the top games from the Twitch API."""
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}'
    }
    url = f'https://api.twitch.tv/helix/games/top?first={limit}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Twitch API: {e}")
        return []

def store_twitch_games(token, client_id):
    """Store Twitch games data in the database."""
    create_tables()  # Ensure the table exists
    games = fetch_top_games(token, client_id)
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    for game in games:
        game_id = int(game['id'])
        name = game['name']
        box_art_url = game['box_art_url']
        cur.execute('''
            INSERT OR IGNORE INTO TwitchGames (game_id, name, box_art_url)
            VALUES (?, ?, ?)
        ''', (game_id, name, box_art_url))
    conn.commit()
    conn.close()
    print("Stored Twitch games in the database.")

def write_twitch_analysis_to_txt():
    """Write the top 10 Twitch games to a text file."""
    try:
        conn = sqlite3.connect('roblox.db')
        cur = conn.cursor()
        cur.execute('''
            SELECT name FROM TwitchGames
            LIMIT 10
        ''')
        top_games = cur.fetchall()
        conn.close()
        with open('twitch_top_games.txt', 'w') as f:
            f.write("Top 10 Games:\n")
            for name, in top_games:
                f.write(f"{name}\n")
        print("Wrote Twitch game analysis to twitch_top_games.txt")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    if __name__ == "__main__":
        create_tables()
        store_data(25)