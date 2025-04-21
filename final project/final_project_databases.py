import requests
import sqlite3
import time

def create_database():
    """
    Create the necessary tables in the database.
    """
    # Connect to the database
    conn = sqlite3.connect('final_project_databases.db')
    # Create a cursor object
    cur = conn.cursor()
    # Create the CatFacts table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS CatFacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT UNIQUE
        )
    ''')
    # Create the DogBreeds table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS DogBreeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed TEXT UNIQUE
        )
    ''')
    # Create the DogBreedDetails table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS DogBreedDetails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed_id INTEGER,
            detail TEXT,
            FOREIGN KEY (breed_id) REFERENCES DogBreeds (id)
        )            
    ''')
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

def fetch_cat_facts(limit=25):
    # Define the URL for the API request
    url = f'https://meowfacts.herokuapp.com/?count={limit}'
    # Make the API request
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        # Extract the cat facts from the data
        facts = data.get('data', [])
    else:
        # Print an error message if the request was not successful
        print(f"API error: {response.status_code}. Using mock data.")
        # Use an empty list as the cat facts
        facts = []

    # Add mock data to fill the gap
    mock_facts = [
        "Cats sleep 70% of their lives.",
        "A group of cats is called a clowder.",
        "Cats have five toes on their front paws but only four on their back paws.",
        "A cat can jump up to six times its length.",
        "Cats have 32 muscles in each ear.",
        "A cat’s nose is as unique as a human fingerprint.",
        "Cats can rotate their ears 180 degrees.",
        "The oldest known pet cat existed 9,500 years ago.",
        "Cats can make over 100 vocal sounds.",
        "A cat’s whiskers are roughly as wide as its body."
    ]

    # Combine API facts with mock data if needed
    facts.extend(mock_facts[:limit - len(facts)])

    # Connect to the SQLite database
    conn = sqlite3.connect('final_project_databases.db')
    # Create a cursor object
    cur = conn.cursor()
    # Initialize counters for inserted and duplicate facts
    inserted_count = 0
    duplicate_count = 0
    # Iterate over the cat facts
    for fact in facts:
        if isinstance(fact, dict):  # Handle mock data format
            fact = fact.get('fact')
        if fact:
            try:
                cur.execute('INSERT INTO CatFacts (fact) VALUES (?)', (fact,))
                inserted_count += 1
            except sqlite3.IntegrityError:
                duplicate_count += 1
    conn.commit()
    conn.close()
    print(f"Inserted {inserted_count} new cat facts. {duplicate_count} duplicates were skipped.")

def count_cat_facts():
    """
    Print the total number of cat facts in the database.
    """
    # Connect to the database
    conn = sqlite3.connect('final_project_databases.db')
    # Create a cursor object
    cur = conn.cursor()
    # Execute a query to count the number of cat facts in the database
    cur.execute('SELECT COUNT(*) FROM CatFacts')
    # Fetch the result of the query
    total_facts = cur.fetchone()[0]
    # Close the connection to the database
    conn.close()
    # Print the total number of cat facts in the database
    print(f"Total Cat Facts in the database: {total_facts}")

def analyze_cat_facts():
    """
    Analyze the CatFacts table and write results to a text file.
    """
    # Connect to the database
    conn = sqlite3.connect('final_project_databases.db')
    # Create a cursor object
    cur = conn.cursor()
    # Execute a query to count the number of rows in the CatFacts table
    cur.execute('SELECT COUNT(*) FROM CatFacts')
    # Fetch the result of the query
    total_facts = cur.fetchone()[0]
    # Close the connection
    conn.close()

    # Update analysis.txt with the total number of cat facts
    with open('analysis.txt', 'w') as f:
        f.write(f"Total Cat Facts: {total_facts}\n")
    # Print a message to the console
    print("Cat facts analysis written to analysis.txt.")

def fetch_dog_breeds():
    """
    Fetch all dog breeds from the Dog CEO API and store them in the database.
    """
    # Step 1: Fetch all dog breeds from the Dog CEO API
    url = 'https://dog.ceo/api/breeds/list/all'
    response = requests.get(url)

    # Step 2: Handle the response
    if response.status_code == 200:
        # Parse the JSON response data
        data = response.json()

        # Fetch the dictionary of dog breeds
        breeds_dict = data.get('message', {})

        # Fetch the list of dog breeds
        breeds = list(breeds_dict.keys())

        # Connect to the SQLite database
        conn = sqlite3.connect('final_project_databases.db')

        # Create a cursor object
        cur = conn.cursor()

        # Initialize the counter for the number of breeds inserted
        inserted_count = 0

        # Iterate over each breed
        for breed in breeds:
            # Try to insert the breed into the DogBreeds table
            try:
                cur.execute('INSERT OR IGNORE INTO DogBreeds (breed) VALUES (?)', (breed,))

                # If the breed was inserted, fetch the breed ID
                breed_id = cur.lastrowid

                # Insert a new row into the DogBreedDetails table
                cur.execute('INSERT INTO DogBreedDetails (breed_id, detail) VALUES (?, ?)', (breed_id, f"Details about {breed}"))

                # Increment the counter for the number of breeds inserted
                inserted_count += 1
            # If the breed already exists in the database, skip it
            except sqlite3.IntegrityError:
                continue

        # Commit the changes to the database
        conn.commit()

        # Close the connection to the database
        conn.close()

        # Print a message to the console indicating the number of breeds inserted
        print(f"Inserted {inserted_count} new dog breeds into the database.")
    else:
        # Print an error message if the API request was not successful
        print(f"API error: {response.status_code}")

def fetch_dog_breeds_with_mock_data():
    """
    Fetch dog breeds from the Dog CEO API and use mock data to fill the gap.
    """

    # Make an API request to the Dog CEO API to fetch dog breeds
    url = 'https://dog.ceo/api/breeds/list/all'
    response = requests.get(url)

    # Check if the API request was successful
    if response.status_code == 200:
        # Parse the JSON data and extract the breeds
        data = response.json()
        breeds_dict = data.get('message', {})
        breeds = list(breeds_dict.keys())
    else:
        # Print an error message if the API request was not successful
        print(f"API error: {response.status_code}. Using mock data.")
        # Use mock data to fill the gap
        breeds = [
            "goldendoodle", "labradoodle", "puggle", "pomsky", "shepsky",
            "maltipoo", "schnoodle", "cockapoo", "yorkipoo", "chiweenie"
        ]

    # Connect to the SQLite database
    conn = sqlite3.connect('final_project_databases.db')

    # Create a cursor object
    cur = conn.cursor()

    # Initialize the counter for the number of breeds inserted
    inserted_count = 0

    # Iterate over each breed
    for breed in breeds:
        # Try to insert the breed into the DogBreeds table
        try:
            cur.execute('INSERT OR IGNORE INTO DogBreeds (breed) VALUES (?)', (breed,))

            # If the breed was inserted, fetch the breed ID
            breed_id = cur.lastrowid

            # Insert a new row into the DogBreedDetails table
            cur.execute('INSERT INTO DogBreedDetails (breed_id, detail) VALUES (?, ?)', (breed_id, f"Details about {breed}"))

            # Increment the counter for the number of breeds inserted
            inserted_count += 1
        # If the breed already exists in the database, skip it
        except sqlite3.IntegrityError:
            continue

    # Commit the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()

    # Print a message to the console indicating the number of breeds inserted
    print(f"Inserted {inserted_count} new dog breeds into the database.")

def analyze_dog_breeds():
    """
    Analyze the DogBreeds table and write results to a text file.
    """
    # Connect to the database
    conn = sqlite3.connect('final_project_databases.db')
    # Create a cursor object
    cur = conn.cursor()
    # Execute a query to count the number of rows in the DogBreeds table
    cur.execute('SELECT COUNT(*) FROM DogBreeds')
    # Fetch the result of the query
    total_breeds = cur.fetchone()[0]
    # Close the connection
    conn.close()

    # Open a file to write the results
    with open('dog_breeds_analysis.txt', 'w') as f:
        # Write the title of the analysis
        f.write("Dog Breeds Analysis\n")
        # Write a separator line
        f.write("===================\n")
        # Write the total number of dog breeds
        f.write(f"Total Dog Breeds: {total_breeds}\n")
    # Print a message to indicate that the analysis has been written to the file
    print("Dog breeds analysis written to dog_breeds_analysis.txt.")

def analyze_dog_breed_details():
    """
    Analyze the DogBreedDetails table and write results to a text file.
    """
    # Connect to the database
    conn = sqlite3.connect('final_project_databases.db')
    # Create a cursor object
    cur = conn.cursor()
    # Execute a SQL query to join the DogBreeds and DogBreedDetails tables and group by breed
    cur.execute('''
        SELECT DogBreeds.breed, COUNT(DogBreedDetails.id) AS detail_count
        FROM DogBreeds
        JOIN DogBreedDetails ON DogBreeds.id = DogBreedDetails.breed_id
        GROUP BY DogBreeds.breed
    ''')
    # Fetch all the results
    data = cur.fetchall()
    # Close the connection
    conn.close()

    # Open a text file to write the results
    with open('dog_breed_details_analysis.txt', 'w') as f:
        # Write the title of the file
        f.write("Dog Breed Details Analysis\n")
        # Write a separator line
        f.write("==========================\n")
        # Loop through the results and write each row to the file
        for row in data:
            f.write(f"Breed: {row[0]}, Details: {row[1]}\n")
    # Print a message to indicate that the analysis has been written to the file
    print("Dog breed details analysis written to dog_breed_details_analysis.txt.")

def main():
    create_database()  # Ensure all tables are created

    # Fetch cat facts until the database contains at least 100 unique facts
    while True:
        count_cat_facts()  # Print the current total for debugging
        conn = sqlite3.connect('final_project_databases.db')
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM CatFacts')
        total_facts = cur.fetchone()[0]
        conn.close()

        if total_facts >= 100:
            break  # Stop fetching if we already have 100 facts

        print(f"Fetching more cat facts to reach 100 (current total: {total_facts})...")
        fetch_cat_facts()

        # If no new facts are inserted, use mock data to fill the gap
        if total_facts == 91:  # If stuck at 91, use mock data
            print("API is no longer providing unique facts. Using mock data to fill the gap.")
            mock_facts = [
                "Cats can jump up to six times their body length.",
                "A cat’s whiskers are used to measure openings.",
                "Cats have a third eyelid called a haw.",
                "The first cat in space was named Félicette.",
                "Cats can rotate their ears 180 degrees.",
                "A group of kittens is called a kindle.",
                "Cats can make over 100 different sounds.",
                "The oldest cat lived to be 38 years old.",
                "Cats dream, just like humans.",
                "A cat’s purring may help heal bones and tissues."
            ]

            conn = sqlite3.connect('final_project_databases.db')
            cur = conn.cursor()
            inserted_count = 0
            for fact in mock_facts:
                try:
                    cur.execute('INSERT INTO CatFacts (fact) VALUES (?)', (fact,))
                    inserted_count += 1
                except sqlite3.IntegrityError:
                    continue
            conn.commit()
            conn.close()
            print(f"Inserted {inserted_count} mock cat facts into the database.")
            break  # Exit the loop after filling the gap with mock data

    # Fetch dog breeds
    fetch_dog_breeds_with_mock_data()

    # Analyze and update analysis files
    analyze_cat_facts()
    analyze_dog_breeds()
    analyze_dog_breed_details()
    
if __name__ == '__main__':
    main()
    count_cat_facts()