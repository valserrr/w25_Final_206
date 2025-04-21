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

def main():
    create_database()
    for _ in range(4):  # To get at least 100 cat facts
        fetch_cat_facts()
        time.sleep(1)  # To avoid hitting the API rate limit
    fetch_dog_breeds()
    fetch_bored_activities()
    analyze_bored_activities()

#Extra Credit API: Bored API
def fetch_bored_activities():
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS BoredActivities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity TEXT UNIQUE,
            type TEXT,
            participants INTEGER,
            price REAL,
            accessibility REAL
        )
    ''')
    # Fetch up to 25 new activities
    count = 0
    while count < 25:
        response = requests.get("https://www.boredapi.com/api/activity/")
        if response.status_code == 200:
            data = response.json()
            try:
                cur.execute('''
                    INSERT OR IGNORE INTO BoredActivities (activity, type, participants, price, accessibility)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    data.get("activity"),
                    data.get("type"),
                    data.get("participants"),
                    data.get("price"),
                    data.get("accessibility")
                ))
                conn.commit()
                count += 1
                time.sleep(0.1)  # Be nice to the API
            except Exception as e:
                print("Error inserting:", e)
        else:
            print("API error:", response.status_code)
            break

    conn.close()

def analyze_bored_activities():
    """Analyze the BoredActivities table and write results to a text file."""
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('''
            SELECT type, COUNT(*) as count
            FROM BoredActivities
            GROUP BY type
        ''')
    data = cur.fetchall()
    conn.close()
    
    with open('bored_analysis.txt', 'w') as f:
            f.write("Bored Activities Analysis\n")
            f.write("==========================\n")
            for row in data:
                f.write(f"Type: {row[0]}, Count: {row[1]}\n")
    
    def fetch_bored_activities():
        conn = sqlite3.connect('final_project_databases.db')
        cur = conn.cursor()
    
        # Create table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS BoredActivities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity TEXT UNIQUE,
                type TEXT,
                participants INTEGER,
                price REAL,
                accessibility REAL
            )
        ''')
        # Fetch up to 25 new activities
        count = 0
        retries = 3  # Number of retries for API errors
        while count < 25:
            try:
                response = requests.get("https://www.boredapi.com/api/activity/")
                if response.status_code == 200:
                    data = response.json()
                    cur.execute('''
                        INSERT OR IGNORE INTO BoredActivities (activity, type, participants, price, accessibility)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        data.get("activity"),
                        data.get("type"),
                        data.get("participants"),
                        data.get("price"),
                        data.get("accessibility")
                    ))
                    conn.commit()
                    count += 1
                    time.sleep(0.1)  # Be nice to the API
                else:
                    print(f"API error: {response.status_code}. Retrying...")
                    retries -= 1
                    if retries == 0:
                        print("Max retries reached. Exiting.")
                        break
                    time.sleep(2)  # Wait before retrying
            except Exception as e:
                print("Error inserting:", e)
                break
    
        conn.close()
        print("Bored activities analysis written to bored_analysis.txt.")

if __name__ == '__main__':
    main()