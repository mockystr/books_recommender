import aiohttp_cors
from api.views import get_recommendation, list_random_books, get_book


def setup_routes(app):
    app.router.add_get('/recommendation', get_recommendation)
    app.router.add_get('/random_books', list_random_books)
    app.router.add_get('/get', get_book)
    
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)
