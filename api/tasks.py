import asyncio
import logging
import os

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
    async def handle_response(resp, book_isbn):
        try:
            schema_response = GoogleResponseSchema().load(resp)
        except ValidationError as e:
            print(e, resp, book_isbn)
            return

        try:
            items = schema_response.get('items')[0]
            volume_info = items.get('volumeInfo')
        except (TypeError, KeyError) as e:
            print(e, resp, book_isbn)
            return

        return {
            'book_isbn': book_isbn,
            'title': volume_info.get('title'),
            'subtitle': volume_info.get('subtitle'),
            'publishedDate': volume_info.get('publishedDate'),
            'description': volume_info.get('description'),
            'page_count': volume_info.get('pageCount'),
            'categories': volume_info.get('categories'),
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail')
        }

    async def link_worker(self, session, book_isbn):
        link_params = {
            'q': f'isbn:{book_isbn}',
            'key': os.getenv('GOOGLE_API_KEY', '')
        }
        async with session.get(f'{books_api}/volumes',
                               params=link_params) as resp:
            handled_resp = await self.handle_response(await resp.json(),
                                                      book_isbn)

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


class ListGoogleBooksISBNTask(DownloadBooksTask):
    def __init__(self, books_isbn):
        super().__init__(books_isbn, many=True)


class GetGoogleBookISBNTask(DownloadBooksTask):
    def __init__(self, book_isbn):
        super().__init__([book_isbn], many=False)


class FromFileTask:
    def __init__(self, books_data):
        self.books_data = books_data
        self.res = []

    def handle_row(self, row):
        return self.res.append({
            'book_isbn': row['ISBN'],
            'title': row['book_title'],
            'book_author': row['book_author'],
            'image_url': row['image_url'],
            'publication_year': row['publication_year'],
            'publisher': row['publisher']
        })


class ListRandomFromFileTask(FromFileTask):
    def __init__(self, books_data, books_count):
        super().__init__(books_data)
        self.books_count = books_count

    def main(self):
        random_samples = self.books_data.sample(n=self.books_count)
        random_books = []
        for index, row in random_samples.iterrows():
            random_books.append(self.handle_row(row))
        return self.res


class ListBooksFromFileByISBNTask(FromFileTask):
    def __init__(self, books_data, books_isbn):
        super().__init__(books_data)
        self.books_isbn = books_isbn

    def main(self):
        books = self.books_data[self.books_data['ISBN'].isin(self.books_isbn)]

        handled_books = []
        for index, row in books.iterrows():
            handled_books.append(self.handle_row(row))
        return self.res
