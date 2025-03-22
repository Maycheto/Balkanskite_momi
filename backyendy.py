# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posture.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


# class AllInfo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     angle = db.Column(db.Float, nullable=False)
#     created = db.Column(db.DateTime, nullable=False)


# class SelectedInfo(db.Model):
#     id = db.Column(db.Integer, primary_key=True, default=1)
#     angle = db.Column(db.Float, nullable=False)


# with app.app_context():
#     db.create_all()
    
#     if not SelectedInfo.query.first():
#         db.session.add(SelectedInfo(id=1, angle=0))  
#         db.session.commit()


# def get_utc_time():
#     return datetime.utcnow()


# def insert_data(coefficient):
#     """ Записва стойността на coefficient в базата данни """
#     with app.app_context():
#         new_entry = AllInfo(angle=coefficient, created=get_utc_time())
#         db.session.add(new_entry)
#         db.session.commit()

#         selected_entry = SelectedInfo.query.first()
#         selected_entry.angle = coefficient
#         db.session.commit()

#         print(f"[DATABASE] Saved coefficient: {coefficient}")
#         print(f"New entry: {selected_entry.angle} at {datetime.utcnow()} (UTC)")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posture.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class AllInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angle = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, nullable=False)


class SelectedInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=1)
    angle = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()
    
    if not SelectedInfo.query.first():
        db.session.add(SelectedInfo(id=1, angle=0))  
        db.session.commit()


def get_utc_time():
    return datetime.utcnow()


def insert_data(coefficient):
    """ Записва стойността на coefficient в базата данни """
    with app.app_context():
        new_entry = AllInfo(angle=coefficient, created=get_utc_time())
        db.session.add(new_entry)
        db.session.commit()

        selected_entry = SelectedInfo.query.first()
        selected_entry.angle = coefficient
        db.session.commit()

        print(f"[DATABASE] Saved coefficient: {coefficient}")
        print(f"New entry: {selected_entry.angle} at {datetime.utcnow()} (UTC)")