from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'

db=SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  address = db.Column(db.String(200), nullable=False)
  pincode = db.Column(db.Integer, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  reservations = db.relationship('Reservation', backref='user')
  vehicle_no = db.Column(db.String(20), nullable=False)

class Reservation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  spot_id = db.Column(db.Integer, nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime, nullable=False)
  cost = db.Column(db.Float, nullable=True, default=0.0)

class ParkingLot(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  prime_location_name = db.Column(db.String(120), nullable=False)
  address = db.Column(db.String(200), nullable=False)
  pincode = db.Column(db.Integer, nullable=False)
  total_spots = db.Column(db.Integer, nullable=False)
  price_per_hour = db.Column(db.Float, nullable=False,default=0.0)

class ParkingSpot(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
  spot_number = db.Column(db.String(20), nullable=False)
  status = db.Column(db.String(20), nullable=False, default='available')  # available, reserved, occupied

class Admin(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

class UserHistory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
  action = db.Column(db.String(50), nullable=False)  # e.g., 'created', 'cancelled'
  timestamp = db.Column(db.DateTime, nullable=False)
  user = db.relationship('User', backref='history')
  reservation = db.relationship('Reservation', backref='history')

class AdminHistory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
  action = db.Column(db.String(50), nullable=False)  # e.g., 'added', 'updated', 'deleted'
  timestamp = db.Column(db.DateTime, nullable=False)
  admin = db.relationship('Admin', backref='history')
