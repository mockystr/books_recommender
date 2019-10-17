import json
import os
from aiohttp import web

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def similar_books(model, v, n=10):
    ms = model.similar_by_vector(v, topn=n + 1)[1:]
    return [i[0] for i in ms]


def json_response(data, status=200):
    return web.Response(text=json.dumps(data),
                        headers={'content-type': 'application/json'},
                        status=status)


books_dict = json.load(open('model/books_dict.json', 'r'))
books_api = 'https://www.googleapis.com/books/v1'
