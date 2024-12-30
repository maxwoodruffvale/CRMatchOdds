from joblib import load
from gatherMatches import deck_to_nums, get_battle_log
import requests
import numpy as np
model = load('randomForestMatchPredictor.joblib')

with open('apikey.txt', 'r') as f:
    API_TOKEN = f.readline()
BASE_URL = "https://api.clashroyale.com/v1"

def predict_team_odds(team1, team2):
    input_data = np.array(team1 + team2).reshape(1, -1)

    probabilities = model.predict_proba(input_data)

    odds_team1 = probabilities[0][0]  # Probability of class '1'
    odds_team2 = probabilities[0][1]  # Probability of class '0'

    return odds_team1

def get_recent_matches_odds(player_tag):
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

team1 = [11, 22, 33, 44, 55, 66, 77, 88]  # Example players for Team 1
team2 = [99, 88, 77, 66, 55, 44, 33, 22]  # Example players for Team 2

#sort of a counter but 2.6 is goated
d1 = ["Knight", "Magic Archer", "Goblin Drill", "The Log", "Tornado", "Ice Spirit", "Skeletons", "Cannon"]
d2 = ["Musketeer", "Skeletons", "The Log", "Fireball", "Ice Spirit", "Cannon", "Hog Rirder", "Ice Golem"]

#really good deck and really buns deck
d1 = ["Goblin Barrel", "Royal Recruits", "Goblinstein", "Cannon Cart", "Goblin Gang", "Dart Goblin", "Arrows", "Cannon"]
d2 = ["Elixir Collector", "Barbarian Hut", "Lightning", "Musketeer", "Zap", "Heal Spirit", "Goblin Machine", "Knight"]
d1 = deck_to_nums(d1)
d2 = deck_to_nums(d2)
#predict_team_odds(d1, d2)
player_id="#2QLYJYPJ"

with requests.Session() as session:
    session.headers.update({"Authorization": f"Bearer {API_TOKEN}"})
    battle_log = get_battle_log(session, player_id)
    for battle in battle_log:
        winner = int(battle["team"][0]["crowns"] < battle["opponent"][0]["crowns"])
        player_deck = [card["name"] for card in battle["team"][0]["cards"]]
        opponent_deck =  [card["name"] for card in battle["opponent"][0]["cards"]]

        d1 = deck_to_nums(player_deck)
        d2 = deck_to_nums(opponent_deck)

        odds = predict_team_odds(d1, d2)

        opponent_name = battle["opponent"][0].get("name")
        player_name = battle["team"][0].get("name")
        print("Winner: " + ("player" if winner==0 else "opponent"))
        print("Odds: " + str(odds))
        st = "-"*int(odds*40)
        st = st + ","*int((1-odds)*40)
        print(st)
        for i in range(4):
            print((player_deck[2*i].ljust(12) + "  " + player_deck[2*i + 1]).ljust(35) + "  -  " + opponent_deck[2*i].ljust(12) + "  " + opponent_deck[2*i + 1])
        # first winner is player, 0 = player win, 1 = opponent win
        #print(battle["team"][0]["cards"][0]) <-- HAS LINKS TO IMAGES FOR FUTURE REFERENCE
        print("\n")