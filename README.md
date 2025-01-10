# Clash Royale Match Predictions Using Random Forest

Program to predict the odds of you winning a clash royale game based on your deck. Predictions are made using a random forest model trained on 1,000,000+ games of clash royale.

![alt text](https://github.com/maxwoodruffvale/CRMatchOdds/blob/main/matchupRoyaleHome.png?raw=true)

## Installation

1. Clone this repository
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.
```bash
pip install -r requirements.txt
```

## Usage

To view in web:

```bash
flask run
```

Alternatively, in interactRF.py, add this code to the end to set up a custom matchup:

```python
d1 = ["Goblin Barrel", "Royal Recruits", "Goblinstein", "Cannon Cart", "Goblin Gang", "Dart Goblin", "Arrows", "Cannon"]
d2 = ["Elixir Collector", "Barbarian Hut", "Lightning", "Musketeer", "Zap", "Heal Spirit", "Goblin Machine", "Knight"]
d1 = deck_to_nums(d1)
d2 = deck_to_nums(d2)
print(predict_team_odds(d1, d2))
```

