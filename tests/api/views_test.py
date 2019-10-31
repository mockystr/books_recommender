class TestRandomBooks:
    async def test_check_len(self, cli):
        resp = await cli.get('/random_books')
        assert resp

        data = await resp.json()
        books = data.get('books')
        assert len(books) == 11


class TestGetRecommendation:
    async def test_response_status(self, cli):
        resp = await cli.get('/recommendation')
        assert resp.status in [200, 400]
