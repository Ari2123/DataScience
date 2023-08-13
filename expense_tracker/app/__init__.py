import os
from flask import Flask
from .models import db

# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'a_default_fallback_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
    
    db.init_app(app)

    @app.cli.command("initdb")
    def initdb_command():
        """Initialize the database."""
        db.create_all()
        print("Initialized the database.")

    from . import routes
    app.register_blueprint(routes.bp)

    return app
