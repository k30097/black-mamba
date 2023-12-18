from flask import Flask, Blueprint, render_template
from flask_login import login_required, current_user

attacks_bp = Blueprint('attacks', __name__, )

@attacks_bp.route('/scraping/')
@login_required
def scraping():
    return render_template('scraping.html')

@attacks_bp.route('/ffuf/')
@login_required
def ffuf():
    return render_template('scraping.html')

@attacks_bp.route('/nmap/')
@login_required
def nmap():
    return render_template('scraping.html')
