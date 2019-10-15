from pandas import DataFrame
from marshmallow import ValidationError

from api.api_schemas import GetRecommendationSchema, GetRandomBooksSchema
from api.utils import json_response, similar_books


async def recommend(request):
    schema = GetRecommendationSchema()
    try:
        r = schema.load({**request.query})
        book_id, books_number = r.get('book_id'), r.get('books_number', 15)
    except ValidationError as e:
        return json_response(data={
            'reason': e.messages,
            'message': 'bad_request'
        }, status=400)

    model = request.app['model']
    similar = similar_books(model, model[book_id], books_number)
    return json_response({'similar': similar, 'status': 'ok'})


async def get_random_books(request):
    schema = GetRandomBooksSchema()
    try:
        r = schema.load({**request.query})
        books_number = r.get('books_number', 15)
    except ValidationError as e:
        return json_response(data={
            'reason': e.messages,
            'message': 'bad_request'
        }, status=400)

    df: DataFrame = request.app['books_table']
    random_samples: DataFrame = df.sample(n=books_number)
    random_books = []
    for index, row in random_samples.iterrows():
        random_books.append({
            'ISBN': row['ISBN'],
            'BookTitle': row['Book-Title'],
            'ImageURL': row['Image-URL-L'],
            'YearOfPublication': row['Year-Of-Publication'],
            'BookRating': row['Book-Rating'],
            'BookAuthor': row['Book-Author']
        })
    return json_response({'books': random_books})
