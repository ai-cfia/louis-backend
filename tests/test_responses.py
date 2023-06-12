import unittest

import louis.crawler.responses as responses

class TestResponses(unittest.TestCase):
    def test_response_from_chunk_token(self):
        row = {
            'tokens': [1,2,3]
        }
        response = responses.response_from_chunk_token(row, 'https://example.com/path')
        json = response.json()
        self.assertEqual(json['tokens'], [1,2,3])