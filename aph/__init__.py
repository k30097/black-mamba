from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from os import path
import os
import json

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'black_mamba'
    current_folder = os.path.dirname(os.path.abspath(__file__))
    db_filename = 'api_db.db'
    db_path = os.path.join(current_folder, db_filename)   
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    from .auth import auth_bp
    from .dashboard import dashboard_bp
    from .attacks import attacks_bp
    
    # blueprints are registered
    app.register_blueprint(auth_bp, url_prefix='/auth/')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(attacks_bp, url_prefix='/dashboard/')
    
    from .models import User, Past_scans_scraping, Past_scans_ffuf, Past_scans_nmap
    
    # login manager uses sessions to store user info and 
    # manage login. default session length is 30 days.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # this looks for a user object in the User table.
    @login_manager.user_loader
    def load_user(id):
        if id is not None and id.isdigit():
            return User.query.get(int(id))
        return None
    
    logging.basicConfig(level=logging.INFO)
    
    def from_json(value):
        return json.loads(value)
    
    app.jinja_env.filters['from_json'] = from_json
    
    create_database(app, db_path)
    
    return app


def create_database(app, db_path):
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
            print('created database')