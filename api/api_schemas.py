from marshmallow import Schema, fields, ValidationError
from api.utils import books_dict


def validate_book_id(value):
    if not books_dict.get(value, None):
        raise ValidationError("Wrong book_id is given")


def validate_n(value):
    if value and value < 0 or value > 15:
        raise ValidationError("Number of books must be positive and"
                              " not more than 15")


class GetRecommendationSchema(Schema):
    book_id = fields.Str(required=True, validate=validate_book_id)
    books_number = fields.Int(required=False, validate=validate_n)


class GetRandomBooksSchema(Schema):
    books_number = fields.Int(required=False, validate=validate_n)
