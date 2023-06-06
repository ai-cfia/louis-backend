"""Test the Kurt spider"""
import unittest
import os

from louis.spiders.kurt import KurtSpider

from louis.responses import response_from_chunk_token

class TestKurt(unittest.TestCase):
    """Test the Kurt spider"""
    def setUp(self):
        self.spider = KurtSpider()

    def test_sample1(self):
        """Test that the spider returns a request for each chunk_id"""
        data = {
            'tokens': list(range(0,100))
        }
        response = response_from_chunk_token(data, 'https://example.com/path')
        item = yield from self.spider.parse(response)
        self.assertEqual(item['chunk_id'], 'https://example.com/path')
