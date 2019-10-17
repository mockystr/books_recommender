from marshmallow import ValidationError

from api.schemas import GetRecommendationSchema
from api.utils import json_response, similar_books
from api.tasks import GetBooksISBNTask


async def recommend(request):
    schema = GetRecommendationSchema()
    try:
        r = schema.load({**request.query})
        book_id = r.get('book_id')
    except ValidationError as e:
        return json_response(data={
            'reason': e.messages,
            'message': 'bad_request'
        }, status=400)

    model = request.app['model']
    books_ids = similar_books(model, model[book_id])
    res = await GetBooksISBNTask(books_ids).main()
    return json_response({'similar': [i for i in res if i]})


async def get_random_books(request):
    books_number = 15
    random_books = []
    return json_response({'books': random_books})
