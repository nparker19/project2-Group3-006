import flask
import requests
import os
import json
from flask import Flask, render_template


app = flask.Flask(__name__, static_folder="./build/static")


@app.route("/")
def home():
    return render_template("home.html")


# This route will handle the fetch API Post call from the new schedule html
@app.route("/suggest", methods=["POST"])
def suggest():
    pass


bp = flask.Blueprint("bp", __name__, template_folder="./build")


@bp.route("/index")
def index():
    """
    Create schedule page which allows the user to edit
    their current daily schedule and save to their google calendar
    """

    return flask.render_template("index.html")


app.register_blueprint(bp)

app.run()
