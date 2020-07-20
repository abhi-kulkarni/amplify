from app import app, db
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
import flask
import datetime


@app.route('/usermanagement_data', methods=['GET'])
def usermanagement_data():
    from models import User
    from app import db

    user=[k.to_dict() for k in db.session.query(User).all()]

    return flask.jsonify(ok=True, users=user)


@app.route('/add_user', methods=['POST'])
def add_user():
    from app import db
    from models import User
    import json
    import uuid

    post_data = flask.request.json.get('post_data', '')
    
    user = User()
    user.id = str(uuid.uuid4())
    user.password = generate_password_hash(post_data.get('password', ''), salt_length=8)
    user.created_on = datetime.datetime.now()
    user.first_name = post_data.get('first_name', '')
    user.last_name = post_data.get('last_name', '')
    user.username = post_data.get('username', '')
    user.email = post_data.get('email', '')
    user.gender = post_data.get('gender', '')
    user.country = post_data.get('country', '')
    user.sso = post_data.get('sso', False)
    user.profile_picture = post_data.get('profile_picture', '')
    extra_data = {"app_theme_color":"#0097A7"}
    user.extra_data = json.dumps(extra_data)
    db.session.add(user)
    db.session.commit()
    return flask.jsonify(ok=True)

@app.route('/edit_user', methods=['POST'])
def edit_user():
    from app import db
    from models import User
    import json
    
    post_data = flask.request.json.get('post_data', '')
    user = User.query.get(post_data.get('id', ''))
    user.first_name = post_data.get('first_name', '')
    user.last_name = post_data.get('last_name', '')
    user.username = post_data.get('username', '')
    user.email = post_data.get('email', '')
    user.country = post_data.get('country', '')
    user.gender = post_data.get('gender', '')
    user.profile_picture = post_data.get('profile_picture', '')
    app_theme_color = post_data.get('app_theme_color', '')
    extra_data = {"app_theme_color": app_theme_color}
    user.extra_data = json.dumps(extra_data)
    db.session.add(user)
    db.session.commit()
    return flask.jsonify(ok=True)

@app.route('/delete_user/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    from models import User
    from app import db
    user=User.query.get(user_id)
    todos = db.session.query(Todo).filter(Todo.user_id == user_id).all()
    for todo in todos:
        db.session.delete(todo)
    db.session.delete(user)
    db.session.commit()
    return flask.jsonify(ok=True)


@app.route("/get_user_data/<string:user_id>", methods=["GET"])
def get_user_data(user_id):
    from app import db
    from models import User
    
    user_data = db.session.query(User).get(user_id)
    if user_data:
        user_data = user_data.to_dict()
        return flask.jsonify(ok=True, user_data=user_data)
    else:
        return flask.jsonify(ok=False)
