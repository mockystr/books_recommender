import json
import os
from aiohttp import web

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def similar_books(model, v, n=15):
    ms = model.similar_by_vector(v, topn=n + 1)[1:]

    new_ms = []
    for j in ms:
        pair = (books_dict[j[0]][0], j[1])
        new_ms.append(pair)

    return new_ms


def json_response(data, status=200):
    return web.Response(text=json.dumps(data),
                        headers={'content-type': 'application/json'},
                        status=status)


books_dict = json.load(open('model/books_dict.json', 'r'))
