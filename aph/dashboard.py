from flask import Flask, Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    return render_template('home.html')

@dashboard_bp.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@dashboard_bp.route('/report/')
@login_required
def reports():
    return render_template('report.html')

@dashboard_bp.route('/account/', methods=['POST' , 'GET'])
@login_required
def account():
    return render_template('account.html')
    
@dashboard_bp.route('/instructions/')
def instructions():
    return render_template('instructions.html')