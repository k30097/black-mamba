from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash
from extensions import in_session

auth_bp = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

@auth_bp.route('/login/', methods=['POST' , 'GET'])
def login():
    if request.method == 'POST':
        try:
            if in_session():
                return redirect(url_for('dashboard.account'))
        except Exception as e:
            flash(f'There was an error: {e}')
    elif request.method == 'GET':
        if in_session():
            return redirect(url_for('dashboard.account'))
    return render_template('login.html')

@auth_bp.route('/signup/')
def signup():
    return render_template('signup.html')

@auth_bp.route('/logout/')
def logout():
    session.pop('email', None)
    print('you have been logged out')
    return render_template('home.html')