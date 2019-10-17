from marshmallow import Schema, fields, ValidationError
from api.utils import books_dict


def validate_book_id(value):
    if not books_dict.get(value, None):
        raise ValidationError("Wrong book_id is given")


class GetRecommendationSchema(Schema):
    book_id = fields.Str(required=True, validate=validate_book_id)


def validate_total_items(value):
    if value != 1:
        raise ValidationError("Total items must be 1")


class RecommendImageLinksSchema(Schema):
    class Meta:
        strict = True

    thumbnail = fields.Str(required=True)


class RecommendVolumeInfoSchema(Schema):
    class Meta:
        strict = True

    title = fields.Str(required=True)
    subtitle = fields.Str(required=False)
    publishedDate = fields.Str(required=False)
    description = fields.Str(required=False)
    pageCount = fields.Int(required=False)
    categories = fields.List(fields.Str(), required=False)
    imageLinks = fields.Nested(RecommendImageLinksSchema, load_only=True,
                               only=('thumbnail',))


class RecommendItemsSchema(Schema):
    class Meta:
        strict = True

    volumeInfo = fields.Nested(
        RecommendVolumeInfoSchema,
        load_only=True,
        only=('title', 'subtitle', 'publishedDate', 'description',
              'description', 'pageCount', 'categories', 'imageLinks')
    )


class RecommendLinkSchema(Schema):
    class Meta:
        strict = True

    totalItems = fields.Int(validate=validate_total_items)
    items = fields.Nested(RecommendItemsSchema, many=True, load_only=True,
                          only=('volumeInfo',))
    kind = fields.Str()
