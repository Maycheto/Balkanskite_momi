from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Свързване към базата данни
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posture.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модели за базата данни
class AllInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angle = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

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

@app.route('/current')
def current():
    return render_template('current.html', title='Current Posture')

@app.route('/current-angle')
def current_angle():
    data = SelectedInfo.query.first()
    if data:
        return jsonify({"angle": data.angle})
    else:
        return jsonify({"error": "No data available"}), 404

@app.route('/today-data')
def today_data_route():
    data = AllInfo.query.order_by(AllInfo.created).all()
    
    if not data:
        return jsonify([])

    today_data = []
    for entry in data:
        formatted_time = entry.created.strftime("%H:%M:%S")
        slouched = entry.angle > 30
        today_data.append({"time": formatted_time, "angle": entry.angle, "slouched": slouched})

    return jsonify(today_data)

if __name__ == '__main__':   
    app.run(debug=True)
