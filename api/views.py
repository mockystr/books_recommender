from api.schemas import GetBookSchema
from api.utils import json_response, similar_books, arguments_params_get
from api.tasks import (
    ListRandomFromFileTask,
    ListBooksFromFileByISBNTask
)


@arguments_params_get(schema=GetBookSchema, fields=['book_isbn'])
async def get_recommendation(request, book_isbn):
    model = request.app['model']

    try:
        books_isbn = similar_books(model, model[book_isbn])
    except KeyError:
        return json_response({
            'message': 'Error while trying get similar books.'
            f'Maybe ISBN {book_isbn} not in vocabulary',
            'status': 'error'
        }, status=400)
    else:
        books_data = request.app['books_data']
        res = await ListBooksFromFileByISBNTask(books_data, books_isbn).main()
        return json_response({'books': res})


@arguments_params_get(schema=GetBookSchema, fields=['book_isbn'])
async def get_book(request, book_isbn):
    books_data = request.app['books_data']
    res = ListBooksFromFileByISBNTask(books_data, [book_isbn]).main()
    if len(res) != 1:
        message = f'Cannot get exactly this book with given ISBN {book_isbn}'
        return json_response({'message': message, 'status': 'error'},
                             status=400)
    return json_response({'book': res})


async def list_random_books(request):
    books_count = 10
    res = ListRandomFromFileTask(request.app['books_data'], books_count).main()
    return json_response({'books': res})
