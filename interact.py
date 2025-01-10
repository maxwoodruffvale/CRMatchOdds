from joblib import load
from gatherMatches import deck_to_nums, get_battle_log
import requests
import numpy as np
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim

class PredictorNN(nn.Module):
    def __init__(self, input_size):
        super(PredictorNN, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

device = torch.device('cpu')

data = pd.read_csv("matches1M.csv")
X = data.iloc[:, 1:].values
scaler = StandardScaler()
X = scaler.fit_transform(X)

model = PredictorNN(16).to(device)

model.load_state_dict(torch.load("predictor_model.pth", map_location=device))
model.eval()  

API_TOKEN = os.getenv('API_KEY')
BASE_URL = "https://api.clashroyale.com/v1"

def predict_team_odds(team1, team2):
    input_data = np.array(team1 + team2).reshape(1, -1)

    probabilities = model.predict_proba(input_data)

    odds_team1 = probabilities[0][0]  # Probability of class '1'
    odds_team2 = probabilities[0][1]  # Probability of class '0'

    return odds_team1

def predict_odds_nn(team1, team2):
    input_data = np.array(team1 + team2).reshape(1, -1)
    input_data = scaler.transform(input_data)
    input_tensor = torch.tensor(input_data, dtype=torch.float32).to(device)
    with torch.no_grad():
        probability = model(input_tensor).item()
    return 1.0 - probability

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

            odds = predict_odds_nn(d1, d2)

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

"""
example of very bad matchup
d1 = ["Goblin Barrel", "Royal Recruits", "Goblinstein", "Cannon Cart", "Goblin Gang", "Dart Goblin", "Arrows", "Cannon"]
d2 = ["Elixir Collector", "Barbarian Hut", "Lightning", "Musketeer", "Zap", "Heal Spirit", "Goblin Machine", "Knight"]
d1 = deck_to_nums(d1)
d2 = deck_to_nums(d2)
print(predict_odds_nn(d1, d2))
"""