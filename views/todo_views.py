from app import app, db
from sqlalchemy import func
import flask
import datetime
import json

@app.route('/get_all_todo_data', methods=['GET'])
def get_all_todo_data():
    from models import Todo
    from app import db

    todos=[k.to_dict() for k in db.session.query(Todo).filter(Todo.user_id == flask.session["user_id"]).all()]
    for todo_obj in todos:
        todo_obj["check"] = False

    return flask.jsonify(ok=True, todos=todos)


@app.route('/add_todo', methods=['POST'])
def add_todo():
    from app import db
    from models import Todo, User
    import uuid

    post_data = flask.request.json.get('post_data', '')

    todo = Todo()
    todo.id = str(uuid.uuid4())
    todo.title = post_data.get('title', '')
    todo.user_id = flask.session["user_id"]
    todo.created_on = datetime.datetime.now()
    todo.status = post_data.get('status', False)
    todo.content = post_data.get('content', '')
    todo.alarm_time = post_data.get('alarm_time', None)

    db.session.add(todo)
    db.session.commit()

    return flask.jsonify(ok=True)

@app.route('/edit_todo', methods=['PUT'])
def edit_todo():
    from app import db
    from models import User, Todo
    import json
    
    post_data = flask.request.json.get('post_data', '')

    todo = db.session.query(Todo).get(post_data.get('id', ''))
    todo.title = post_data.get('title', '')
    todo.content = post_data.get('content', '')
    todo.alarm_time = post_data.get('alarm_time', '')
    todo.status = post_data.get('status', False)

    db.session.add(todo)
    db.session.commit()

    return flask.jsonify(ok=True)

@app.route('/delete_todo/<string:todo_id>',methods=['DELETE'])
def delete_todo(todo_id):
    from models import Todo, User
    from app import db

    todo=db.session.query(Todo).get(todo_id)
    db.session.delete(todo)
    db.session.commit()

    return flask.jsonify(ok=True)


@app.route('/delete_selected_todos',methods=['POST'])
def delete_selected_todos():
    from models import Todo, User
    from app import db

    selected_todos = flask.request.json.get('selected_todos', '')
    todo_data = db.session.query(Todo).filter(Todo.id.in_(selected_todos)).all()
    for todo_obj in todo_data:
        db.session.delete(todo_obj)
    db.session.commit()

    return flask.jsonify(ok=True)


@app.route("/get_todo_data/<string:todo_id>", methods=["GET"])
def get_todo_data(todo_id):
    from app import db
    from models import Todo
    
    todo_data = db.session.query(Todo).get(todo_id)
    if todo_data:
        todo_data = todo_data.to_dict()
        return flask.jsonify(ok=True, todo_data=todo_data)
    else:
        return flask.jsonify(ok=False)
