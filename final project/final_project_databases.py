import requests
import sqlite3
import time

def create_database():
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
    conn.commit()
    conn.close()

def fetch_cat_facts(limit=100):
    url = 'https://catfact.ninja/facts'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        facts = data.get('data', [])
        conn = sqlite3.connect('final_project_databases.db')
        cur = conn.cursor()
        for item in facts:
            fact = item.get('fact')
            if fact:
                try:
                    cur.execute('INSERT INTO CatFacts (fact) VALUES (?)', (fact,))
                except sqlite3.IntegrityError:
                    continue
        conn.commit()
        conn.close()

def fetch_dog_breeds(limit=100):
    url = 'https://dog.ceo/api/breeds/list/all'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        breeds_dict = data.get('message', {})
        breeds = list(breeds_dict.keys())
        conn = sqlite3.connect('final_project_databases.db')
        cur = conn.cursor()
        for breed in breeds:
            try:
                cur.execute('INSERT INTO DogBreeds (breed) VALUES (?)', (breed,))
            except sqlite3.IntegrityError:
                continue
        conn.commit()
        conn.close()

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

#Extra Credit API: DOG FACTS API
def create_database():
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
        CREATE TABLE IF NOT EXISTS DogFacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT UNIQUE
        )
    ''')  # New table for Dog Facts
    conn.commit()
    conn.close()

def fetch_dog_facts(limit=25):
    """
    Fetch dog facts from the Dog Facts API and store them in the database.
    :param limit: The number of dog facts to fetch.
    """
    url = f'https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number={limit}'
    response = requests.get(url)
    if response.status_code == 200:
        facts = response.json()
        conn = sqlite3.connect('final_project_databases.db')
        cur = conn.cursor()
        for fact in facts:
            try:
                cur.execute('INSERT INTO DogFacts (fact) VALUES (?)', (fact,))
            except sqlite3.IntegrityError:
                continue
        conn.commit()
        conn.close()
        print(f"Inserted {len(facts)} dog facts into the database.")
    else:
        print(f"API error: {response.status_code}")

def analyze_dog_facts():
    """
    Analyze the DogFacts table and write results to a text file.
    """
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM DogFacts')
    total_facts = cur.fetchone()[0]
    conn.close()

    with open('dog_facts_analysis.txt', 'w') as f:
        f.write("Dog Facts Analysis\n")
        f.write("===================\n")
        f.write(f"Total Dog Facts: {total_facts}\n")
    print("Dog facts analysis written to dog_facts_analysis.txt.")

def main():
    create_database()
    for _ in range(4):  # To get at least 100 cat facts
        fetch_cat_facts()
        time.sleep(1)  # To avoid hitting the API rate limit
    fetch_dog_breeds()

    fetch_dog_facts(limit=25)  # Fetch dog facts
    analyze_dog_facts()  # Analyze dog facts

if __name__ == '__main__':
    main()