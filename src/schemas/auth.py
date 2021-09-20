from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import Schema, ValidationError, fields, post_load

from src.models.users import Users
from src.utils.auth import validate_email as val_email


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        ordered = True


class UserAuthSchema(UserSchema):
    @post_load
    def validate_email(self, in_data, **kwargs):
        email = val_email(in_data["email"])
        if not email:
            raise ValidationError("Invalid email format")

        return in_data


class GetUserSchema(Schema):
    keywords = fields.String(
        required=False, default=None, allow_none=True, missing=None
    )


class RegisterSchema(UserAuthSchema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)
    name = fields.String(required=True)
    referral_code = fields.String(allow_none=True, default=None, missing=None)

    class Meta:
        exclude = ["is_deleted", "deleted", "salt"]

    # referral_code = fields.String(missing=None, default=None)


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class InsertReferralSchema(Schema):
    id = fields.Integer(required=True)
    referral_code = fields.String(required=True)
