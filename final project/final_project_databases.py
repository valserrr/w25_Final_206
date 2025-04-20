# Final Project: Databases
# This code is part of a final project for a course on databases.
# The project involves scraping data from Roblox, storing it in a SQLite database, and performing some analysis.
import sqlite3
import requests
import bs4 as bsoup  
import robloxpy
from robloxpy.Game import Internal

def create_tables():
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    # Create the Games table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Games (
            game_id INTEGER PRIMARY KEY,
            universe_id INTEGER,
            title TEXT,
            visits INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    # Create the TwitchGames table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS TwitchGames (
            game_id INTEGER PRIMARY KEY,
            name TEXT,
            box_art_url TEXT
        )
    ''')
    conn.commit()
    conn.close()
def scrape_game_ids(limit: int = 25) -> list[int]:
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
            except:
                continue
        if len(game_ids) >= limit:
            break
    return list(game_ids)

def scrape_game_data(place_id):
    try:
        universe_id = robloxpy.Game.Internal.GetUniverseID(place_id)
        visits = robloxpy.Game.Internal.GetGameVisits(place_id)
        title = f"Game {place_id}"  # Placeholder, robloxpy internal doesn’t return title
        return {
            'game_id': place_id,
            'universe_id': universe_id,
            'title': title,
            'visits': visits
        }
    except Exception as e:
        print(f"Error with place_id {place_id}: {e}")
        return None
def store_data(limit=25):
    create_tables()
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    game_ids = scrape_game_ids(limit)
    inserted = 0
    for place_id in game_ids:
        data = scrape_game_data(place_id)
        if data:
            cur.execute('''
                INSERT OR IGNORE INTO Games (game_id, universe_id, title, visits)
                VALUES (?, ?, ?, ?)
            ''', (data['game_id'], data['universe_id'], data['title'], data['visits']))
            inserted += 1
            if inserted >= limit:
                break
        conn.commit()
    conn.close()
    print(f"Inserted {inserted} rows into the database.")

    def analyze_data_and_output():
        conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()

    # Fetch data
    cur.execute("SELECT game_id, title, visits FROM Games")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No data to analyze.")
        return

    total_visits = sum([row[2] for row in rows])
    avg_visits = total_visits / len(rows)
    most_visited = max(rows, key=lambda x: x[2])

    # Write to text file
    with open("roblox_analysis.txt", "w") as f:
        f.write("ROBLOX GAME VISITS ANALYSIS\n")
        f.write("===========================\n\n")
        f.write(f"Total Games Analyzed: {len(rows)}\n")
        f.write(f"Average Visits per Game: {avg_visits:.2f}\n\n")
        f.write("Most Visited Game:\n")
        f.write(f"Game ID: {most_visited[0]}\n")
        f.write(f"Title: {most_visited[1]}\n")
        f.write(f"Visits: {most_visited[2]}\n")

    print("Analysis complete. Output written to roblox_analysis.txt.")

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
