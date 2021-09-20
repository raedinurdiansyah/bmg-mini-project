from marshmallow import Schema, fields


class InfoHeroSchema(Schema):
    attack = fields.Integer()
    defense = fields.Integer()
    magic = fields.Integer()
    difficulty = fields.Integer()


class ImageSchema(Schema):
    pass


class GetHeroSchema(Schema):
    version = fields.String()
    id = fields.String(default=None, missing=None)
    key = fields.String()
    name = fields.String()
    title = fields.String()
    blurb = fields.String()
    info = fields.Dict()
    image = fields.Dict()
    tags = fields.List(fields.Str())
    partype = fields.String()
    stats = fields.Dict()
