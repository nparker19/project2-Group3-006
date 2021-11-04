import flask
import requests
import os
from flask import Flask, render_template

app = flask.Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

app.run()