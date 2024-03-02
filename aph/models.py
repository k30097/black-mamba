from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import JSON

# each class represents a different database model, aka different type of data
# stored. the User database model is the main one, used to link all the others together
# this means that each database entry is related to a different user, which is the only one
# that can see the data on the user page.
# march 2 2024: all scans are implemented.

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    nmap_scans = db.relationship('Past_scans_nmap', backref='user', lazy=True)
    dirbuster_scans = db.relationship('Past_scans_dirbuster', backref='user', lazy=True)
    scraping_scans = db.relationship('Past_scans_scraping', backref='user', lazy=True)
    
class Past_scans_nmap(db.Model):
    nmap_scan_id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(20))
    results = db.Column(JSON)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Past_scans_dirbuster(db.Model):
    dirbuster_scan_id = db.Column(db.Integer, primary_key=True)
    target_url = db.Column(db.String(150))
    results = db.Column(JSON)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Past_scans_scraping(db.Model):
    scraping_scan_id = db.Column(db.Integer, primary_key=True)
    target_url = db.Column(db.String(150))
    results = db.Column(JSON)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))