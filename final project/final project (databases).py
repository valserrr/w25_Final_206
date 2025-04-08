# Final Project: Databases
# This code creates a SQLite database with two tables: roblox_games and minecraft_servers.
# It also includes functions to scrape data from APIs or websites, access and store data in the database,
# and calculate the average number of users visiting games according to their genre.
import sqlite3

def main():
    # Create a connection to the database
    conn = sqlite3.connect('final_project.db')
    c = conn.cursor()
     # Create the Roblox games table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS roblox_games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            genre TEXT,
            user_count INTEGER
        )
    ''')
    # Create the Minecraft servers table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS minecraft_servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_name TEXT,
            genre TEXT,
            user_count INTEGER
        )
    ''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def scrape_data():
    '''access either two APIs or one API and one website with BSoup 
    (e.g. Facebook, GitHub, Gmail, Yelp, etc). '''
    pass

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