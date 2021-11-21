from flask.helpers import url_for
from werkzeug.utils import redirect
from app import app, db
from models import User
import os
from authlib.integrations.flask_client import OAuth
from datetime import timedelta, datetime
from flask import session, request
from functools import wraps
import flask
from flask_login import login_user, current_user, LoginManager
from flask_login.utils import login_required
from methods import suggest, sortDictTimeMilitary, sortDictTimeRegular
import json

from createSchedule import creatSchedules
from checkConnection import checkConnect

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)


@app.route("/landingpage")
def landingpage():
    return flask.render_template("landingpage.html")


@app.route("/functionality")
def functionality():
    return flask.render_template("functionality.html")


@app.route("/purpose")
def purpose():
    return flask.render_template("purpose.html")


@app.route("/contact")
def contact():
    return flask.render_template("contact.html")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        pass
    else:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    return flask.redirect(flask.url_for("login"))


# login required function for google authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get("profile", None)

        if user:
            return f(*args, **kwargs)
        return flask.redirect(flask.url_for("login"))

    return decorated_function


app.config["SESSION_COOKIE_NAME"] = "google-login-session"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)


oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
    client_kwargs={"scope": "openid email profile"},
)


@app.route("/authorize")
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()
    user = oauth.google.userinfo()
    session["profile"] = user_info
    session.permanent = True
    return redirect("/")


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("index"))

    else:
        return flask.jsonify({"status": 401, "reason": "Username or Password Error"})


@app.route("/")
@login_required
def hello_world():
    email = dict(session)["profile"]["email"]
    email_user = User.query.filter_by(email=email).first()
    if email_user:
        pass
    else:
        email_user = User(email=email)
        db.session.add(email_user)
        db.session.commit()
    return flask.render_template("home.html", currentUserEmail=email_user)


@app.route("/login/google")
def google_login():
    google = oauth.create_client("google")
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/")
@login_required
def main():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("/"))  # redirect to next page.
    return flask.redirect(flask.url_for("login"))


@app.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("landingpage")


# This route will handle the fetch API Post call from the create schedule page
@app.route("/suggestions", methods=["POST"])
def suggestions():

    scheduleDict = flask.request.json.get("scheduleDict")
    suggestDict = flask.request.json.get("suggestDict")
    message = []
    militaryTime = False
    try:
        scheduleDict = sortDictTimeRegular(scheduleDict)
    except ValueError:
        try:
            militaryTime = True
            scheduleDict = sortDictTimeMilitary(scheduleDict)
        except:
            message = ["Invalid time entered"]
            return flask.jsonify(
                {
                    "schedule_server": scheduleDict,
                    "suggest_server": suggestDict,
                    "message_server": message,
                }
            )
    message = ["success"]
    return flask.jsonify(
        {
            "schedule_server": scheduleDict,
            "suggest_server": suggestDict,
            "message_server": message,
        }
    )


@app.route("/complete", methods=["POST"])
def complete():
    militaryTime = True
    scheduleDate = flask.request.json.get("currentDate")
    scheduleDict = flask.request.json.get("scheduleDict")
    try:
        scheduleDict = sortDictTimeMilitary(scheduleDict)
    except ValueError:
        try:
            checkConnect()
            creatSchedules(scheduleDict)
        except KeyError:
            pass

    return flask.jsonify({"schedule_server": scheduleDict})


bp = flask.Blueprint("bp", __name__, template_folder="./build")


@bp.route("/index")
def index():
    """
    Renders the creat schedule page which allows the user to edit
    their current daily schedule, receive suggestions, and save to their google calendar
    """

    return flask.render_template("index.html")


app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(
        # host=os.getenv("IP", "0.0.0.0"),
        # port=int(os.getenv("PORT", "8080")),
        debug=True,
    )
