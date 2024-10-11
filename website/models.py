from . import db
import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating out of 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default = func.now())

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), nullable=False)
    booking_time = db.Column(db.DateTime(timezone=True), default = func.now())
    amount = db.Column(db.Float, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    phone = db.Column(db.String(15), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    language = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable= True)
    screenings = db.relationship('Screening', backref='movie', lazy=True, cascade="all, delete-orphan")

class Cinema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    total_screens = db.Column(db.Integer, nullable=False)
    screenings = db.relationship('Screening', backref='cinema', lazy=True, cascade="all, delete")


class Screening(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinema.id'), nullable=False)
    screen_number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    bookings = db.relationship('Booking', backref='screening', lazy=True)


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'), nullable=False)
    row = db.Column(db.String(5), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='seat', lazy=True)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_time = db.Column(db.DateTime(timezone=True), default = func.now())
    status = db.Column(db.String(20), nullable=False)  # e.g., 'Paid', 'Pending', 'Failed'


    