import flask as fk
from flask import render_template, redirect, url_for, session, request
import logging

logging.basicConfig(level=logging.DEBUG)
app = fk.Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if(fk.request.method == "GET"):
        return render_template("home.html")
    else:
        return render_tempalte()

@app.route("/about", methods=["GET"])
def about():
    return "About page otw"

@app.route("/custom-match", methods=["GET", "POST"])
def custom_match():
    return "Custom match otw"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)