from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse
from .models import User
from . import db

auth_bp = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

@auth_bp.route('/login/', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('logged in', category='success')
                print('logged in')
                login_user(user, remember=True)
                return redirect(url_for('dashboard.account'))
            else:
                print('password in incorrect')
                flash('password in incorrect', category='error')
        else:
            print('email is not in the database')
            flash('email is not in the database', category='error')
    return render_template('login.html')


@auth_bp.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        # check if the user is already signed up with this email.
        # if the email is not found in the database then a new user
        # is created. the password stored is the hashed version.
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('this email has already been used', category='error')
            print('this email has already been used')
        elif password != password2:
            flash('passwords do not match', category='error')
        elif len(email) < 4:
            flash('insert a valid email', category='error')
        elif len(password) < 5:
            flash('password is too short, min. 5 characters', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('new account created, you are now logged in', category='success')
            return redirect(url_for('dashboard.account'))
    return render_template('signup.html')

@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('you have been logged out', category='success')
    return redirect(url_for('dashboard.home'))