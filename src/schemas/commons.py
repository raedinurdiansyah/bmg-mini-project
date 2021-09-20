from datetime import datetime

from marshmallow import EXCLUDE, Schema, fields, post_dump


class BaseResponseSchema(Schema):
    "This class is base schema for API response"

    code = fields.Integer()
    timestamp = fields.DateTime(default=lambda: datetime.utcnow())

    class Meta:
        ordered = True


class ErrorSchema(Schema):
    "This class is base schema for API error response"

    code = fields.Integer()
    message = fields.String(required=True)


class DefaultResponseSchema(BaseResponseSchema):
    "This class is default response for API success or failed"

    data = fields.Field(missing=None, default={})
    errors = fields.Nested(ErrorSchema(many=True, unknown=EXCLUDE))
    message = fields.String(default="", missing="")

    @post_dump(pass_many=True)
    def remove_skip_values(self, data, **kwargs):
        """to remove the useless field"""
        dict_copy = data.copy()

        for key, value in data.items():
            if value is None or value == {}:
                dict_copy.pop(key, None)

        return dict_copy
