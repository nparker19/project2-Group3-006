from types import prepare_class
from flask.helpers import url_for
from werkzeug.utils import redirect
from app import app, db
from models import User_DB
import os
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
from flask import session, request
from functools import wraps
import flask
from flask_login import login_user, current_user, LoginManager
from flask_login.utils import login_required
from methods import (
    suggest,
    sortDictTimeRegular,
    convertScheduleToRegTime,
)

from createSchedule import creatSchedules
from checkConnection import checkConnect
from listSchedule import listSchedules

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    return User_DB.query.get(user_name)


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


# login required function for google authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get("profile", None)

        if user:
            return f(*args, **kwargs)
        return flask.redirect(flask.url_for("landingpage"))

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


@app.route("/")
@login_required
def hello_world():
    email = dict(session)["profile"]["email"]
    email_user = User_DB.query.filter_by(email=email).first()
    if email_user:
        pass
    else:
        email_user = User_DB(email=email)
        db.session.add(email_user)
        db.session.commit()

    return flask.render_template(
        "home.html",
        currentUserEmail=email_user,
    )


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


# This route accepts the unsorted schedule from the client and returns to the client a sorted schedule
@app.route("/sorting", methods=["POST"])
def sorting():
    errorMessage = []
    unsortedSchedule = flask.request.json.get("unsortedSchedule")
    try:
        convertedDict = convertScheduleToRegTime(unsortedSchedule)
        sortedSchedule = sortDictTimeRegular(convertedDict)
    except ValueError:
        errorMessage.append("Invalid Time entered.")
        return flask.jsonify({"message_server": errorMessage})

    return flask.jsonify(
        {
            "message_server": errorMessage,
            "server_sorted_Schedule": sortedSchedule,
        }
    )


# This route handles the fetch API most call for when the "receive suggestions" button is pressed.
@app.route("/suggestions", methods=["POST"])
def suggestions():
    """
    This method takes in a schedule dictionary and a suggestions dictionary from the client,
    and returns schedule suggestions to the client.
    """
    errorMessage = []
    scheduleDict = flask.request.json.get("scheduleDict")
    suggestDict = flask.request.json.get("suggestDict")
    try:
        suggestionsList = suggest(scheduleDict, suggestDict)
    except Exception as error:
        errorMessage.append(
            f"We were unable to retrieve your schedule suggestions. Error: {error}"
        )
        return flask.jsonify(
            {
                "message_server": errorMessage,
            }
        )
    return flask.jsonify(
        {
            "schedule_server": scheduleDict,
            "suggest_server": suggestDict,
            "suggestions_server": suggestionsList,
            "message_server": errorMessage,
        }
    )


@app.route("/complete", methods=["POST"])
def complete():
    errorMessage = []
    scheduleDate = flask.request.json.get("currentDate")
    scheduleDict = flask.request.json.get("scheduleDict")

    try:
        checkConnect()
        creatSchedules(scheduleDict)
    except Exception as error:
        errorMessage.append(
            f"Calendar was not successfully saved to google calendar. Error: {error}"
        )
        return flask.jsonify(
            {
                "message_server": errorMessage,
            }
        )
    return flask.jsonify(
        {"schedule_server": scheduleDict, "message_server": errorMessage}
    )


bp = flask.Blueprint("bp", __name__, template_folder="./build")





@bp.route("/index")
def index():
    """
    Renders the creat schedule page which allows the user to edit
    their current daily schedule, receive suggestions, and save to their google calendar
    """

    return flask.render_template("index.html")


app.register_blueprint(bp)


def addUserEmailDB(userEmail):
    email_user = User_DB.query.filter_by(email=userEmail).first()
    if email_user:
        pass
    else:
        new_email_user = User_DB(email=userEmail)
        db.session.add(new_email_user)
        db.session.commit()


if __name__ == "__main__":
    app.run(
        # host=os.getenv("IP", "0.0.0.0"),
        # port=int(os.getenv("PORT", "8080")),
        debug=True,
    )