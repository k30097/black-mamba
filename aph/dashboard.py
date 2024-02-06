from flask import Flask, Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Past_scans_ffuf, Past_scans_nmap, Past_scans_scraping, User

# this blueprint page includes all the entries on the navbar at the top of the page

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    return render_template('home.html')

@dashboard_bp.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@dashboard_bp.route('/account/', methods=['POST' , 'GET'])
@login_required
def account():
    
    # on this page the user can see the results of the past scans completed while logged on this account
    # as of feb 6 2024 nmap scans are the only type included, but others will follow.
    
    nmap_scans =  Past_scans_nmap.query.filter_by(user_id=current_user.id).all()
    ffuf_scans = Past_scans_ffuf.query.filter_by(user_id=current_user.id).all()
    scraping_scans = Past_scans_scraping.query.filter_by(user_id=current_user.id).all()
        
    print('nmap_scans', nmap_scans)
    print('ffuf_scans', ffuf_scans)
    print('scraping_scans', scraping_scans)
    return render_template('account.html', current_user=current_user, nmap_scans=nmap_scans, ffuf_scans=ffuf_scans, scraping_scans=scraping_scans)
    
@dashboard_bp.route('/instructions/')
def instructions():
    return render_template('instructions.html')