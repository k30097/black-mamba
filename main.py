from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from auth import auth_bp
from dashboard import dashboard_bp
from attacks import attacks_bp
import os

# app backbone. everything is initialized here
app = Flask(__name__)
db = SQLAlchemy()
current_folder = os.path.dirname(os.path.abspath(__file__))
db_filename = 'api_db.db'
db_path = os.path.join(current_folder, db_filename)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'black_mamba'
db.init_app(app)

# blueprints are registered
app.register_blueprint(auth_bp, url_prefix='/auth/')
app.register_blueprint(dashboard_bp, url_prefix='/')
app.register_blueprint(attacks_bp, url_prefix='/features/')


# the app starts when this file is run
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)