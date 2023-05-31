# test chunking

import os
import unittest

from louis.chunking import chunk, split

example1 = ('<h1>high-level title</h1>'
                '<h2>second-level title</h2>'
                    '<p>paragraph below second-level</p>'
                '<h2>another second-level</h2>'
                    '<p>paragraph within 2nd level</p>'
                    '<h3>third-level title</h3>'
                        '<p>paragraph below third-level heading</p>'
            '<h1>last high-level title, sibling to the first</h1>')

EXPECTED_TOKENS = "[12156, 11852, 2316, 2132, 11852, 2316, 14646, 3770, 2132, 11852, 2500, 2132, 11852, 14646, 2949, 220, 17, 303, 2237, 4948, 11852, 2316, 14646, 3770, 4948, 11852, 14836, 1566, 1579, 11852, 2316, 11, 45323, 311, 279, 1176]"

CWD = os.path.dirname(os.path.abspath(__file__))

class TestChunking(unittest.TestCase):
    def test_chunking(self):
        soup = chunk(example1) 
        self.assertEqual(
            soup.select('div.h0-block')[0]['tokens'], EXPECTED_TOKENS)
        splitted = split(soup)
        self.assertEqual(splitted[0][1], EXPECTED_TOKENS)

    def test_chunking_sample1(self):
        with open(f"{CWD}/responses/1547741756885.html") as f:
            html = f.read()
        soup = chunk(html)
        # print(soup)
        splitted = split(soup)
        # print(splitted)