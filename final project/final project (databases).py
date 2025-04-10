# Final Project: Databases
# This code creates a SQLite database with two tables: Creators and Games.
# It also includes functions to scrape data from APIs or websites, access and store data in the database,
import sqlite3
import requests  # type: ignore
import bs4 as bsoup  # type: ignore
from robloxy import Game, User  # type: ignore
def create_tables():
    conn = sqlite3.connect('roblox.db')
    c = conn.cursor()
     # Create the Creators table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS Creators (
            creator_id INTEGER PRIMARY KEY,
            username TEXT,
            followers INTEGER,
            account_age INTEGER,
        )
    ''')
    # Create the Games table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS Games (
            game_id INTEGER PRIMARY KEY,
            title TEXT,
            visits INTEGER,
            creator_id INTEGER,
              FOREIGN KEY (creator_id) REFERENCES Creators (creator_id)
        )
    ''')
    conn.commit()
    conn.close()


def scrape_game_ids(limit: int = 25) -> list[int]:
    """Scrape Roblox game IDs from the discover page."""
    # Set the URL to the Roblox discover page
    url = 'https://www.roblox.com/discover'
    response = requests.get(url)
    soup = bsoup.BeautifulSoup(response.text, 'html.parser')
    # Find all game links on the page
    # Note: The class name may change, so check the actual HTML structure
    game_links = soup.find_all('a', class_='game-card-link')
    game_ids = set()
    # Extract game IDs from the links
    # Note: The game ID is usually in the URL, e.g., /games/123456789/Game-Name
    for link in game_links:
        href = link.get('href')
        if '/games/' in href:
            try:
                game_id = int(href.split('/games/')[1].split('/')[0])
                game_ids.add(game_id)
      # Limit the number of game IDs to the specified limit
            except ValueError:
                continue
        if len(game_ids) >= limit:
            break
    return list(game_ids)

def scrape_game_creator_info(game_id):
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

def access_database(limit= 100):
    '''Access 100 rows in the database'''

    pass

def store_data(limit = 100):
    '''Store 100 rows in the database'''
    # Create the database and tables if they don't exist
    create_tables()
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()
    # Scrape game IDs
    game_ids = scrape_game_ids(limit)
    inserted = 0
    # Loop through each game ID and scrape its creator info
    for game_id in game_ids:
        data = scrape_game_creator_info(game_id)
        if data:
            # Insert creator
            cur.execute('''
                INSERT OR IGNOREINTO Creators (creator_id, username, followers, account_age)
                VALUES (?, ?, ?, ?)
            ''', (data['creator_id'], data['creator_username'], data['followers'], data['account_age']))
            # Insert game
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

def calculate_average_visits_per_creator():
    """Calculate the average number of visits per game by the creator."""
    # Connect to the database
    conn = sqlite3.connect('roblox.db')
    if conn:
        # Create a cursor to run SQL queries
        cursor = conn.cursor()
        # SQL query to combine data from both tables and calculate average visits per creator
        query = '''
            SELECT c.username, AVG(g.visits) AS average_visits
            FROM Creators c
            INNER JOIN Games g ON c.creator_id = g.creator_id
            GROUP BY c.username;
        '''
        # Run the query and get all results
        results = cursor.execute(query).fetchall()

        # Open a text file to write the results
        with open('average_visits_per_creator.txt', 'w') as file:
            # Write the header line
            file.write("Creator\tAverage Visits\n")
            for row in results:
            # Write each creator and its average visits, rounded to 2 decimal places
                file.write(f"{row[0]}\t{round(row[1], 2)}\n")
        conn.commit()
        conn.close()

        print("Average visits per creator calculated and saved to average_visits_per_creator.txt")
    else:
        print("Failed to connect to the database.")
if __name__ == "__main__":
    main()