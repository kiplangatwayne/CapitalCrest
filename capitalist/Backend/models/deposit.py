# Deposit Model
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask  import app, current_app, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
db = SQLAlchemy(app)

class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)