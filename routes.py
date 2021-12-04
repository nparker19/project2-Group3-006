"""
this script is the central to the app and calls major functions
in other part of the entire application. The route and html rendering
are defined here
"""

from datetime import timedelta
from functools import wraps
from operator import truediv
from types import prepare_class
import os
from flask import session
from flask.helpers import url_for
from werkzeug.utils import redirect
import flask
from flask_login import current_user, LoginManager
from flask_login.utils import login_required
from authlib.integrations.flask_client import OAuth
from models import User_DB
from app import app, db

from methods import (
    suggest_generator,
    sort_dict_time_regular,
    convert_schedule_to_reg_time,
)


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_name):
    """
    function load user and query db for user
    """
    return User_DB.query.get(user_name)

@app.route("/landingpage")
def landingpage():
    """
    function direction route to the landingpage of app
    """
    return flask.render_template("landingpage.html")

@app.route("/functionality")
def functionality():
    """
    function direction route to the functionality html of app
    """
    return flask.render_template("functionality.html")

@app.route("/purpose")
def purpose():
    """
    function direction route to the purpose html of app
    """
    return flask.render_template("purpose.html")

@app.route("/contact")
def contact():
    """
    function direction route to the contact html of app
    """
    return flask.render_template("contact.html")

@app.route("/signup")
def signup():
    """
    function define signup and route to signup html
    """
    return flask.render_template("signup.html")

# #disable pylint
# routes.py:74:0: E0102: function already defined line 14 (function-redefined)
# routes.py:74:0: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)

# login required function for google authentication
def login_required(f):
    """
    This function define login and direct route to landing page
    """
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
    OAUTHLIB_INSECURE_TRANSPORT=os.getenv("OAUTHLIB_INSECURE_TRANSPORT"),
    OAUTHLIB_STRICT_TOKEN_TYPE="Bearer",
)

# W0621: Redefining name 'google' from outer scope (line 92)
# (redefined-outer-name)
# routes.py:116:4: E0237: Assigning to attribute 'permanent'
# not defined in class slots (assigning-non-slot)
# routes.py:139:8: E1101: Instance of 'scoped_session' has
# no 'add' member (no-member)
# routes.py:140:8: E1101: Instance of 'scoped_session' has
# no 'commit' member (no-member)

@app.route("/authorize")
def authorize():
    """
    This method handle the user google autherization
    """
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
    """
    This method direct route to login html
    """
    return flask.render_template("login.html")

@app.route("/")
@login_required
def hello_world():
    """
    This method handles query for user
    and direct user to home page
    """
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
    """
    This method direct route to to authorization method
    log-in users
    """
    google = oauth.create_client("google")
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/")
@login_required
def main():
    """
    This method take in schedule dictionary and return dict to server
    """
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("/"))  # redirect to next page.
    return flask.redirect(flask.url_for("login"))

@app.route("/logout")
def logout():
    """
    This method directs user to landingpage
    """
    for key in list(session.keys()):
        session.pop(key)
    return redirect("landingpage")


@app.route("/sorting", methods=["POST"])
def sorting():
    """
    This route accepts the unsorted schedule from the client
    and returns to the client a sorted schedule
    """
    errorMessage = []
    unsortedSchedule = flask.request.json.get("unsortedSchedule")
    try:
        convertedDict = convert_schedule_to_reg_time(unsortedSchedule)
        sortedSchedule = sort_dict_time_regular(convertedDict)
    except ValueError:
        errorMessage.append("Invalid Time entered.")
        return flask.jsonify({"message_server": errorMessage})

    return flask.jsonify(
        {
            "message_server": errorMessage,
            "server_sorted_schedule": sortedSchedule,
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
    scheduleDict= flask.request.json.get("scheduleDict")
    suggestDict = flask.request.json.get("suggestDict")
    try:
        suggestionsList = suggest_generator(scheduleDict, suggestDict)
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

# disable pylint
# routes.py:211:11: W0703: Catching too general exception Exception (broad-except)
# routes.py:241:11: W0703: Catching too general exception Exception (broad-except)
# routes.py:264:0: C0103: Argument name "userEmail"
# doesn't conform to snake_case naming style (invalid-name)
# routes.py:273:8: E1101: Instance of 'scoped_session' has no 'add' member (no-member)
# routes.py:274:8: E1101: Instance of 'scoped_session' has no 'commit' member (no-member)

bp = flask.Blueprint("bp", __name__, template_folder="./build")

@bp.route("/index")
def index():
    """
    Renders the create schedule page which allows the user to edit
    their current daily schedule, receive suggestions, and save to their google calendar
    """
    return flask.render_template("index.html")
app.register_blueprint(bp)


def add_user_email(user_email):
    email_user = User_DB.query.filter_by(email=user_email).first()
    if email_user:
        pass
    else:
        new_email_user = User_DB(email=user_email)
        db.session.add(new_email_user)
        db.session.commit()

if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
    )
