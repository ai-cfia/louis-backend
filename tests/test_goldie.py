import unittest

from scrapy import Request

from louis.fake_response import fake_response_from_file
from louis.spiders.goldie import GoldieSpider

# get directory of this file
# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory'
import os
cwd = os.path.dirname(os.path.abspath(__file__))


class TestGoldie(unittest.TestCase):

    def setUp(self):
        self.spider = GoldieSpider()
        
    def _test_item_results(self, results, expected_length):
        returned_results = []
        for item in results:
            if isinstance(item, Request):
                # probably a Request object for additional processing
                continue
            self.assertIsNotNone(item['url'])
            returned_results.append(item)
        self.assertEqual(len(returned_results), expected_length)
        return returned_results

    def test_sample1(self):
        url="https://inspection.canada.ca/inspection-and-enforcement/enforcement-of-the-sfcr/eng/1546989322632/1547741756885"
        response = fake_response_from_file(
            f'{cwd}/responses/1547741756885.html', 
            url=url)
        results = self.spider.parse(response)
        results = self._test_item_results(results, 1)
        self.assertEqual(results[0]['title'], 'Enforcement of the Safe Food for Canadians Regulations - Canadian Food Inspection Agency')
        self.assertEqual(results[0]['url'], url)
        self.assertTrue(results[0]['html_content'].startswith(
            '<html><body><main class="container" property="mainContentOfPage" typeof="WebPageElement"> <h1 id="wb-cont" property="name">Enforcement of the <i>Safe Food for Canadians Regulations</i>'))

    def test_sample2(self):
        url="https://inspection.canada.ca/food-safety-for-industry/toolkit-for-food-businesses/understanding-the-sfcr/eng/1492029195746/1492029286734"
        response = fake_response_from_file(
            f'{cwd}/responses/1492029286734.html', 
            url=url)
        results = self.spider.parse(response)
        results = self._test_item_results(results, 1)

if __name__ == '__main__':
    unittest.main()