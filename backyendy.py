from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import time
import pytz 

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



def insert_data():
    with app.app_context():


        while True:
            new_angle = round(random.uniform(5, 35), 2)

            new_entry = AllInfo(angle=new_angle, created=get_utc_time())
            db.session.add(new_entry)
            db.session.commit()

            selected_entry = SelectedInfo.query.first()
            selected_entry.angle = new_angle
            db.session.commit()

            print(f"New entry: {new_angle} at {datetime.utcnow()} (UTC)")
            time.sleep(1)


if __name__ == "__main__":
    insert_data()
