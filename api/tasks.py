import asyncio
import logging

import aiohttp
import asyncpool
from marshmallow import ValidationError

from api.utils import books_api
from api.schemas import GoogleResponseSchema


class DownloadBooksTask:
    def __init__(self, books_isbn, many):
        self.queue = asyncio.Queue()
        self.books_isbn = books_isbn
        self.many = bool(many)
        self.res = [] if self.many else None
        self.loop = asyncio.get_running_loop()

    @staticmethod
    async def handle_response(resp):
        try:
            schema_response = GoogleResponseSchema().load(resp)
            items = schema_response.get('items')[0]
            volume_info = items.get('volumeInfo')
        except ValidationError as e:
            print(e, '\n', resp)
            return

        return {
            'title': volume_info.get('title'),
            'subtitle': volume_info.get('subtitle'),
            'publishedDate': volume_info.get('publishedDate'),
            'description': volume_info.get('description'),
            'page_count': volume_info.get('pageCount'),
            'categories': volume_info.get('categories'),
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail')
        }

    async def link_worker(self, session, book_isbn):
        async with session.get(f'{books_api}/volumes',
                               params={'q': f'isbn:{book_isbn}'}) as resp:
            handled_resp = await self.handle_response(await resp.json())

            if self.many:
                if handled_resp:
                    self.res.append(handled_resp)
            else:
                self.res = handled_resp

    async def main(self):
        async with aiohttp.ClientSession() as session:
            async with asyncpool.AsyncPool(self.loop, num_workers=10,
                                           name="RecPool",
                                           logger=logging.getLogger("RecPool"),
                                           worker_co=self.link_worker,
                                           max_task_time=300) as pool:
                for isbn in self.books_isbn:
                    await pool.push(session, isbn)

        return self.res


class ListBooksISBNTask(DownloadBooksTask):
    def __init__(self, books_isbn):
        super().__init__(books_isbn, many=True)


class GetBookISBNTask(DownloadBooksTask):
    def __init__(self, book_isbn):
        super().__init__([book_isbn], many=False)
