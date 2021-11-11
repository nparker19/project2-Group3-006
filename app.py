<<<<<<< HEAD
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
=======
import flask
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = flask.Flask(__name__, static_folder="./build/static")
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b"I am a secret key!"
db = SQLAlchemy(app)
>>>>>>> 3e97b34fdfe07a90c001e264da531b16cdeb6793
