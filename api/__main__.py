import os

from aiohttp import web
from gensim.models.doc2vec import Doc2Vec

from api.routes import setup_routes
from api.utils import books_dict, books_data


async def create_app():
    app = web.Application()
    app['model'] = Doc2Vec.load('model/book_model')
    app['books_dict'] = books_dict
    app['books_data'] = books_data
    setup_routes(app)

    print('SERVER IS RUNNING')
    return app


web.run_app(create_app(), port=int(os.environ.get('SERVER_PORT', 8000)))
