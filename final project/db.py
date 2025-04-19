from bs4 import BeautifulSoup
import requests

def get_popular_game_ids(limit=25):
    """Scrape popular game IDs from the Roblox Discover page."""
    url = 'https://www.roblox.com/discover'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            game_links = soup.find_all('a', class_='game-card-link')
            game_ids = set()
            for link in game_links:
                href = link.get('href')
                if href and '/games/' in href:
                    try:
                        game_id = int(href.split('/games/')[1].split('/')[0])
                        game_ids.add(game_id)
                    except ValueError:
                        continue
                if len(game_ids) >= limit:
                    break
            print(f"Fetched Game IDs: {list(game_ids)}")
            return list(game_ids)
        else:
            print("Failed to fetch game IDs, status code:", response.status_code)
            return []

    except Exception as e:
        print("Error fetching popular games:", e)
        return []

# Example usage:
game_ids = get_popular_game_ids(limit=25)
print(game_ids)

