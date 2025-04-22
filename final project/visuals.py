import sqlite3
import matplotlib.pyplot as plt

def visualize_cat_facts_distribution():
    """Visualize the distribution of cat facts lengths."""
    
    # Establish a connection to the SQLite database
    with sqlite3.connect('final_project_databases.db') as conn:
        # Create a cursor object to interact with the database
        cur = conn.cursor()
        # Execute a SQL query to select the length of each cat fact
        cur.execute('SELECT LENGTH(fact) FROM CatFacts')
        # Fetch all results and extract the lengths into a list
        fact_lengths = [row[0] for row in cur.fetchall()]
    
    # Check if there are any fact lengths to visualize
    if not fact_lengths:
        # Print a message if no data is available for visualization
        print("No data available in the CatFacts table for visualization.")
        return

    # Create a new figure for the histogram with specified size
    plt.figure(figsize=(10, 6))
    # Plot a histogram of the cat fact lengths
    plt.hist(fact_lengths, bins=10, color='skyblue', edgecolor='black')
    # Set the title of the plot
    plt.title('Distribution of Cat Fact Lengths')
    # Label the x-axis
    plt.xlabel('Length of Fact')
    # Label the y-axis
    plt.ylabel('Number of Facts')
    # Add grid lines to the y-axis for better readability
    plt.grid(axis='y', alpha=0.75)
    # Save the plot as a PNG file
    plt.savefig('cat_fact_lengths.png')
    # Close the plot to free up memory
    plt.close()  
    # Print a message indicating that the visualization has been saved
    print("Cat fact lengths visualization saved as 'cat_fact_lengths.png'.")

def visualize_dog_breed_counts():
    """Visualize the distribution of dog breeds using a pie chart, limited to 25 breeds."""
    
    # Open a connection to the SQLite database
    with sqlite3.connect('final_project_databases.db') as conn:
        # Create a cursor object to interact with the database
        cur = conn.cursor()
        
        # Execute a SQL query to select the breed and count the number of times 
        # each breed appears in the DogBreeds table, limited to 25
        cur.execute('SELECT breed, COUNT(*) FROM DogBreeds GROUP BY breed LIMIT 25')
        
        # Fetch all results from the query and store them in a list
        breed_data = cur.fetchall()
    
    # Extract the breeds and counts from the list
    breeds = [row[0] for row in breed_data]  # List comprehension to extract breeds
    counts = [row[1] for row in breed_data]  # List comprehension to extract counts
    
    # Create a new figure for the pie chart with specified size
    plt.figure(figsize=(10, 10))
    
    # Plot a pie chart of the dog breeds
    plt.pie(counts, 
            labels=breeds,  # Set the labels for each slice
            autopct='%1.1f%%',  # Set the format for the percentage in the slice
            startangle=140,  # Set the angle for the first slice
            colors=plt.cm.Paired.colors)  # Set the colors of the slices
    
    # Set the title of the plot
    plt.title('Distribution of Dog Breeds (Top 25)')
    
    # Ensure the aspect ratio of the plot is equal so the pie chart appears as a circle
    plt.axis('equal')
    
    # Save the plot as a PNG file
    plt.savefig('dog_breed_distribution_pie.png')
    
    # Close the figure after saving to free up memory
    plt.close()

if __name__ == '__main__':
    visualize_cat_facts_distribution()
    visualize_dog_breed_counts()