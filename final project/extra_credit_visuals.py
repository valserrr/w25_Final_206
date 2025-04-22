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

if __name__ == '__main__':
    visualize_pony_kinds()