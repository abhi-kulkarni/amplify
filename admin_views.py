from app import app, requires_auth, db
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
import flask
import datetime



@app.route('/api/userManagementData', methods=['GET'])
# @requires_auth('admin','manager')
def userManagementData():
    from models import User
    from app import db

    user=[k.to_dict() for k in db.session.query(User).all()]

    return flask.jsonify(ok=True, users=user)


@app.route('/api/new_user', methods=['POST'])
# @requires_auth('admin','manager')
def new_user():
    from app import db
    from models import User
    user = User()
    user.password = generate_password_hash(flask.request.json.get('password', ''), salt_length=8)
    user.created_on = datetime.datetime.now()
    user.role = flask.request.json.get('privilege', '')
    user.firstName = flask.request.json.get('firstName', '')
    user.lastName = flask.request.json.get('lastName', '')
    user.participantId = ''
    user.roleId = 1
    user.email = flask.request.json.get('email', '')
    db.session.add(user)
    db.session.commit()
    return flask.jsonify(ok=True)


@app.route('/api/delete_user/<int:userId>',methods=['DELETE'])
# @requires_auth('admin','manager')
def delete_user(userId):
    from models import User
    from app import db
    user=User.query.get(userId)
    db.session.delete(user)
    db.session.commit()
    return flask.jsonify(ok=True)


@app.route('/api/getUserData/<int:userId>', methods=['GET'])
# @requires_auth('admin','manager')
def getUserData(userId):
    from models import User
    from app import db
    user=User.query.get(userId)
    user_data = user.to_dict()
    del user_data['password']
    return flask.jsonify(ok=True, user_data=user_data)


@app.route('/api/edit_user', methods=['POST'])
# @requires_auth('admin','manager')
def edit_user():
    from app import db
    from models import User
    user = User.query.get(flask.request.json.get('id', ''))
    user.role = flask.request.json.get('privilege', '')
    user.firstName = flask.request.json.get('firstName', '')
    user.lastName = flask.request.json.get('lastName', '')
    user.email = flask.request.json.get('email', '')
    db.session.add(user)
    db.session.commit()
    return flask.jsonify(ok=True)