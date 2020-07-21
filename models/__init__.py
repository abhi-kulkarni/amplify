from app import db
import datetime
import json
import decimal
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT

class User(db.Model):
    id=db.Column(db.String(200),primary_key=True)
    email=db.Column(db.String(150),nullable=False, unique=True)
    first_name=db.Column(db.String(150),nullable=False)
    last_name=db.Column(db.String(150),nullable=True)
    username=db.Column(db.String(150),nullable=False)
    password=db.Column(db.String(150),nullable=False)
    last_passwords=db.Column(db.TEXT(),nullable=True)
    created_on=db.Column(db.DateTime,nullable=False)
    expiry_token=db.Column(db.String(50),nullable=True)
    expiry_date=db.Column(db.DateTime,nullable=True)
    sso=db.Column(db.Boolean,nullable=True)
    locked=db.Column(db.Boolean,nullable=True)
    provider=db.Column(db.String(50),nullable=True)
    profile_picture = db.Column(LONGTEXT())
    last_login=db.Column(db.DateTime)
    extra_data=db.Column(db.TEXT())
    gender=db.Column(db.String(10),nullable=True)
    country=db.Column(db.String(100),nullable=True)

    def to_dict(self):
        fields = {}
        for field in [x for x in dir(self) if not x.startswith("_") and x != 'metadata']:
            data = self.__getattribute__(field)
            if type(data) is datetime.datetime:
                data = data.strftime('%Y-%m-%dT%H:%M:%SZ')
            if type(data) is datetime.date:
                data = data.strftime('%Y-%m-%d')
            if not hasattr(data, '__call__'):
                try:
                    json.dumps(data)
                    if field[-4:] == "List" and type(data) is not list:
                        fields[field] = [x for x in data.split(",") if x.strip() != ""]
                    else:
                        fields[field] = data
                except TypeError:
                    if type(data) is decimal.Decimal:
                        fields[field] = float(data)
                    else:
                        fields[field] = None
        return fields


class Todo(db.Model):

    id=db.Column(db.String(200),primary_key=True)
    title=db.Column(db.String(50), nullable=False)
    user_id=db.Column(db.String(200))
    content=db.Column(db.TEXT(),nullable=True)
    status=db.Column(db.Boolean,nullable=True)
    created_on=db.Column(db.DateTime)
    alarm_time=db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        fields = {}
        for field in [x for x in dir(self) if not x.startswith("_") and x != 'metadata']:
            data = self.__getattribute__(field)
            if type(data) is datetime.datetime:
                data = data.strftime('%Y-%m-%dT%H:%M:%SZ')
            if type(data) is datetime.date:
                data = data.strftime('%Y-%m-%d')
            if not hasattr(data, '__call__'):
                try:
                    json.dumps(data)
                    if field[-4:] == "List" and type(data) is not list:
                        fields[field] = [x for x in data.split(",") if x.strip() != ""]
                    else:
                        fields[field] = data
                except TypeError:
                    if type(data) is decimal.Decimal:
                        fields[field] = float(data)
                    else:
                        fields[field] = None
        return fields