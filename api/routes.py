import aiohttp_cors
from api.views import recommend


def setup_routes(app):
    app.router.add_get('/recommend', recommend)
    # app.router.add_get('/get_random_books', get_random_books)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)
