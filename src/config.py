from os import environ

from dotenv import load_dotenv

load_dotenv(".env")


class Config:
    """Set Flask configuration from .env file"""

    # Database
    DB_NAME = environ.get("DB_NAME", "bmg")
    DB_USER = environ.get("DB_USER", "bmg")
    DB_PASS = environ.get("DB_PASS", "password")
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_PORT = environ.get("DB_PORT", "5432")

    # SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = environ.get("SECRET_KEY", "hard-and-random-string")
    HERO_URL = environ.get(
        "HERO_URL",
        "https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json",
    )
    REF_TEMPLATE = environ.get("REF_TEMPLATE", "BMG")
