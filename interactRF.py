from joblib import load
from gatherMatches import deck_to_nums, get_battle_log
import requests
import numpy as np
import os

model = load('randomForestMatchPredictor.joblib')

#API_TOKEN = os.getenv('API_KEY')
with open('apikey.txt', 'r') as f:
    API_TOKEN = f.readline()
BASE_URL = "https://api.clashroyale.com/v1"

def predict_team_odds(team1, team2):
    input_data = np.array(team1 + team2).reshape(1, -1)

    probabilities = model.predict_proba(input_data)

    odds_team1 = probabilities[0][0]  # Probability of class '1'
    odds_team2 = probabilities[0][1]  # Probability of class '0'

    return odds_team1

def get_recent_matches(player_tag):
    sanitized_tag = player_tag.lstrip("#")
    url = f"{BASE_URL}/players/%23{sanitized_tag}/battlelog" 

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()

    print(f"Error fetching battle log for {player_tag}: {response.status_code} {response.text}")
    return []

def get_recent_matches_and_odds(player_tag):
    with requests.Session() as session:
        session.headers.update({"Authorization": f"Bearer {API_TOKEN}"})
        battle_log = get_battle_log(session, player_tag)
        matches_data = []
        for battle in battle_log:
            winner = int(battle["team"][0]["crowns"] < battle["opponent"][0]["crowns"])
            winner_color = "blue" if winner == 0 else "red"
            crowns = [battle["team"][0]["crowns"], battle["opponent"][0]["crowns"]]

            player_deck_names = [card["name"] for card in battle["team"][0]["cards"]]
            opponent_deck_names =  [card["name"] for card in battle["opponent"][0]["cards"]]
            player_deck_imgs = [card["iconUrls"]["medium"] for card in battle["team"][0]["cards"]]
            opponent_deck_imgs = [card["iconUrls"]["medium"] for card in battle["opponent"][0]["cards"]]

            d1 = deck_to_nums(player_deck_names)
            d2 = deck_to_nums(opponent_deck_names)

            odds = predict_team_odds(d1, d2)

            opponent_name = battle["opponent"][0].get("name")
            player_name = battle["team"][0].get("name")
            
            battle_data = {
                'winner':winner,
                'winner_color':winner_color,
                'crowns':crowns,
                'player_deck_names':player_deck_names,
                'opponent_deck_names':opponent_deck_names,
                'player_deck_imgs':player_deck_imgs,
                'opponent_deck_imgs':opponent_deck_imgs,
                'odds':odds,
                'opponent_name':opponent_name,
                'player_name':player_name
            }
            matches_data.append(battle_data)
            
        return matches_data

def get_recent_matches_key(player_tag, key):
    with requests.Session() as session:
        session.headers.update({"Authorization": f"Bearer {key}"})
        battle_log = get_battle_log(session, player_tag)
        matches_data = []
        for battle in battle_log:
            winner = int(battle["team"][0]["crowns"] < battle["opponent"][0]["crowns"])
            winner_color = "blue" if winner == 0 else "red"
            crowns = [battle["team"][0]["crowns"], battle["opponent"][0]["crowns"]]

            player_deck_names = [card["name"] for card in battle["team"][0]["cards"]]
            opponent_deck_names =  [card["name"] for card in battle["opponent"][0]["cards"]]
            player_deck_imgs = [card["iconUrls"]["medium"] for card in battle["team"][0]["cards"]]
            opponent_deck_imgs = [card["iconUrls"]["medium"] for card in battle["opponent"][0]["cards"]]

            d1 = deck_to_nums(player_deck_names)
            d2 = deck_to_nums(opponent_deck_names)

            odds = predict_team_odds(d1, d2)

            opponent_name = battle["opponent"][0].get("name")
            player_name = battle["team"][0].get("name")
            
            battle_data = {
                'winner':winner,
                'winner_color':winner_color,
                'crowns':crowns,
                'player_deck_names':player_deck_names,
                'opponent_deck_names':opponent_deck_names,
                'player_deck_imgs':player_deck_imgs,
                'opponent_deck_imgs':opponent_deck_imgs,
                'odds':odds,
                'opponent_name':opponent_name,
                'player_name':player_name
            }
            matches_data.append(battle_data)
            
        return matches_data