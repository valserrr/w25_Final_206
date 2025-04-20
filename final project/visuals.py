# This is where we will create the data visualization for the data we have collected.
import matplotlib.pyplot as plt 
import sqlite3
# Twitch API credentials
client_id = "09wmqv5mqgpcxec5wazvja5y89p1fs"
client_secret = "pwr99bomrk9shnk1ren9hdogickwam"

def visualize_scatterplot():
    """Generate a scatter plot of creator followers vs game visits."""
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()

    cur.execute('''
        SELECT Creators.followers, Games.visits
        FROM Games
        JOIN Creators ON Games.creator_id = Creators.creator_id
        WHERE Creators.followers IS NOT NULL AND Games.visits IS NOT NULL
        LIMIT 100
    ''')

    data = cur.fetchall()
    conn.close()

    followers = [row[0] for row in data]
    visits = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.scatter(followers, visits, color='darkorange', alpha=0.6)
    plt.title("Creator Followers vs Game Visits")
    plt.xlabel("Followers")
    plt.ylabel("Visits")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("followers_vs_visits_scatter.png")
    plt.show()

def visualize_bargraph():
    """Generate a bar chart showing visits per game (top 10)."""
    conn = sqlite3.connect('roblox.db')
    cur = conn.cursor()

    cur.execute('''
        SELECT title, visits
        FROM Games
        ORDER BY visits DESC
        LIMIT 10
    ''')

    data = cur.fetchall()
    conn.close()

    titles = [row[0][:15] + '...' if len(row[0]) > 15 else row[0] for row in data]
    visits = [row[1] for row in data]

    plt.figure(figsize=(12, 6))
    plt.bar(titles, visits, color='mediumseagreen')
    plt.title("Top 10 Games by Visits")
    plt.xlabel("Game Title")
    plt.ylabel("Visits")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("top_games_bargraph.png")
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

if __name__ == "__main__":
    # Call the visualization functions
    visualize_scatterplot()
    visualize_bargraph()
    visualize_top_twitch_games()
    print("Data visualizations generated successfully.")
