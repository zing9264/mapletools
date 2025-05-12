from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Simulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    target_count = db.Column(db.Integer, nullable=False)
    scroll_cost = db.Column(db.Integer, nullable=False)
    success_rate = db.Column(db.Float, nullable=False)
    max_attempts = db.Column(db.Integer, nullable=False)
    total_scrolls = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    distribution = db.Column(db.Text, nullable=False)  # JSON 字串
