from app import db
import datetime
import json
import decimal

__author__ = 'mayur'


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),nullable=False)
    firstName=db.Column(db.String(150),nullable=False)
    lastName=db.Column(db.String(150),nullable=True)
    password=db.Column(db.String(150),nullable=False)
    created_on=db.Column(db.DateTime,nullable=False)
    role = db.Column(db.String(200))
    expiryToken=db.Column(db.String(50),nullable=True)
    expiryDate=db.Column(db.DateTime,nullable=True)
    flag=db.Column(db.Boolean,nullable=True)

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