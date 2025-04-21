import sqlite3
import matplotlib.pyplot as plt

def analyze_data():
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM CatFacts')
    cat_facts_count = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM DogBreeds')
    dog_breeds_count = cur.fetchone()[0]
    conn.close()
    with open('analysis.txt', 'w') as f:
        f.write(f'Total Cat Facts: {cat_facts_count}\n')
        f.write(f'Total Dog Breeds: {dog_breeds_count}\n')

#Bored API ANALYSIS
import sqlite3

def analyze_bored_data():
    conn = sqlite3.connect("project_data.db")
    cur = conn.cursor()

    # Count of activities by type
    cur.execute('''
        SELECT type, COUNT(*) 
        FROM BoredActivities 
        GROUP BY type
    ''')
    activity_counts = cur.fetchall()

    # Average price by type
    cur.execute('''
        SELECT type, AVG(price)
        FROM BoredActivities
        GROUP BY type
    ''')
    avg_prices = cur.fetchall()

    # Save analysis to text file
    with open("bored_analysis.txt", "w") as f:
        f.write("Activity Counts by Type:\n")
        for activity_type, count in activity_counts:
            f.write(f"{activity_type}: {count}\n")

        f.write("\nAverage Price by Type:\n")
        for activity_type, avg_price in avg_prices:
            f.write(f"{activity_type}: ${avg_price:.2f}\n")

    conn.close()

def visualize_data():
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('SELECT LENGTH(fact) FROM CatFacts')
    fact_lengths = [row[0] for row in cur.fetchall()]
    conn.close()
    plt.hist(fact_lengths, bins=10, color='skyblue', edgecolor='black')
    plt.title('Distribution of Cat Fact Lengths')
    plt.xlabel('Length of Fact')
    plt.ylabel('Number of Facts')
    plt.savefig('cat_fact_lengths.png')
    plt.show()

if __name__ == '__main__':
    analyze_data()
    visualize_data()