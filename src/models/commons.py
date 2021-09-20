from datetime import datetime

from src import db


class ID(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)


class Timestamp(db.Model):
    __abstract__ = True

    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Deletable(db.Model):
    __abstract__ = True

    is_deleted = db.Column(
        db.Boolean(), default=False, nullable=False, server_default="false"
    )
    deleted = db.Column(db.DateTime, default=None, nullable=True)


class BaseModel(ID, Timestamp, Deletable):
    """
    This class is the abstract model that inherited from other model
    """

    __abstract__ = True
