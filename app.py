import flask as fk
from flask import render_template, redirect, url_for, session, request, make_response
from interactRF import get_recent_matches_and_odds, get_recent_matches_key, predict_team_odds
import math

import sys
print(sys.executable)

app = fk.Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    previous_tag = request.cookies.get('tag')
    previous_key = request.cookies.get('key')
    if(fk.request.method == "GET"):
        if(previous_tag and previous_key):
            matches = get_recent_matches_key("#" + previous_tag, previous_key)
            return render_template("home.html", match_data = matches)
        else:
            return render_template("home.html")
    else:
        key = request.form.get('key')
        if(key == "" and previous_key):
            key = previous_key
        tag = request.form.get('tag')
        save = request.form.get('save')
        matches = get_recent_matches_key("#" + tag, key)
        response = make_response(render_template('home.html', match_data=matches))
        if(save=="on"):
            response.set_cookie('tag', tag)
            response.set_cookie('key', key)
        return(response)

@app.route("/about", methods=["GET"])
def about():
    return "About page otw"

@app.route("/custom-match", methods=["GET", "POST"])
def custom_match():
    if(fk.request.method == "GET"):
        with open("card_imgs.csv", "r") as file:
            card_imgs = file.readlines()
        card_imgs = [line.strip().split(',') for line in card_imgs]
        return render_template("custommatch.html", card_imgs=card_imgs)
    else:
        player_cards=request.form.get('playerCards').split(',')
        opp_cards=request.form.get('enemyCards').split(',')
        print(player_cards)
        print(opp_cards)
        with open("card_imgs.csv", "r") as file:
            card_imgs = file.readlines()
        card_imgs = [line.strip().split(',') for line in card_imgs]

        player_card_imgs = [card_imgs[int(card)][2] for card in player_cards]
        opp_card_imgs = [card_imgs[int(card)][2] for card in opp_cards]

        player_cards = [int(card) for card in player_cards]
        opp_cards = [int(card) for card in opp_cards]
        player_cards.sort()
        opp_cards.sort()

        odds = predict_team_odds(player_cards, opp_cards)
        return render_template("custommatchresults.html", odds=odds, player_cards=player_cards, opp_cards=opp_cards, player_card_imgs=player_card_imgs, opp_card_imgs=opp_card_imgs)

@app.route("/howto", methods=["GET"])
def howto():
    return render_template("howto.html")

@app.template_filter('floor')
def floor_filter(value):
    return math.floor(value)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)