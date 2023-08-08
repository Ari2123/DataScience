from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '212123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from . import routes
    app.register_blueprint(routes.bp)
    return app
