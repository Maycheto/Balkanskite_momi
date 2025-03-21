from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posture.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


BULGARIA_TZ = pytz.timezone('Europe/Sofia')

class AllInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angle = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



class SelectedInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angle = db.Column(db.Float, nullable=False)

@app.route('/')
def home():
    return render_template('index.html', title='Home', content='Welcome to the Home Page')

@app.route('/report')
def report():
    return render_template('report.html', title='Report')

@app.route('/about-us')
def about_us():
    return render_template('index.html', title='About Us', content='Learn more about us on this page.')

@app.route('/current-angle')
def current_angle():
    data = SelectedInfo.query.first()
    if data:
        print(f"[LOG] Current angle from DB: {data.angle}")
        return jsonify({"angle": data.angle})
    else:
        print("[ERROR] No data in SelectedInfo table!")
        return jsonify({"error": "No data available"}), 404




@app.route('/today-data')
def today_data_route():
    data = AllInfo.query.order_by(AllInfo.created).all()

    if not data:
        return jsonify({"timeline": [], "good_posture": 100, "bad_posture": 0})

    total_records = len(data)  # Броим само реалните записи
    slouched_count = sum(1 for entry in data if entry.angle > 30)

    # Изчисляваме процентите
    bad_posture_percentage = (slouched_count / total_records) * 100
    good_posture_percentage = 100 - bad_posture_percentage

    today_data = []
    for entry in data:

        if entry.created.tzinfo is None:
            entry.created = pytz.utc.localize(entry.created) 
        local_time = entry.created.replace(tzinfo=pytz.utc).astimezone(BULGARIA_TZ)
        formatted_time = local_time.strftime("%H:%M:%S")

        slouched = entry.angle > 30

        today_data.append({"time": formatted_time, "angle": entry.angle, "slouched": slouched})

    return jsonify({
        "timeline": today_data,
        "good_posture": round(good_posture_percentage, 2),
        "bad_posture": round(bad_posture_percentage, 2)
    })




if __name__ == '__main__':
    print("[LOG] Starting Flask app...")
    app.run(debug=True)
