# Final Project: Databases
# This code creates a SQLite database with two tables: Creators and Games.
# It also includes functions to scrape data from APIs or websites, access and store data in the database,
import sqlite3
import requests  # type: ignore
import bs4 as bsoup  # type: ignore

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


def scrape_game_ids(limit: int = 25) -> List[int]:
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

def access_database():
    '''Access 100 rows in the database'''

    pass

def store_data():
    '''Store 100 rows in the database'''
    pass

def calculate_average_users_per_genre():
    """Calculate the average number of users visiting games according to their genre."""
    # Connect to the database
    conn = sqlite3.connect('final_project.db')
    if conn:
        # Create a cursor to run SQL queries
        cursor = conn.cursor()
        # SQL query to combine data from both tables and calculate average users per genre
        query = '''
            SELECT genre, AVG(user_count) AS average_users
            FROM (
                SELECT genre, user_count FROM roblox_games
                UNION ALL  -- Combine rows from roblox_games and minecraft_servers
                SELECT genre, user_count FROM minecraft_servers
            )
            GROUP BY genre;
        '''
        # Run the query and get all results
        results = cursor.execute(query).fetchall()

        # Open a text file to write the results
        with open('average_users_per_genre.txt', 'w') as file:
            file.write("Genre\tAverage Users\n")  # Write the header line
            for row in results:
                # Write each genre and its average user count, rounded to 2 decimal places
                file.write(f"{row[0]}\t{round(row[1], 2)}\n")
        # Commit the changes to the database
        conn.commit()
        # Close the connection when done
        conn.close()

        print("Average users per genre calculated and saved to average_users_per_genre.txt")
    else:
        print("Failed to connect to the database.")
if __name__ == "__main__":
    main()