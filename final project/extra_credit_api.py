import requests
import sqlite3

def create_database():
    """
    Create the necessary tables in the database.
    """
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS PonyCharacters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            alias TEXT,
            residence TEXT,
            occupation TEXT,
            kind TEXT,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_pony_characters(limit=100):
    """
    Fetch 100 pony characters from the Pony API and store them in the database.
    """
    url = f"https://ponyapi.net/v1/character/all?limit={limit}"
    response = requests.get(url)
    print(f"API Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json().get('data', [])
        print(f"Fetched {len(data)} characters from the API.")
        conn = sqlite3.connect('final_project_databases.db')
        cur = conn.cursor()
        inserted_count = 0
        for character in data:
            name = character.get('name')
            alias = character.get('alias')
            residence = character.get('residence')
            occupation = character.get('occupation')
            kind = ', '.join(character.get('kind', []))
            image_url = character.get('image', [None])[0]
            try:
                cur.execute('''
                    INSERT OR IGNORE INTO PonyCharacters (name, alias, residence, occupation, kind, image_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, alias, residence, occupation, kind, image_url))
                inserted_count += 1
            except sqlite3.IntegrityError as e:
                print(f"Duplicate entry for character {name}: {e}")
                continue
        conn.commit()
        conn.close()
        print(f"Inserted {inserted_count} new pony characters into the database.")
    else:
        print(f"API error: {response.status_code}")

def verify_pony_characters_table():
    """
    Verify the contents of the PonyCharacters table.
    """
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM PonyCharacters')
    rows = cur.fetchall()
    conn.close()
    print(f"Total rows in PonyCharacters table: {len(rows)}")
    for row in rows:
        print(row)

def analyze_pony_characters():
    """
    Analyze the PonyCharacters table and write results to a text file.
    """
    conn = sqlite3.connect('final_project_databases.db')
    cur = conn.cursor()
    cur.execute('SELECT name, alias, residence, occupation, kind FROM PonyCharacters')
    data = cur.fetchall()
    conn.close()

    with open('pony_analysis.txt', 'w') as f:
        f.write("Pony Characters Analysis\n")
        f.write("=========================\n")
        for row in data:
            f.write(f"Name: {row[0]}, Alias: {row[1]}, Residence: {row[2]}, Occupation: {row[3]}, Kind: {row[4]}\n")
    print("Pony characters analysis written to pony_analysis.txt.")

def main():
    create_database()  # Create the database and table if they don't exist
    fetch_pony_characters(limit=100)  # Fetch 100 pony characters at once
    analyze_pony_characters()  # Analyze the pony characters
    verify_pony_characters_table()  # Verify the table contents

if __name__ == "__main__":
    main()