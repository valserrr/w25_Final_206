import sqlite3
import matplotlib.pyplot as plt

def visualize_cat_facts_distribution():
    """Visualize the distribution of cat facts lengths."""
    with sqlite3.connect('final_project_databases.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT LENGTH(fact) FROM CatFacts')
        fact_lengths = [row[0] for row in cur.fetchall()]
    
    plt.figure(figsize=(10, 6))
    plt.hist(fact_lengths, bins=10, color='skyblue', edgecolor='black')
    plt.title('Distribution of Cat Fact Lengths')
    plt.xlabel('Length of Fact')
    plt.ylabel('Number of Facts')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('cat_fact_lengths.png')
    plt.close()  # Close the figure after saving

def visualize_dog_breed_counts():
    """Visualize the breed distribution using a pie chart."""
    with sqlite3.connect('final_project_databases.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT breed, COUNT(*) FROM DogBreeds GROUP BY breed')
        breed_data = cur.fetchall()
    
    breeds = [row[0] for row in breed_data]
    counts = [row[1] for row in breed_data]
    
    plt.figure(figsize=(10, 10))
    plt.pie(counts, labels=breeds, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Dog Breeds')
    plt.axis('equal')  
    plt.tight_layout()
    plt.savefig('dog_breed_distribution.png')
    plt.close()  # Close the figure after saving

def visualize_bored_activity_types():
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()

    cur.execute('''
        SELECT type, COUNT(*) as count
        FROM BoredActivities
        GROUP BY type
    ''')
    data = cur.fetchall()
    conn.close()

    types = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.bar(types, counts, color='skyblue', edgecolor='black')
    plt.xlabel("Activity Type")
    plt.ylabel("Number of Activities")
    plt.title("Distribution of Activity Types (Bored API)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.savefig('bored_activity_types.png')
    plt.close()  # Close the figure after saving

if __name__ == '__main__':
    visualize_cat_facts_distribution()
    visualize_dog_breed_counts()
visualize_bored_activity_types()