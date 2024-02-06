from flask import Flask, Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
from .models import Past_scans_nmap, Past_scans_ffuf, Past_scans_scraping
from . import db
import logging
import ipaddress
import nmap
import json

attacks_bp = Blueprint('attacks', __name__)

# initialized nmap scanner. The max port range is currently set manually
# but eventually it will be decided by the user. Currently set at 22 to get 
# faster scans for testing purposes.
scanner = nmap.PortScanner()
port_range = 22

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
                # ^ this validates the input and raises an exception
                result = scanner.scan(target_ip, f'1-{port_range}')
                # Store the JSON results as a dictionary in the session
                nmap_scan_results = result
                session['nmap_scan_results'] = nmap_scan_results
                results_dict = json.loads(json.dumps(result))
                new_scan = Past_scans_nmap(target=target_ip, results=results_dict, user=current_user)
                db.session.add(new_scan)
                db.session.commit()
                # nmap scan is performed on the target ip, within the selected port range.
                # the results come in JSON format and saved in the database as a dictionary
                flash('Scan completed and stored successfully', category='success')

                logging.info(f'New Nmap scan added for user id {current_user.id}')
                logging.info(f'Scan results: {json.dumps(result)}')

                return render_template('nmap.html', nmap_scan_results=nmap_scan_results)
            except ipaddress.AddressValueError:
                flash('Invalid IP address. Please enter a valid IP address.', category='error')
            except Exception as e:
                flash(f'Error: {e}. Please try again.', category='error')

    return render_template('nmap.html', nmap_scan_results=nmap_scan_results)