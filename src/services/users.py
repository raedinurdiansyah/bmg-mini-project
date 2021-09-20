from http import HTTPStatus

from flask import current_app
from sqlalchemy import func

from src import db
from src.models.users import ReferralUsers, Users
from src.schemas.auth import UserSchema
from src.utils.auth import get_digest
from src.utils.handle_response import default_response


class UserServices:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.referral_code = kwargs.get("referral_code")

    @staticmethod
    def _get_user(params: dict, return_query: bool = False) -> Users:
        user_query = Users.query.filter_by(is_deleted=False)
        if params.get("keywords"):
            user_query = user_query.filter(
                Users.name.ilike(f"%{params.get('keywords')}%"),
            )
        else:
            if params.get("id"):
                user_query = user_query.filter(Users.id == params.get("id"))
            if params.get("name"):
                user_query = user_query.filter(
                    func.lower(Users.name) == func.lower(params.get("name"))
                )
            if params.get("email"):
                user_query = user_query.filter(
                    func.lower(Users.email) == func.lower(params.get("email"))
                )
            if params.get("username"):
                user_query = user_query.filter(
                    func.lower(Users.username) == func.lower(params.get("username"))
                )

        if return_query:
            return user_query
        else:
            return user_query.first()

    @staticmethod
    def generate_referral_code(id: int, name: str) -> str:
        fname = name.split(" ")[0]
        return f"{current_app.config.get('REF_TEMPLATE')}{fname.upper()}{id}"

    @staticmethod
    def check_referral(ref_code: str) -> dict:
        parsed_code = ref_code[:3]
        if parsed_code == current_app.config.get("REF_TEMPLATE"):
            referral_exist = (
                ReferralUsers.query.filter_by(is_deleted=False)
                .filter(func.lower(ReferralUsers.referral_code) == func.lower(ref_code))
                .first()
            )
            if referral_exist:
                return dict(
                    user_id=referral_exist.user_id,
                    referral_code=referral_exist.referral_code,
                )

        return {}

    def get_users(self, **params):
        # TODO use pagination
        user_query = self._get_user(params, return_query=True)
        if user_query.count() == 0:
            return default_response(data=[])

        return default_response(data=UserSchema(many=True).dump(user_query))

    def create(self, do_commit: bool = False) -> default_response:
        """To create new user"""
        try:
            user_exist = self._get_user({"username": self.username})
            if user_exist:
                raise Exception("User already registered")

            ref_data = None
            if self.referral_code:
                ref_data = self.check_referral(self.referral_code)
                if not ref_data:
                    raise Exception("Invalid referral code")
        except Exception as e:
            return default_response(
                status=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e), data=[]
            )

        salt, salted_pwd = get_digest(self.password)

        user_params = dict(
            email=self.email,
            username=self.username,
            name=self.name,
            password=salted_pwd,
            salt=salt.decode("utf=8"),
        )
        user = Users(**user_params)
        db.session.add(user)
        db.session.flush()

        ref_code = self.generate_referral_code(user.id, user.name)

        ref_params = dict(user_id=user.id, referral_code=ref_code)
        if self.referral_code and ref_data:
            ref_params["referrer_id"] = ref_data["user_id"]

        ref_user = ReferralUsers(**ref_params)
        db.session.add(ref_user)

        try:
            if do_commit:
                db.session.commit()
            else:
                db.session.flush()
        except Exception:
            db.session.rollback()

        return default_response(
            status=HTTPStatus.CREATED, message="Register is success", data=[]
        )

    def update_user(self, **params) -> default_response:
        """To update username, name, and email"""
        user = self._get_user({"id": self.id})
        if not user:
            return default_response(
                status=HTTPStatus.UNPROCESSABLE_ENTITY, message="Invalid user", data=[]
            )

        for key, value in params.items():
            setattr(user, key, value)

        db.session.add(user)
        return default_response(
            data=UserSchema(only=["id", "updated", "username", "email", "name"]).dump(
                user
            ),
            message="User successfully updated",
        )

    def insert_referral(self):
        try:
            ref_data = self.check_referral(self.referral_code)
            if not ref_data:
                raise Exception("Invalid referral code")

            user = self._get_user({"id": self.id})
            if not user:
                raise Exception("Invalid User")

            user_referral = ReferralUsers.query.filter_by(
                user_id=user.id, is_deleted=False
            ).first()

            if user_referral.referrer_id:
                raise Exception("Cannot input referral more than one")
        except Exception as e:
            return default_response(
                status=HTTPStatus.UNPROCESSABLE_ENTITY, message=e, data=[]
            )

        user_referral.referrer_id = ref_data["user_id"]
        db.session.add(user_referral)

        return default_response(message="Input referral success", data=[])
