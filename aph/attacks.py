from flask import Flask, Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
import ipaddress
import nmap

attacks_bp = Blueprint('attacks', __name__, )

nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe"
scanner = nmap.PortScanner(nmap_search_path=nmap_path)
port_range = 65535

@attacks_bp.route('/scraping/')
@login_required
def scraping():
    return render_template('scraping.html')

@attacks_bp.route('/ffuf/')
@login_required
def ffuf():
    return render_template('ffuf.html')

@attacks_bp.route('/nmap/', methods=['GET', 'POST'])
@login_required
def nmap_scan():
    nmap_scan_results = session.get('nmap_scan_results', {})
    
    if request.method == 'POST':
        target_ip = request.form.get('ip_address')
        
        if target_ip:
            try:
                ip_address_obj = ipaddress.ip_address(target_ip)
                result = scanner.scan(target_ip, f'1-{port_range}')
                nmap_scan_results = result
                flash('scan completed successfully', category='success')
                session['nmap_scan_results'] = nmap_scan_results
                return render_template('nmap.html', nmap_scan_results=nmap_scan_results)
            except Exception as e:
                flash(f'{e}, try again', category='error')
                
    return render_template('nmap.html', nmap_scan_results=nmap_scan_results)
