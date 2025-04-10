#This is where we will create the data visualization for the data we have collected.
import matplotlib.pyplot as plt 
import sqlite3

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
    plt.scatter(followers, visits, color='green', alpha=0.6)
    plt.title("Followers vs Game Visits")
    plt.xlabel("Followers")
    plt.ylabel("Visits")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("followers_vs_visits_scatter.png")
    plt.show()
    visualize_scatterplot()

def visualize_bargraoh():
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
    plt.bar(titles, visits, color='skyblue')
    plt.title("Top 10 Games by Visits")
    plt.xlabel("Game Title")
    plt.ylabel("Visits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_games_bargraph.png")
    plt.show()
