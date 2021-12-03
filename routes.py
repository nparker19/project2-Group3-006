"""
this script is the central to the app and calls major functions
in other part of the entire application. The route and html rendering
are defined here
"""
import os
from datetime import timedelta
from functools import wraps
from authlib.integrations.flask_client import OAuth
from flask.helpers import url_for
from werkzeug.utils import redirect
import flask
from flask import session
from flask_login import current_user, LoginManager
from flask_login.utils import login_required
from app import app, db
from models import User_DB
from methods import (
    suggest,
    sort_dict_time_regular,
    convert_schedule_to_regtime,
)


# from googlecalmethods import check_connect,create_schedules
# # from listschedule import list_schedules

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
)

@app.route("/authorize")
def authorize():
    """
    This method handle the user google autherization
    """
    google = oauth.create_client("google")
    # token = google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()
    # user = oauth.google.userinfo()
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

# This route accepts the unsorted schedule from the client
# and returns to the client a sorted schedule
# @app.route("/sorting", methods=["POST"])
def sorting():
    """
    This method directs sort lists
    """
    error_message = []
    unsorted_schedule = flask.request.json.get("unsorted_schedule")
    try:
        converted_dict = convert_schedule_to_regtime(unsorted_schedule)
        sorted_schedule = sort_dict_time_regular(converted_dict)
    except ValueError:
        error_message.append("Invalid Time entered.")
        return flask.jsonify({"message_server": error_message})

    return flask.jsonify(
        {
            "message_server": error_message,
            "server_sorted_Schedule": sorted_schedule,
        }
    )

# This route handles the fetch API most call for when the "receive suggestions" button is pressed.
@app.route("/suggestions", methods=["POST"])
def suggestions():
    """
    This method takes in a schedule dictionary and a suggestions dictionary from the client,
    and returns schedule suggestions to the client.
    """
    error_message = []
    schedule_dict = flask.request.json.get("schedule_dict")
    suggest_dict = flask.request.json.get("suggest_dict")
    try:
        suggestions_list = suggest(schedule_dict, suggest_dict)
    except Exception as error:
        error_message.append(
            f"We were unable to retrieve your schedule suggestions. Error: {error}"
        )
        return flask.jsonify(
            {
                "message_server": error_message,
            }
        )
    return flask.jsonify(
        {
            "schedule_server": schedule_dict,
            "suggest_server": suggest_dict,
            "suggestions_server": suggestions_list,
            "message_server": error_message,
        }
    )

@app.route("/complete", methods=["POST"])
def complete():
    """
    This method takes in schedule dictionary and return dict to server
    """
    error_message = []
    # schedule_date = flask.request.json.get("currentDate")
    schedule_dict = flask.request.json.get("schedule_dict")

    try:
        check_connect()
        create_schedules(schedule_dict)
    except Exception as error:
        error_message.append(
            f"Calendar was not successfully saved to google calendar. Error: {error}"
        )
        return flask.jsonify(
            {
                "message_server": error_message,
            }
        )
    return flask.jsonify(
        {"schedule_server": schedule_dict, "message_server": error_message}
    )
bp = flask.Blueprint("bp", __name__, template_folder="./build")

@bp.route("/index")
def index():
    """
    Renders the create schedule page which allows the user to edit
    their current daily schedule, receive suggestions, and save to their google calendar
    """
    return flask.render_template("index.html")
app.register_blueprint(bp)

def add_user_emaildb(userEmail):
    """
    function query user database
    """
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