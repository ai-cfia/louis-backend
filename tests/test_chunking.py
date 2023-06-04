# test chunking

import os
import unittest

from bs4 import BeautifulSoup

from louis.chunking import segment_blocks_into_chunks, chunk

EXAMPLE1 = (
    "<h1>high-level title</h1>"
    "<h2>second-level title</h2>"
    "<p>paragraph below second-level</p>"
    "<h2>another second-level</h2>"
    "<p>paragraph within 2nd level</p>"
    "<h3>third-level title</h3>"
    "<p>paragraph below third-level heading</p>"
    "<h1>last high-level title, sibling to the first</h1>"
)


EXPECTED_TOKENS = [
    12156,
    11852,
    2316,
    5686,
    11852,
    2316,
    28827,
    3770,
    2132,
    11852,
    43063,
    2132,
    11852,
    28827,
    2949,
    220,
    17,
    303,
    2237,
    32827,
    11852,
    2316,
    28827,
    3770,
    4948,
    11852,
    14836,
    4354,
    1579,
    11852,
    2316,
    11,
    45323,
    311,
    279,
    1176,
]

CWD = os.path.dirname(os.path.abspath(__file__))


class TestChunking(unittest.TestCase):
    def test_chunking(self):
        soup, chunks = chunk(EXAMPLE1)
        #print(chunks)
        # print(chunks[0]['tokens'])
        self.assertEqual(chunks[0]["tokens"], EXPECTED_TOKENS)
        titles = [c["title"] for c in chunks]
        self.assertEqual(
            chunks[0]["title"],
            "high-level title",
        )

    def test_chunking_sample1(self):
        with open(f"{CWD}/responses/1547741756885.html", encoding="UTF-8") as f:
            html = f.read()
        soup, chunks = chunk(html)
        # sentences = []
        # text_content = ''
        # for c in chunks:
        #     text_content += c['text_content']
        # split_text = [s.strip() for s in text_content.split('.')]
        # print(split_text)
        # self.assertEqual(sentences, split_text)

    def test_chunking_sample2(self):
        with open(f"{CWD}/responses/1430250287405.html", encoding="UTF-8") as f:
            html = f.read()
        soup, chunks = chunk(html)
        # sentences = soup.get_text(strip=True).split('.')
        # text_content = ''
        # for c in chunks:
        #     text_content += c['text_content']
        # split_text = [s.strip() for s in text_content.split('.')]
        # print(split_text)
        # self.assertEqual(sentences, split_text)
        titles = [c["title"] for c in chunks]
        unique_titles_sorted = sorted(list(set(titles)))
        #print(unique_titles_sorted)
        self.assertEqual(unique_titles_sorted, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'Z', 'À retenir'])
        #print(chunks)
        #print(soup.prettify())

    def test_chunking_fragment2(self):
        with open(f"{CWD}/responses/fragment2.html", encoding="UTF-8") as f:
            html = f.read()
        soup, chunks = chunk(html)
        # print(soup.prettify())
        # print(chunks)
        self.assertEqual(
            chunks[0]["text_content"],
            "Z Zoonose (Zoonosis) Le terme « zoonose » n'est pas employé dans la Loi sur la salubrité des aliments au Canada ni dans le Règlement sur la salubrité des aliments au Canada. En général, le terme « zoonose » indique infection ou maladie pouvant être transmise entre les animaux et les humains.",
        )
        self.assertEqual(chunks[0]["title"], "Glossary")

    def test_block_by_heading(self):
        with open(f"{CWD}/responses/wrapped.html", encoding="UTF-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "lxml")
        chunks = segment_blocks_into_chunks(soup)
