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
    # Execute the SQL command to create the table
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
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

def fetch_pony_characters(limit=25):
    """
    Fetch pony characters from the Pony API and store them in the database.
    :param limit: The number of characters to fetch.
    """
    # Construct the API request URL with the specified limit
    url = f"https://ponyapi.net/v1/character/all?limit={limit}"
    # Make the API request
    response = requests.get(url)
    # Debugging: Print the API response status code
    print(f"API Response Status Code: {response.status_code}")

    # Check if the API request was successful
    if response.status_code == 200:
        # Parse the JSON response data
        data = response.json()
        # Extract the list of character dictionaries from the response data
        characters = data.get('data', [])
        # Debugging: Print the number of characters fetched
        print(f"Fetched {len(characters)} characters from the API.")

        # Connect to the SQLite database
        conn = sqlite3.connect('final_project_databases.db')
        # Create a cursor object to interact with the database
        cur = conn.cursor()
        # Initialize a counter for the number of characters inserted into the database
        inserted_count = 0

        # Iterate over each character in the list
        for character in characters:
            # Extract the character's name
            name = character.get('name')
            # Extract the character's alias
            alias = character.get('alias')
            # Extract the character's residence
            residence = character.get('residence')
            # Extract the character's occupation
            occupation = character.get('occupation')
            # Join the character's kinds into a single string
            kind = ', '.join(character.get('kind', []))
            # Extract the first image URL from the list of image URLs
            image_url = character.get('image', [None])[0]

            # Debugging: Print the character being processed
            print(f"Inserting character: {name}, Alias: {alias}, Residence: {residence}, Occupation: {occupation}, Kind: {kind}, Image URL: {image_url}")

            try:
                # Insert the character into the PonyCharacters table
                cur.execute('''
                    INSERT OR IGNORE INTO PonyCharacters (name, alias, residence, occupation, kind, image_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, alias, residence, occupation, kind, image_url))
                # Increment the counter for the number of characters inserted
                inserted_count += 1
            except sqlite3.IntegrityError as e:
                # Print an error message if there was an IntegrityError
                print(f"IntegrityError for character {name}: {e}")
                # Skip the current character
                continue

        # Commit the changes to the database
        conn.commit()
        # Close the connection to the database
        conn.close()
        # Print the number of characters inserted
        print(f"Inserted {inserted_count} new pony characters into the database.")
    else:
        # Print an error message if the API request was not successful
        print(f"API error: {response.status_code}")

def verify_pony_characters_table():
    """
    Verify the contents of the PonyCharacters table.
    """
    # Connect to the database
    conn = sqlite3.connect('final_project_databases.db')
    # Create a cursor object
    cur = conn.cursor()
    # Execute a SELECT statement to retrieve all rows from the PonyCharacters table
    cur.execute('SELECT * FROM PonyCharacters')
    # Fetch all rows from the result set
    rows = cur.fetchall()
    # Close the connection to the database
    conn.close()
    # Print the total number of rows in the PonyCharacters table
    print(f"Total rows in PonyCharacters table: {len(rows)}")
    # Iterate through each row in the result set
    for row in rows:
        # Print the row
        print(row)

def analyze_pony_characters():
    """
    Analyze the PonyCharacters table and write results to a text file.
    """
    # Connect to the database
    conn = sqlite3.connect('final_project_databases.db')
    # Create a cursor object
    cur = conn.cursor()
    # Execute a query to select all data from the PonyCharacters table
    cur.execute('SELECT name, alias, residence, occupation, kind FROM PonyCharacters')
    # Fetch all the data from the query
    data = cur.fetchall()
    # Close the connection
    conn.close()

    # Open a text file to write the results
    with open('pony_analysis.txt', 'w') as f:
        # Write the title of the analysis
        f.write("Pony Characters Analysis\n")
        # Write a separator line
        f.write("=========================\n")
        # Loop through each row of data
        for row in data:
            # Write the data to the file
            f.write(f"Name: {row[0]}, Alias: {row[1]}, Residence: {row[2]}, Occupation: {row[3]}, Kind: {row[4]}\n")
    # Print a message to indicate that the analysis has been written to the file
    print("Pony characters analysis written to pony_analysis.txt.")

def check_table_schema():
    """
    Check the schema of the PonyCharacters table.
    """
    # Connect to the database
    conn = sqlite3.connect('final_project_databases.db')
    # Create a cursor object
    cur = conn.cursor()
    # Execute a query to get the schema of the table
    cur.execute("PRAGMA table_info(PonyCharacters)")
    # Fetch all the results
    schema = cur.fetchall()
    # Close the connection
    conn.close()
    # Print the schema of the table
    print("PonyCharacters Table Schema:")
    for column in schema:
        print(column)

def main():
    create_database()  # Create a new database
    check_table_schema()  # Debugging: Check table schema
    fetch_pony_characters(limit=10)  # Fetch 10 pony characters
    analyze_pony_characters()  # Analyze the pony characters
    verify_pony_characters_table()  # Debugging: Verify table contents

if __name__ == "__main__":
    main()