import requests
import csv

with open('apikey.txt', 'r') as f:
    API_TOKEN = f.readline()
BASE_URL = "https://api.clashroyale.com/v1"


def get_all_cards():
    url = f"{BASE_URL}/cards"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}

cards = get_all_cards()
card_names = [card['name'] for card in cards]

def card_to_num(card_name):
    for i, name in enumerate(card_names):
        if name == card_name:
            return i
    return -1

def num_to_card(num):
    return card_names[num]

def deck_to_nums(deck):
    cards = [card_to_num(card) for card in deck]
    cards.sort()
    return cards

def get_battle_log(session, player_tag):
    sanitized_tag = player_tag.lstrip("#")
    url = f"{BASE_URL}/players/%23{sanitized_tag}/battlelog" 
    response = session.get(url)
    
    if response.status_code == 200:
        return response.json()

    print(f"Error fetching battle log for {player_tag}: {response.status_code} {response.text}")
    return []

def extract_matches(limit):
    print("extracting matches")
    matches = []
    player_queue = ["#C0V0UQ9UY"]
    processed_players = set()

    with requests.Session() as session:
        session.headers.update({"Authorization": f"Bearer {API_TOKEN}"})

        output_file = "matches.csv"
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            header = ['Winner'] + [f'P{i+1}' for i in range(8)] + [f'O{i+1}' for i in range(8)]
            writer.writerow(header)

            while(player_queue):
                if(len(matches) >= limit):
                        break
                
                player = player_queue.pop(0)
                if player in processed_players:
                    continue
                processed_players.add(player)

                battle_log = get_battle_log(session, player)
                for battle in battle_log:
                    if battle.get('type') != "pathOfLegend":
                        continue

                    match_data = {
                        "winner": int(battle["team"][0]["crowns"] < battle["opponent"][0]["crowns"]),
                        "player_deck": [card_to_num(card["name"]) for card in battle["team"][0]["cards"]],
                        "opponent_deck": [card_to_num(card["name"]) for card in battle["opponent"][0]["cards"]],
                    }

                    # first winner is player, 0 = player win, 1 = opponent win
                    #print(battle["team"][0]["cards"][0]) #<-- HAS LINKS TO IMAGES FOR FUTURE REFERENCE

                    matches.append(match_data)

                    if(len(matches) % 100 == 0): print(f'{len(matches):10}')
                    if(len(matches) >= limit):
                        break

                    player_queue.append(battle["opponent"][0].get("tag"))
                    
                    player_deck = match_data['player_deck']
                    player_deck.sort()
                    opponent_deck = match_data['opponent_deck']
                    opponent_deck.sort()
                    row = [match_data['winner']] + player_deck + opponent_deck

                    writer.writerow(row)
    return matches
#131.215.220.164