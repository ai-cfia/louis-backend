import unittest

from responses import fake_response_from_file
from louis.spiders.goldie import GoldieSpider

class TestGoldie(unittest.TestCase):

    def setUp(self):
        self.spider = GoldieSpider()
        
    def _test_item_results(self, results, expected_length):
        returned_results = []
        for item in results:
            self.assertIsNotNone(item['url'])
            self.assertIsNotNone(item['title'])
            self.assertIsNotNone(item['subtitle'])
            returned_results.append(item)
        self.assertEqual(len(returned_results), expected_length)
        return returned_results

    def test_sample1(self):
        url="https://inspection.canada.ca/inspection-and-enforcement/enforcement-of-the-sfcr/eng/1546989322632/1547741756885"
        response = fake_response_from_file(
            '1547741756885.html', 
            url=url)
        results = self.spider.parse(response)
        results = self._test_item_results(results, 3)
        self.assertEqual(results[0]['title'], 'Enforcement of the Safe Food for Canadians Regulations')
        self.assertEqual(results[0]['subtitle'], 'How is CFIA enforcing the SFCR?')
        self.assertEqual(results[0]['url'], url)
        self.assertTrue(results[0]['content'].startswith(
            "CFIA's enforcement approach to the SFCR balances the need to protect Canada's food safety"))

    def test_sample2(self):
        url="https://inspection.canada.ca/food-safety-for-industry/toolkit-for-food-businesses/understanding-the-sfcr/eng/1492029195746/1492029286734"
        response = fake_response_from_file(
            '1492029286734.html', 
            url=url)
        results = self.spider.parse(response)
        results = self._test_item_results(results, 7)

if __name__ == '__main__':
    unittest.main()