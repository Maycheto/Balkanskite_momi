# from flask import Flask, render_template, jsonify
# import random
# import datetime

# app = Flask(__name__)

# # Симулация на текущ ъгъл на изгърбване
# def get_current_angle():
#     return round(random.uniform(5, 50), 2)

# # Симулация на данни за деня с изгърбвания
# def generate_today_data():
#     start_time = datetime.datetime.strptime("12:00", "%H:%M")
#     end_time = datetime.datetime.strptime("15:37", "%H:%M")
#     delta = (end_time - start_time) / 10  # 10 точки във времето
    
#     data = []
#     time = start_time
#     for _ in range(100):
#         angle = get_current_angle()
#         slouched = angle > 30  # Ако ъгълът е над 30 градуса, се брои за изгърбване
#         data.append({"time": time.strftime("%H:%M:%S"), "angle": angle, "slouched": slouched})
#         time += delta
    
#     return data

# today_data = generate_today_data()

# @app.route('/')
# def home():
#     return render_template('index.html', title='Home', content='Welcome to the Home Page')

# @app.route('/report')
# def report():
#     return render_template('report.html', title='Report')

# @app.route('/about-us')
# def about_us():
#     return render_template('index.html', title='About Us', content='Learn more about us on this page.')

# @app.route('/current-angle')
# def current_angle():
#     return jsonify({"angle": get_current_angle()})

# @app.route('/today-data')
# def today_data_route():
#     return jsonify(today_data)

# if __name__ == '__main__':
#     app.run(debug=True)

# --------------------------------------------------------------------------------------------------------------------------------------
# from flask import Flask, render_template, jsonify
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # 📌 Свързваме се към съществуващата база
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backyendy.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # 📌 Дефинираме модела на таблиците (само за четене)
# class AllInfo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     angle = db.Column(db.Float, nullable=False)
#     created = db.Column(db.DateTime, default=db.func.current_timestamp())

# class SelectedInfo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     angle = db.Column(db.Float, nullable=False)

# @app.route('/')
# def home():
#     return render_template('index.html', title='Home', content='Welcome to the Home Page')

# @app.route('/report')
# def report():
#     return render_template('report.html', title='Report')

# @app.route('/about-us')
# def about_us():
#     return render_template('index.html', title='About Us', content='Learn more about us on this page.')

# # 📌 Взима последния записан ъгъл от SelectedInfo
# @app.route('/current-angle')
# def current_angle():
#     selected_entry = SelectedInfo.query.first()
#     if selected_entry:
#         print(f"[LOG] Current angle requested: {selected_entry.angle}")  # ✅ Принтиране в терминала
#         return jsonify({"angle": selected_entry.angle})
    
#     print("[LOG] No data available in SelectedInfo")
#     return jsonify({"error": "No data available"}), 404

# # 📌 Взима всички записи за деня от AllInfo
# @app.route('/today-data')
# def today_data_route():
#     all_entries = AllInfo.query.all()
#     print(f"[LOG] Fetching all records from AllInfo. Found: {len(all_entries)} records")  # ✅ Принтиране в терминала

#     data = [
#         {"time": entry.created.strftime("%H:%M:%S"), "angle": entry.angle, "slouched": entry.angle > 30}
#         for entry in all_entries
#     ]

#     return jsonify(data)

# if __name__ == '__main__':
#     print("[LOG] Starting Flask app...")  # ✅ Индикация, че сървърът стартира
#     app.run(debug=True)

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Свързване към съществуващата база данни
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posture.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модели за базата данни
class SelectedInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angle = db.Column(db.Float, nullable=False)

@app.route('/current-angle')
def current_angle():
    data = SelectedInfo.query.first()  # Взимаме единствения запис
    if data:
        print(f"[LOG] Current angle from DB: {data.angle}")  # ✅ Принтира в терминала
        return jsonify({"angle": data.angle})
    else:
        print("[ERROR] No data in SelectedInfo table!")  # ✅ Ако няма запис
        return jsonify({"error": "No data available"}), 404

if __name__ == '__main__':
    print("[LOG] Starting Flask app...")
    app.run(debug=True)
