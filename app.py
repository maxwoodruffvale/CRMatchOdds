import flask as fk
from flask import render_template, redirect, url_for, session, request, make_response
import logging
from interact import get_recent_matches_and_odds
import math

import sys
print(sys.executable)

logging.basicConfig(level=logging.DEBUG)
app = fk.Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    previous_tag = request.cookies.get('tag')


    if(fk.request.method == "GET"):
        if(previous_tag):
            matches = get_recent_matches_and_odds("#" + previous_tag)
            return render_template("home.html", match_data = matches)
        else:
            return render_template("home.html")
    else:
        tag = request.form.get('tag')
        save = request.form.get('save')
        matches = get_recent_matches_and_odds("#" + tag)
        response = make_response(render_template('home.html', match_data=matches))
        if(save=="on"):
            response.set_cookie('tag', tag)
            print("save it")
        
        return(response)
        #return render_template("home.html", match_data = matches)

        #        response = make_response(render_template_string(template, previous_input=user_input))
        #         response.set_cookie('user_input', user_input)
        #    previous_input = request.cookies.get('user_input')


@app.route("/about", methods=["GET"])
def about():
    return "About page otw"

@app.route("/custom-match", methods=["GET", "POST"])
def custom_match():
    return "Custom matches coming soon"

@app.template_filter('floor')
def floor_filter(value):
    return math.floor(value)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)