from flask import Flask, Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
from .models import Past_scans_nmap, Past_scans_dirbuster, Past_scans_scraping
from requests.exceptions import SSLError, MissingSchema
from bs4 import BeautifulSoup
import urllib3.exceptions
from . import db
import jsonify
import logging
import ipaddress
import requests
import nmap
import json

attacks_bp = Blueprint('attacks', __name__)
# wordlist for dirbuster (top 2000 most common directories)
WORDLIST_URL = 'https://raw.githubusercontent.com/digination/dirbuster-ng/master/wordlists/common.txt'
# suppressing warning for SSL dirbusters
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# initialized nmap scanner
scanner = nmap.PortScanner()

@attacks_bp.route('/scraping/', methods=['GET', 'POST'])
@login_required
def scraping():
    if request.method == 'POST':
        target_url = request.form.get('target_url')
        if target_url:
            try:
                # bypass SSL certificate verification by setting verify=False
                response = requests.get(target_url, verify=False)
                if response.ok:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # dictionary to store tag counts
                    tag_counts = {
                        'script': len(soup.find_all('script')),
                        'input': len(soup.find_all('input')),
                        'textarea': len(soup.find_all('textarea')),
                        'select': len(soup.find_all('select')),
                        'a': len(soup.find_all('a')),
                        'iframe': len(soup.find_all('iframe')),
                        'input_file': len(soup.find_all('input', {'type': 'file'}))
                    }
                    print(type(tag_counts))
                    new_scan = Past_scans_scraping(target_url=target_url, results=tag_counts, user=current_user)
                    db.session.add(new_scan)
                    db.session.commit()
                    flash('Scraping completed and stored successfully.', category='success')
                else:
                    flash('Failed to retrieve the webpage. Please check the URL.', category='error')
            except SSLError as ssl_error:
                # log the SSL error or provide feedback to the user
                flash('SSL Error: Failed to establish a secure connection. The SSL certificate could not be verified.', category='error')
            except MissingSchema:
                flash('Invalid URL. Must begin with http:// or https://.', category='error')
            except Exception as e:
                flash(f'An error occurred: {e}', category='error')
    return render_template('scraping.html')

@attacks_bp.route('/dirbuster/', methods=['GET', 'POST'])
# approx. 6 minutes per scan
@login_required
def dirbuster():
    if request.method == 'POST':
        target_url = request.form.get('target_url').rstrip('/')
        if target_url:
            found_directories = []
            try:
                # fetch the wordlist
                response = requests.get(WORDLIST_URL, timeout=10)
                if response.status_code == 200:
                    wordlist = response.text.split('\n') 
                    for directory in wordlist:
                        directory = directory.strip()
                        if directory:
                            full_url = f'{target_url}/{directory}'
                            res = requests.get(full_url, verify=False, timeout=5)
                            if res.status_code == 200:
                                found_directories.append(directory)
                else:
                    flash('failed to download the wordlist.', 'error')
                    return render_template('dirbuster.html')
                if found_directories:
                    new_scan = Past_scans_dirbuster(target_url=target_url, results={"found": found_directories}, user=current_user)
                    db.session.add(new_scan)
                    db.session.commit()
                    flash('Dirbuster scan completed successfully.', 'success')
                else:
                    flash('No directories found.', 'info')
            except Exception as e:
                flash(f'Request failed: {str(e)}', 'error')
                return render_template('dirbuster.html')
    return render_template('dirbuster.html')

@attacks_bp.route('/nmap/', methods=['GET', 'POST'])
# approx. 2 minutes per scan
@login_required
def nmap_scan():
    nmap_scan_results = session.get('nmap_scan_results', {})
    if request.method == 'POST':
        target_ip = request.form.get('ip_address')
        max_port = request.form.get('max_port', None)
        if target_ip:
            try:
                ip_address_obj = ipaddress.ip_address(target_ip)
                # ^ this validates the input and raises an exception
                # validate max_port
                if max_port is not None:
                    try:
                        max_port = int(max_port)
                        if not 1 <= max_port <= 65535:
                            raise ValueError("Port must be between 1 and 65535")
                    except ValueError as e:
                        flash(str(e), 'error')
                        return render_template('nmap.html')
                else:
                    # default if not provided
                    max_port = 10000
                result = scanner.scan(target_ip, f'1-{max_port}')
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