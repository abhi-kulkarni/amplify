from flask import Flask, render_template
import flask
import os
from sqlalchemy import func
from flask_cors import CORS
from decimal import Decimal
from werkzeug.security import check_password_hash, generate_password_hash
import json
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

env = os.environ.get


class Config:
    LOCALE = env("AMPLIFY_LOCALE", 'en_US.utf8')
    SECRET_KEY = env("AMPLIFY_SECRET_KEY",
                     "\xa9\x01\xd2\xc7\x97U\xe7ijo\x1c\xc8\xd8'\x9b-\xf3\xad\x02\x8e\xd2\x16\xc4u\xbfN+')\xfb\x8e\x9a")
    SQLALCHEMY_DATABASE_URI = env(
        "AMPLIFY_SQL_ALCHEMY_DATABASE_URI", "mysql://<user>:<password>@localhost/<db>")
    DEBUG = (env("AMPLIFY_DEBUG", 'True') == 'True')
    BASE_URL = env("AMPLIFY_BASE_URL", "https://amplify.com")
    DEBUG_EMAIL_SEND = (env("AMPLIFY_DEBUG_EMAIL_SEND", 'True') == 'True')
    TEST_EMAIL_ID = env("AMPLIFY_TEST_EMAIL_ID", "abhishekkulkarni706@gmail.com")


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        self.encoding = 'latin-1'
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

app = Flask(__name__)

app.json_encoder = DecimalEncoder

# app.config.from_pyfile('config.py')

app.config.from_object(Config())

db = SQLAlchemy(app)

db.init_app(app)

cors = CORS(app, allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials", "withCredentials"],
            supports_credentials=True, resources={r"/*": {"origins": "*"}})


def requires_auth(*privs):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # print flask.session
            if 'user_id' not in flask.session:
                return unauthorized_abort()
            else:
                if len(privs) > 0:
                    if len(set(privs).intersection(set(flask.session['userPrivilege'])))==0:
                        return unauthorized_abort()
                return f(*args, **kwargs)

        return decorated

    return wrapper


def unauthorized_abort():
    if flask.request.is_xhr:
        return flask.abort(401)
    else:
        return flask.redirect(flask.url_for("user.login"))

@app.route("/api/hello", methods=["GET", "POST"])
def hello():
    print("Hello")


@app.route("/login", methods=["POST"])
def login():
    from models import User
    import datetime
    from sqlalchemy import or_

    if flask.request.method == "POST" and "username" in flask.request.json["post_data"] and "password" in flask.request.json["post_data"]:
        users = db.session.query(User).filter(or_(func.lower(flask.request.json["post_data"]["username"]) == func.lower(User.email), func.lower(flask.request.json["post_data"]["username"]) == func.lower(User.username))).all()
        if len(users) != 0:
            user = users[0]
            if check_password_hash(user.password, flask.request.json["post_data"]["password"]):
                flask.session["user_id"] = user.id
                flask.session["email"] = user.email
                flask.session["first_name"] = user.first_name
                flask.session["last_name"] = user.last_name
                flask.session["username"] = user.username
                flask.session["last_login"] = user.last_login

                temp_dict = dict()
                temp_dict["userId"] = user.id
                temp_dict["userEmail"] = user.email
                temp_dict["userName"] = user.username
                temp_dict["firstName"] = user.first_name
                temp_dict["lastName"] = user.last_name
                temp_dict["last_login"] = str(user.last_login)

                user.last_login = datetime.datetime.now()
                db.session.add(user)
                db.session.commit()

                return flask.jsonify(ok=True, user_data=temp_dict)
            else:
                return flask.jsonify(ok=False, error="No such user or incorrect password")
        else:
            return flask.jsonify(ok=False, error="No such user or incorrect password")
    return flask.jsonify(ok=False, error='')


@app.route("/login_fb_google_sso", methods=["POST"])
def login_fb_google_sso():
    from models import User
    import datetime

    if flask.request.method == "POST" and "email" in flask.request.json["post_data"]:
        user = db.session.query(User).filter(flask.request.json["post_data"]["email"] == User.email, User.provider == flask.request.json["post_data"]["provider"]).first()
        if user:
            flask.session["user_id"] = user.id
            flask.session["email"] = user.email
            flask.session["first_name"] = user.first_name
            flask.session["last_name"] = user.last_name
            flask.session["username"] = user.username
            flask.session["last_login"] = user.last_login

            temp_dict = dict()
            temp_dict["userId"] = user.id
            temp_dict["userEmail"] = user.email
            temp_dict["userName"] = user.username
            temp_dict["firstName"] = user.first_name
            temp_dict["lastName"] = user.last_name
            temp_dict["last_login"] = str(user.last_login)

            user.last_login = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()

            return flask.jsonify(ok=True, user_data=temp_dict)
        else:
            return flask.jsonify(ok=False, error="No such user found")



@app.route("/get_authenticated_user_information")
def get_authenticated_user_information():
    import datetime
    if "user_id" in flask.session and flask.session["user_id"]:
        from models import User
        user = db.session.query(User).get(flask.session["user_id"])

        temp_dict = dict()
        temp_dict["userId"] = user.id
        temp_dict["userEmail"] = user.email
        temp_dict["userName"] = user.username
        temp_dict["firstName"] = user.first_name
        temp_dict["lastName"] = user.last_name
        temp_dict["appThemeColor"] = json.loads(user.extra_data)["app_theme_color"]

        flask.session["first_name"] = user.first_name
        flask.session["last_name"] = user.last_name
        flask.session["user_id"] = user.id
        flask.session["email"] = user.email
        flask.session["username"] = user.username
        db.session.add(user)
        db.session.commit()
        return flask.jsonify(ok=True, user_data=temp_dict, is_logged_in=True)
    else:
        return flask.jsonify(ok=False,is_logged_in=False)


@app.route("/validate_email", methods=["POST"])
def validate_email():
    from models import User

    email = flask.request.json.get("email", "")

    user = db.session.query(User).filter(User.email == email).first()
    if user:
        return flask.jsonify(ok=True)
    else:
        return flask.jsonify(ok=False)

@app.route("/forgot_password", methods=["POST"])
def forgot_password():
    from models import User

    email = flask.request.json.get("email", "")
    password = flask.request.json.get("password", "")
    user = db.session.query(User).filter(User.email == email).first()
    user.password = generate_password_hash(password, salt_length=8)

    db.session.add(user)
    db.session.commit()

    return flask.jsonify(ok=True)

@app.route("/validate_password", methods=["POST"])
def validate_password():
    from models import User

    user = User.query.get(flask.session["user_id"])
    if check_password_hash(user.password, flask.request.json.get("current_password","")):
        return flask.jsonify(ok=True)
    else:
        return flask.jsonify(ok=False)

@app.route("/change_password", methods=["POST"])
def change_password():
    from models import User

    user = User.query.get(flask.session["user_id"])
    if user:
        user.password = generate_password_hash(flask.request.json.get("password",""), salt_length=8)
        db.session.add(user)
        db.session.commit()
        return flask.jsonify(ok=True)
    else:
        return flask.jsonify(ok=False)


@app.route("/logout", methods= ["GET"])
def logout():
    from flask import session

    if "user_id" in flask.session:
        session.clear()
    return flask.jsonify(ok=True)


@app.route("/clear_session/", methods=["GET"])
def clear_session():
    from flask import session

    if "user_id" in flask.session:
        session.clear()

    return flask.jsonify(ok=True)

from views import user_views
from views import todo_views

if __name__ == '__main__':
    app.run()
