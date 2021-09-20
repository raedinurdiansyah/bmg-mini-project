from src import db
from src.models.commons import BaseModel


class Token(BaseModel):
    __tablename__ = "token"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    token = db.Column(db.String(500))
    expires = db.Column(db.DateTime)
    is_active = db.Column(
        db.Boolean, default=True, nullable=False, server_default="true"
    )
