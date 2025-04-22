import sqlite3
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

def visualize_pony_kinds():
    """
    Visualize the distribution of pony kinds with all bars in different shades of pink.
    """
    with sqlite3.connect('final_project_databases.db') as conn:
        cur = conn.cursor()
        # Fetch all kinds from the PonyCharacters table
        cur.execute('SELECT kind FROM PonyCharacters')
        data = cur.fetchall()

    if not data:
        print("No data available in the PonyCharacters table for visualization.")
        return

    # Flatten the list of kinds and split by commas
    all_kinds = []
    for row in data:
        kinds = row[0].split(', ')  # Split the string into individual kinds
        all_kinds.extend(kinds)

    # Count the occurrences of each kind
    kind_counts = Counter(all_kinds)

    # Prepare data for visualization
    kinds = list(kind_counts.keys())
    counts = list(kind_counts.values())

    # Generate different shades of pink
    pink_shades = plt.cm.pink(np.linspace(0.4, 0.9, len(kinds)))  # Corrected to lowercase 'pink'

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(kinds, counts, color=pink_shades)
    plt.title('Distribution of Pony Kinds')
    plt.xlabel('Kind')
    plt.ylabel('Number of Ponies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('pony_kinds_distribution.png')
    plt.close()
    print("Pony kinds distribution visualization saved as 'pony_kinds_distribution.png'.")

def visualize_pony_residences():
    """
    Visualize the distribution of pony residences with all bars in different shades of green.
    """
    with sqlite3.connect('final_project_databases.db') as conn:
        cur = conn.cursor()
        # Fetch all residences from the PonyCharacters table, limited to 25 ponies
        cur.execute('SELECT residence FROM PonyCharacters LIMIT 25')
        data = cur.fetchall()

    if not data:
        print("No data available in the PonyCharacters table for visualization.")
        return

    # Flatten the list of residences and split by newlines
    all_residences = []
    for row in data:
        if row[0]:  # Check if the residence is not None
            residences = row[0].split('\n')  # Split the string into individual residences
            all_residences.extend(residences)

    # Count the occurrences of each residence
    residence_counts = Counter(all_residences)

    # Prepare data for visualization
    residences = list(residence_counts.keys())
    counts = list(residence_counts.values())

    # Generate different shades of green
    green_shades = plt.cm.Greens(np.linspace(0.4, 0.9, len(residences)))

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(residences, counts, color=green_shades)
    plt.title('Distribution of Pony Residences')
    plt.xlabel('Residence')
    plt.ylabel('Number of Ponies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('pony_residences_distribution.png')
    plt.close()
    print("Pony residences distribution visualization saved as 'pony_residences_distribution.png'.")

if __name__ == '__main__':
    visualize_pony_kinds()
    visualize_pony_residences()