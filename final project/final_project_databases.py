import requests
import sqlite3
import time

def create_database():
    """
    Create the necessary tables in the database.
    """
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS CatFacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT UNIQUE
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS DogBreeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed TEXT UNIQUE
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS DogBreedDetails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed_id INTEGER,
            detail TEXT,
            FOREIGN KEY (breed_id) REFERENCES DogBreeds (id)
        )
    ''')
    conn.commit()
    conn.close()

def fetch_cat_facts(limit=25):
    url = f'https://meowfacts.herokuapp.com/?count={limit}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        facts = data.get('data', [])
        conn = sqlite3.connect('final_project_databases.db')
        cur = conn.cursor()
        inserted_count = 0
        duplicate_count = 0
        for fact in facts:
            print(f"Fetched fact: {fact}")  # Debugging: Log each fact
            if fact:
                try:
                    cur.execute('INSERT INTO CatFacts (fact) VALUES (?)', (fact,))
                    inserted_count += 1
                except sqlite3.IntegrityError:
                    duplicate_count += 1
        conn.commit()
        conn.close()
        print(f"Inserted {inserted_count} new cat facts. {duplicate_count} duplicates were skipped.")
    else:
        print(f"API error: {response.status_code}")

def count_cat_facts():
    """
    Print the total number of cat facts in the database.
    """
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM CatFacts')
    total_facts = cur.fetchone()[0]
    conn.close()
    print(f"Total Cat Facts in the database: {total_facts}")

def analyze_cat_facts():
    """
    Analyze the CatFacts table and write results to a text file.
    """
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM CatFacts')
    total_facts = cur.fetchone()[0]
    conn.close()

    # Update analysis.txt with the total number of cat facts
    with open('analysis.txt', 'w') as f:
        f.write(f"Total Cat Facts: {total_facts}\n")
    print("Cat facts analysis written to analysis.txt.")

def fetch_dog_breeds():
    """
    Fetch all dog breeds from the Dog CEO API and store them in the database.
    """
    url = 'https://dog.ceo/api/breeds/list/all'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        breeds_dict = data.get('message', {})
        breeds = list(breeds_dict.keys())  # Fetch all breeds
        conn = sqlite3.connect('final_project_databases.db')
        cur = conn.cursor()
        inserted_count = 0
        for breed in breeds:
            try:
                cur.execute('INSERT OR IGNORE INTO DogBreeds (breed) VALUES (?)', (breed,))
                breed_id = cur.lastrowid
                cur.execute('INSERT INTO DogBreedDetails (breed_id, detail) VALUES (?, ?)', (breed_id, f"Details about {breed}"))
                inserted_count += 1
            except sqlite3.IntegrityError:
                continue
        conn.commit()
        conn.close()
        print(f"Inserted {inserted_count} new dog breeds into the database.")
    else:
        print(f"API error: {response.status_code}")

def fetch_dog_breeds_with_mock_data():
    """
    Fetch dog breeds from the Dog CEO API and use mock data to fill the gap.
    """
    url = 'https://dog.ceo/api/breeds/list/all'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        breeds_dict = data.get('message', {})
        breeds = list(breeds_dict.keys())
    else:
        print(f"API error: {response.status_code}. Using mock data.")
        breeds = [
            "goldendoodle", "labradoodle", "puggle", "pomsky", "shepsky",
            "maltipoo", "schnoodle", "cockapoo", "yorkipoo", "chiweenie"
        ]

    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    inserted_count = 0
    for breed in breeds:
        try:
            cur.execute('INSERT OR IGNORE INTO DogBreeds (breed) VALUES (?)', (breed,))
            breed_id = cur.lastrowid
            cur.execute('INSERT INTO DogBreedDetails (breed_id, detail) VALUES (?, ?)', (breed_id, f"Details about {breed}"))
            inserted_count += 1
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    conn.close()
    print(f"Inserted {inserted_count} new dog breeds into the database.")

def analyze_dog_breeds():
    """
    Analyze the DogBreeds table and write results to a text file.
    """
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM DogBreeds')
    total_breeds = cur.fetchone()[0]
    conn.close()

    with open('dog_breeds_analysis.txt', 'w') as f:
        f.write("Dog Breeds Analysis\n")
        f.write("===================\n")
        f.write(f"Total Dog Breeds: {total_breeds}\n")
    print("Dog breeds analysis written to dog_breeds_analysis.txt.")

def analyze_dog_breed_details():
    """
    Analyze the DogBreedDetails table and write results to a text file.
    """
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT DogBreeds.breed, COUNT(DogBreedDetails.id) AS detail_count
        FROM DogBreeds
        JOIN DogBreedDetails ON DogBreeds.id = DogBreedDetails.breed_id
        GROUP BY DogBreeds.breed
    ''')
    data = cur.fetchall()
    conn.close()

    with open('dog_breed_details_analysis.txt', 'w') as f:
        f.write("Dog Breed Details Analysis\n")
        f.write("==========================\n")
        for row in data:
            f.write(f"Breed: {row[0]}, Details: {row[1]}\n")
    print("Dog breed details analysis written to dog_breed_details_analysis.txt.")

#EXTRA CREDIT API

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
        time.sleep(1)  # Avoid hitting the API rate limit

    # Fetch dog breeds
    fetch_dog_breeds_with_mock_data()

    # Analyze and update analysis files
    analyze_cat_facts()
    analyze_dog_breeds()
    analyze_dog_breed_details()
if __name__ == '__main__':
    main()
    count_cat_facts()