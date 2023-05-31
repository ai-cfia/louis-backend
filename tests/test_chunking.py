# test chunking

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

class TestChunking(unittest.TestCase):
    def test_chunking(self):
        soup = chunk(example1) 
        self.assertEqual(
            soup.select('div.h0-block')[0]['tokens'], 
            "[12156, 11852, 2316, 2132, 11852, 2316, 14646, 3770, 2132, 11852, 2500, 2132, 11852, 14646, 2949, 220, 17, 303, 2237, 4948, 11852, 2316, 14646, 3770, 4948, 11852, 14836, 1566, 1579, 11852, 2316, 11, 45323, 311, 279, 1176]")
        # splitted = split(soup)
        # self.assertEqual(splitted, [example1])