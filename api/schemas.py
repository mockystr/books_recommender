from marshmallow import Schema, fields, ValidationError, EXCLUDE
from api.utils import books_dict


def validate_book_isbn(value):
    if not books_dict.get(value, None):
        raise ValidationError("Wrong book isbn is given")


class GetBookSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    book_isbn = fields.Str(required=True, validate=validate_book_isbn)


def validate_total_items(value):
    if value != 1:
        raise ValidationError("Total items must be 1")


class GoogleImageLinksSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    thumbnail = fields.Str(required=True)


class GoogleVolumeInfoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=True)
    subtitle = fields.Str(required=False)
    publishedDate = fields.Str(required=False)
    description = fields.Str(required=False)
    pageCount = fields.Int(required=False)
    categories = fields.List(fields.Str(), required=False)
    imageLinks = fields.Nested(GoogleImageLinksSchema)


class GoogleItemsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    volumeInfo = fields.Nested(GoogleVolumeInfoSchema)


class GoogleResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    totalItems = fields.Int(validate=validate_total_items)
    items = fields.Nested(GoogleItemsSchema, many=True)
