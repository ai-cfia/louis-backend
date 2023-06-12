import flask_unittest


class TestSmartSearch(flask_unittest.AppTestCase):
    def create_app(self):
        from louis.api.smartsearch import app
        return app

    def test_basic_query(self, app):
        with app.test_client() as client:
            rv = client.post('/search', json={'query': "What is the CFIA?"})
            self.assertEqual(len(rv.json), 10)
