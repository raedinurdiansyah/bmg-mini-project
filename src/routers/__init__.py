from src.routers.auth import auth_blueprint
from src.routers.hero import hero_blueprint
from src.routers.users import user_blueprint


def register_routes(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(hero_blueprint)
    app.register_blueprint(user_blueprint)
