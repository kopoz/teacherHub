from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    from .views import task_api_bp, task_bp
    app.register_blueprint(task_bp)
    app.register_blueprint(task_api_bp)

    return app
