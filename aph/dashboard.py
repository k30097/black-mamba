from flask import Flask, Blueprint, render_template
from flask_login import login_required, current_user
from .models import Past_scans_dirbuster, Past_scans_nmap, Past_scans_scraping

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
    nmap_scans =  Past_scans_nmap.query.filter_by(user_id=current_user.id).all()
    dirbuster_scans = Past_scans_dirbuster.query.filter_by(user_id=current_user.id).all()
    scraping_scans = Past_scans_scraping.query.filter_by(user_id=current_user.id).all()
    total_scans = len(nmap_scans) + len(dirbuster_scans) + len(scraping_scans)
    account_creation_date = current_user.date_created.strftime('%Y-%m-%d')  
    print('nmap_scans', nmap_scans)
    print('dirbuster_scans', dirbuster_scans)
    print('scraping_scans', scraping_scans)
    return render_template('account.html', email=current_user.email, 
                           account_creation_date=account_creation_date,
                           total_scans=total_scans,
                           nmap_scans=nmap_scans, dirbuster_scans=dirbuster_scans, 
                           scraping_scans=scraping_scans)
    
@dashboard_bp.route('/instructions/')
def instructions():
    return render_template('instructions.html')