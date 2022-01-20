# Import flask and template operators
from flask import Flask
from flask_login import LoginManager


# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Import a module / component using its blueprint handler variable (mod_auth)
from app.routes.main import main
from app.routes.content_set import content_set
from app.routes.user_login import user_login
from app.routes.content import content
from app.routes.countries import countries
from app.routes.location import location
from app.routes.region import region


db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'user_login.login_user_page'
login_manager.init_app(app)

from .models import  User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
        
# Register blueprint(s)
app.register_blueprint(main)
app.register_blueprint(content_set)
app.register_blueprint(user_login)
app.register_blueprint(content)
app.register_blueprint(countries)
app.register_blueprint(location)
app.register_blueprint(region)

# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy


db.create_all()