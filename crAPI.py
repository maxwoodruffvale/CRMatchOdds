import requests
key=""
with open('apikey.txt', 'r') as f:
    key = f.readline()
API_TOKEN = key
BASE_URL = "https://api.clashroyale.com/v1"

def get_battle_log(player_tag):
    sanitized_tag = player_tag.lstrip("#")
    url = f"{BASE_URL}/players/%23{sanitized_tag}/battlelog" 
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching battle log for {player_tag}: {response.status_code} {response.text}")
        return []

def extract_matches(limit):
    print("extracting matches")
    matches = []
    player_queue = ["#C0V0UQ9UY"]

    while(player_queue):
        player = player_queue.pop()
        battle_log = get_battle_log(player)
        for battle in battle_log:
            if battle.get('type') != "pathOfLegend":
                continue

            match_data = {
                "winner": "player" if battle["team"][0]["crowns"] > battle["opponent"][0]["crowns"] else "opponent",
                "player_deck": [card["name"] for card in battle["team"][0]["cards"]],
                "opponent_deck": [card["name"] for card in battle["opponent"][0]["cards"]],
            }

            matches.append(match_data)
            if(len(matches) >= limit):
                return matches

            opponent_tag = battle["opponent"][0].get("tag")
            if(opponent_tag):
                player_queue.append(opponent_tag)
    
    return matches

all_matches = extract_matches(1000)

for i, match in enumerate(all_matches, start=1):
    print(f"Match {i}:")
    print(f"  Winner: {match['winner']}")
    print(f"  Player Deck: {', '.join(match['player_deck'])}")
    print(f"  Opponent Deck: {', '.join(match['opponent_deck'])}")
    print()