from sqlalchemy.orm import backref, relationship

from src import db
from src.models.commons import BaseModel


class Users(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(25), nullable=False, unique=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    # TODO add uuid


class ReferralUsers(BaseModel):
    __tablename__ = "referral_users"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship(
        "Users", lazy="joined", backref=backref("referral_user", uselist=False)
    )
    referral_code = db.Column(db.String(100), nullable=True)
    referrer_id = db.Column(db.Integer, nullable=True)
