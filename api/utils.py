import functools
import json
import os
from aiohttp import web
from marshmallow import ValidationError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def similar_books(model, v, n=10):
    ms = model.similar_by_vector(v, topn=n + 1)[1:]
    return [i[0] for i in ms]


def json_response(data, status=200):
    return web.Response(text=json.dumps(data),
                        headers={'content-type': 'application/json'},
                        status=status)


def arguments_params_get(schema, fields=None):
    if not fields:
        fields = []

    def _arguments(func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            try:
                r = schema().load({**request.query})
            except ValidationError as e:
                return json_response(data={
                    'reason': e.messages,
                    'message': 'bad_request'
                }, status=400)
            data = {f_name: r.get(f_name) for f_name in fields}
            kwargs.update(data)
            return func(request, *args, **kwargs)

        return inner

    return _arguments


books_dict = json.load(open('model/books_dict.json', 'r'))
books_api = 'https://www.googleapis.com/books/v1'
