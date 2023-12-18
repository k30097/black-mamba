from flask import Flask, Blueprint, render_template

attacks_bp = Blueprint('attacks', __name__, )

@attacks_bp.route('/scraping/')
def scraping():
    return render_template('scraping.html')

@attacks_bp.route('/ffuf/')
def ffuf():
    return render_template('scraping.html')

@attacks_bp.route('/nmap/')
def nmap():
    return render_template('scraping.html')
