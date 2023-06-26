from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    # Register blueprints
    from .views import course_bp, course_api_bp, task_bp, task_api_bp, objective_bp, trunk_content_api_bp
    app.register_blueprint(course_api_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(task_api_bp)
    app.register_blueprint(objective_bp)
    app.register_blueprint(trunk_content_api_bp)

    return app
