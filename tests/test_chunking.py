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

EXPECTED_TOKENS = "[12156, 11852, 2316, 5686, 11852, 2316, 28827, 3770, 2132, 11852, 43063, 2132, 11852, 28827, 2949, 220, 17, 303, 2237, 32827, 11852, 2316, 28827, 3770, 4948, 11852, 14836, 4354, 1579, 11852, 2316, 11, 45323, 311, 279, 1176]"

CWD = os.path.dirname(os.path.abspath(__file__))

class TestChunking(unittest.TestCase):
    def test_chunking(self):
        soup, splitted = chunk(example1) 
        self.assertEqual(
            soup.select('body.h0-block')[0]['tokens'], EXPECTED_TOKENS)
        splitted = split(soup)
        #print(splitted)
        self.assertEqual(splitted[0][1], EXPECTED_TOKENS)

    def test_chunking_sample1(self):
        with open(f"{CWD}/responses/1547741756885.html") as f:
            html = f.read()
        soup, splitted = chunk(html)
        print(soup)
        print(splitted)

    def test_chunking_sample2(self):
        with open(f"{CWD}/responses/1430250287405.html") as f:
            html = f.read()
        soup, splitted = chunk(html)

    def test_chunking_fragment2(self):
        with open(f"{CWD}/responses/fragment2.html") as f:
            html = f.read()
        soup, splitted = chunk(html)
        self.assertEqual(splitted[0][0], "Z Zoonose ( Zoonosis ) Le terme « zoonose » n'est pas employé dans la Loi sur la salubrité des aliments au Canada ni dans le Règlement sur la salubrité des aliments au Canada . En général, le terme « zoonose » indique infection ou maladie pouvant être transmise entre les animaux et les humains.")