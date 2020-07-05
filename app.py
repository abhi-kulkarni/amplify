from flask import Flask, render_template
import flask
from sqlalchemy import func
from flask_cors import CORS
from decimal import Decimal
from werkzeug.security import check_password_hash, generate_password_hash
import json
from flask_sqlalchemy import SQLAlchemy

from functools import wraps
import sqlalchemy


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        self.encoding = 'latin-1'
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


app = Flask(__name__)

app.json_encoder = DecimalEncoder

app.config.from_pyfile('config.py')

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
            if 'userId' not in flask.session:
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
        return flask.redirect(flask.url_for('user.login'))


@app.route("/api/login", methods=["GET", "POST"])
def login():
    from models import User
    if flask.request.method == 'POST' and 'username' in flask.request.json['post_data'] and 'password' in flask.request.json['post_data']:
        users = db.session.query(User).filter(func.lower(flask.request.json['post_data']['username']) == func.lower(User.email)).all()
        if len(users) != 0: # or len(usersbyrepid) != 0
            if len(users) != 0:
                user = users[0]
            if check_password_hash(user.password, flask.request.json['post_data']['password']):
                flask.session['userId'] = user.id
                flask.session['userEmail'] = user.email
                flask.session['userName'] = user.firstName+' '+user.lastName

                temp_dict = dict()
                temp_dict['userId'] = user.id
                temp_dict['userEmail'] = user.email
                temp_dict['userName'] = user.firstName + ' ' + user.lastName

                return flask.jsonify(ok=True, user_data=temp_dict)
            else:
                return flask.jsonify(ok=False, error="No such user or incorrect password")
        else:
            return flask.jsonify(ok=False, error="No such user or incorrect password")
    return flask.jsonify(ok=False, error='')


@app.route('/api/get_authenticated_user_information')
def get_authenticated_user_information():
    if 'userId' in flask.session and flask.session['userId']:
        from models import User
        user = db.session.query(User).get(flask.session['userId'])

        temp_dict = dict()
        temp_dict['userId'] = user.id
        temp_dict['userEmail'] = user.email
        temp_dict['userName'] = user.firstName + ' ' + user.lastName

        flask.session['userId'] = user.id
        flask.session['userEmail'] = user.email
        flask.session['userName'] = user.firstName + ' ' + user.lastName

        return flask.jsonify(ok=True, user_data=temp_dict, is_logged_in=True)
    else:
        return flask.jsonify(ok=False,is_logged_in=False)


@app.route('/api/changePassword', methods=['POST'])
def submit_password():
    from models import User
    user = User.query.get(flask.session['userId'])
    error = ""
    msg = ""
    if check_password_hash(user.password, flask.request.json.get('currentPassword','')):
        if len(flask.request.json.get('newPassword','')) >= 8:
            if flask.request.json.get('newPassword','') == flask.request.json.get('confirmPassword',''):
                user.password = generate_password_hash(flask.request.json.get('newPassword',''), salt_length=8)
                db.session.commit()
                msg = "Password is changed successfully. Please sign-in with new password."
            else:
                error = "Does not match new password."
        else:
            error = "Password length should be atleast 8 character."
    else:
        error = "Current Password is wrong."

    return flask.jsonify(ok=True, error=error, msg=msg)


@app.route('/api/logout', methods= ['GET'])
def logout():
    if 'userId' in flask.session:
        del flask.session['userId']
        del flask.session['userEmail']
        del flask.session['userName']
    return flask.jsonify(ok=True)


@app.route("/api/clear_session/", methods=["GET"])
def clear_session():
    from flask import session

    if 'user_id' in flask.session:
        session.clear()

    return flask.jsonify(ok=True)

from admin_views import *

if __name__ == '__main__':
    app.run()
