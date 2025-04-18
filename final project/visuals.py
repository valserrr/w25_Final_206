# This is where we will create the data visualization for the data we have collected.
import matplotlib.pyplot as plt 
import sqlite3

def visualize_scatterplot():
    """Generate a scatter plot of creator followers vs game visits."""
    # Connect to the SQLite database
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()

    # Execute a SQL query to select the creator followers and game visits
    cur.execute('''
        SELECT Creators.followers, Games.visits
        FROM Games
        JOIN Creators ON Games.creator_id = Creators.creator_id
        WHERE Creators.followers IS NOT NULL AND Games.visits IS NOT NULL
        LIMIT 100
    ''')

    # Fetch all the data from the query
    data = cur.fetchall()
    conn.close()

    # Extract the followers and visits from the data
    followers = [row[0] for row in data]
    visits = [row[1] for row in data]

    # Create a scatter plot of followers vs visits
    plt.figure(figsize=(10, 6))
    plt.scatter(followers, visits, color='green', alpha=0.6)
    plt.title("Followers vs Game Visits")
    plt.xlabel("Followers")
    plt.ylabel("Visits")
    plt.grid(True)
    plt.tight_layout()
    # Save the scatterplot as a PNG file
    plt.savefig("followers_vs_visits_scatter.png")
    # Display the scatterplot
    plt.show()

def visualize_bargraph():
    """Generate a bar chart showing visits per game (top 10)."""
    # Connect to the SQLite database
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()

    # Execute a SQL query to select the top 10 games by visits
    cur.execute('''
        SELECT title, visits
        FROM Games
        ORDER BY visits DESC
        LIMIT 10
    ''')

    # Fetch the data from the database
    data = cur.fetchall()
    conn.close()

    # Extract the game titles and visits from the data
    titles = [row[0][:15] + '...' if len(row[0]) > 15 else row[0] for row in data]
    visits = [row[1] for row in data]

    # Create a bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(titles, visits, color='skyblue')
    plt.title("Top 10 Games by Visits")
    plt.xlabel("Game Title")
    plt.ylabel("Visits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the chart as a PNG file
    plt.savefig("top_games_bargraph.png")
    # Display the chart
    plt.show()

def visualize_top_twitch_games():
    """Generate a bar chart of the top 10 Twitch games by name."""
    # Connect to the SQLite database
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()

    # Execute a SQL query to select the top 10 Twitch games
    cur.execute('''
        SELECT name, box_art_url
        FROM TwitchGames
        LIMIT 10
    ''')

    # Fetch the data from the database
    data = cur.fetchall()
    print(f"Fetched {len(data)} rows for scatterplot.")
    conn.close()

    # Extract the game names and box art URLs
    names = [row[0] for row in data]
    box_art_urls = [row[1] for row in data]

    # Create a bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(names, range(len(names)), color='orchid')
    plt.title("Top 10 Twitch Games")
    plt.xlabel("Game Name")
    plt.ylabel("Index")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("twitch_top_games_bar.png")
    plt.show()

<<<<<<< HEAD:final project/data visualization.py
    if __name__ == "__main__":
        print("Starting visualization script...")

        try:
            visualize_scatterplot()
            print("Scatterplot done.")
        except Exception as e:
            print(f"Scatterplot failed: {e}")

        try:
            visualize_bargraph()
            print("Bargraph done.")
        except Exception as e:
            print(f"Bargraph failed: {e}")

        try:
            visualize_top_twitch_games()
            print("Twitch graph done.")
        except Exception as e:
            print(f"Twitch graph failed: {e}")

        print("All visualizations attempted.")
  
=======
if __name__ == "__main__":
    # Call the visualization functions
    visualize_scatterplot()
    visualize_bargraph()
    visualize_top_twitch_games()
    print("Data visualizations generated successfully.")
>>>>>>> 227240c859b79fae1f3e431336567386c127055d:final project/visuals.py
