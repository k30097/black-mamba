from flask import Flask, Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Past_scans_ffuf, Past_scans_nmap, Past_scans_scraping, User


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