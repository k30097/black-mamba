from flask import Flask, Blueprint, render_template, request, session, redirect, url_for

auth_bp = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

@auth_bp.route('/login/', methods=['POST' , 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        return redirect(url_for('dashboard.account'))
    else:
        pass
    return render_template('login.html')

@auth_bp.route('/signup/')
def signup():
    return render_template('signup.html')

@auth_bp.route('/logout/')
def logout():
    return render_template('home.html')