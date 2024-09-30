from flask import Flask, Blueprint, render_template,request,flash,redirect, url_for, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db
from . import mail
from flask_mail import Message
import random
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


def generate_otp():
    otp = random.randint(100000, 999999)
    return str(otp)
def send_otp(recipient_email, otp):
    msg = Message('Your otp code', recipients=[recipient_email])
    msg.body = f'use this otp {otp} to complete verification'
    mail.send(msg)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()

        if not user:
            flash("Email does not exist!", category="alert-danger")
            return redirect(url_for('auth.signUp'))
        else:
            if check_password_hash(user.password, password):
                flash("Login Succesfull", category="alert-success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password incorrect, try again!", category="alert-danger")
    return render_template("login.html" ,user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/check-email", methods=["POST"])
def checkemail():
    email_data = request.get_json()
    email = email_data.get('email')

    if not email:
        return jsonify({"message" : "Please provide email", "exists" : False}),200
    user = User.query.filter_by(email = email).first()

    if user:
        return jsonify({"message": "Email already exists", "exists": True}),200
    else:
        return jsonify({"message":"email available", "exists": False}),200



@auth.route("/signUp", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()

        if user:
            flash("Email already exist", category="alert-danger")
            return redirect(url_for('auth.signUp'))
        elif len(email)<3:
            flash("Email must be greater than 2 characters" , category="alert-danger")
        elif len(name) < 2:
            flash("Name must be greater than 1 character", category="alert-danger")
        elif password1 != password2:
            flash("password must be same", category="alert-danger")
        else:
            otp = generate_otp()
            send_otp(email, otp)
            session['otp'] = otp
            session['user_data'] = {
                'email' : email,
                'name' : name,
                'password': generate_password_hash(password1, method="pbkdf2:sha256")
            }
            flash(f"OTP sent to {email}", category="alert-success")
            return redirect(url_for('auth.verifyOTP'))   
    return render_template("signup.html" ,user=current_user)

@auth.route("/verifyOTP", methods= ["GET","POST"])
def verifyOTP():
    if request.method == "POST":
            otp1 = request.form.get('otp1')
            otp2 = request.form.get('otp2')
            otp3 = request.form.get('otp3')
            otp4 = request.form.get('otp4')
            otp5 = request.form.get('otp5')
            otp6 = request.form.get('otp6')
            user_otp = otp1+otp2+otp3+otp4+otp5+otp6
            stored_otp = session.get('otp')
            if user_otp == stored_otp:
                user_data = session.get('user_data')
                if user_data:
                    new_user = User(email = user_data['email'], name= user_data['name'], password = user_data['password'])
                    db.session.add(new_user)
                    db.session.commit()
                    session.pop('otp', None)
                    session.pop('user_data', None)
                    flash("OTP verified and user registered succesfully" ,category="alert-success")
                    return redirect(url_for("auth.login"))
    return render_template("verifyOTP.html", user= current_user)

@auth.route("/resend_otp")
def resend_otp():
    email = session.get('email') 
    if email:
        otp = generate_otp() 
        send_otp(email, otp) 
        session['otp'] = otp  
        flash(f"OTP sent to your {email}.", category="alert-success")
    else:
        flash("Could not resend OTP. Please try again.", category="alert-danger")
    return redirect(url_for('auth.verifyOTP'))  # Redirect to the OTP verification page