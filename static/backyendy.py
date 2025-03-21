from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import time

app = Flask(__name__)

# Конфигуриране на базата данни (SQLite файл)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posture.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 📌 Таблица, която записва всички измервания
class AllInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angle = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

# 📌 Таблица, която съдържа само последния записан ъгъл
class SelectedInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=1)
    angle = db.Column(db.Float, nullable=False)

# Създаваме базата и таблиците
with app.app_context():
    db.create_all()
    
    # Проверяваме дали в SelectedInfo има запис, ако няма - създаваме
    if not SelectedInfo.query.first():
        db.session.add(SelectedInfo(id=1, angle=0))  # Начална стойност
        db.session.commit()

# 📌 Функция за въвеждане на данни
def insert_data():
    with app.app_context():
        while True:
            new_angle = round(random.uniform(5, 50), 2)

            # 📌 Добавяне в AllInfo
            new_entry = AllInfo(angle=new_angle)
            db.session.add(new_entry)
            db.session.commit()

            # 📌 Презаписване на единствения запис в SelectedInfo
            selected_entry = SelectedInfo.query.first()
            selected_entry.angle = new_angle  # Взима последния ъгъл
            db.session.commit()

            # ✅ Принтираме в терминала
            print(f"New entry: {new_angle} at {datetime.utcnow()}")
            print(f"SelectedInfo updated: Angle -> {new_angle}")

            time.sleep(5)  # ❗ Изчаква 5 секунди преди следващото измерване

# Стартираме записа на данни
if __name__ == "__main__":
    insert_data()