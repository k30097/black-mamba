from flask import Flask, Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    return render_template('home.html')

@dashboard_bp.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')

@dashboard_bp.route('/report/')
def reports():
    return render_template('report.html')

@dashboard_bp.route('/account/')
def account():
    return render_template('account.html')

@dashboard_bp.route('/instructions/')
def instructions():
    return render_template('instructions.html')