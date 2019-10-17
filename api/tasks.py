import asyncio
import logging

import aiohttp
import asyncpool

from api.utils import books_api


class GetBooksTask:
    @staticmethod
    async def handle_response(resp):
        total_items = resp.get('totalItems')
        if total_items != 1:
            print(resp)
            return
        items = resp.get('items', [])[0]
        volume_info = items.get('volumeInfo')

        return {
            'title': volume_info.get('title'),
            'subtitle': volume_info.get('subtitle'),
            'publishedDate': volume_info.get('publishedDate'),
            'description': volume_info.get('description'),
            'page_count': volume_info.get('pageCount'),
            'categories': volume_info.get('categories'),
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail')
        }


class GetBooksISBNTask(GetBooksTask):
    def __init__(self, books_ids):
        self.queue = asyncio.Queue()
        self.books_ids = books_ids
        self.res = []
        self.loop = asyncio.get_running_loop()

    async def rec_link_worker(self, session, book_isbn):
        async with session.get(f'{books_api}/volumes',
                               params={'q': f'isbn:{book_isbn}'}) as resp:
            self.res.append(await self.handle_response(await resp.json()))

    async def main(self):
        async with aiohttp.ClientSession() as session:
            async with asyncpool.AsyncPool(self.loop, num_workers=10,
                                           name="RecPool",
                                           logger=logging.getLogger("RecPool"),
                                           worker_co=self.rec_link_worker,
                                           max_task_time=300) as pool:
                for book in self.books_ids:
                    await pool.push(session, book)

        return self.res
