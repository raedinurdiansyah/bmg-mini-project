import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.models import load_models

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app() -> Flask:
    load_models(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("src.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from src.routers import register_routes

        register_routes(app)

        return app
