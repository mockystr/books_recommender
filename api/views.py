import random

from api.schemas import GetBookSchema
from api.utils import json_response, similar_books, arguments_params_get
from api.tasks import ListBooksISBNTask, GetBookISBNTask


@arguments_params_get(schema=GetBookSchema, fields=['book_isbn'])
async def get_recommendation(request, book_isbn):
    model = request.app['model']
    books_isbn = similar_books(model, model[book_isbn])
    res = await ListBooksISBNTask(books_isbn).main()
    return json_response({'books': res})


@arguments_params_get(schema=GetBookSchema, fields=['book_isbn'])
async def get_book(request, book_isbn):
    return json_response({'book': await GetBookISBNTask(book_isbn).main()})


async def list_random_books(request):
    books_count = 10
    books_isbn = list(request.app['books_dict'])
    random_indexes = random.sample(range(len(books_isbn)), books_count)
    random_isbn = [books_isbn[i] for i in random_indexes]
    res = await ListBooksISBNTask(random_isbn).main()
    return json_response({'books': res})
