import unittest
import dotenv

from louis.agent.chain import ChainAgent

dotenv.load_dotenv()

class TestChainAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = ChainAgent()
        self.maxDiff = None

    def test_basic_query(self):
        response = self.agent.run("What does the acronym CFIA stand for? Only answer with the expanded acronym.")
        self.assertIn('input', response)
        self.assertIn('output', response)
        self.assertIn('intermediate_steps', response)
        self.assertEqual(response['output'], 'Canadian Food Inspection Agency')

    def test_name(self):
        response = self.agent.run("In 2023, who is the president of the CFIA? Name only in the answer.")
        self.assertEqual(response['output'], 'Dr. Harpreet S. Kochhar')

    def test_inspectors(self):
        response = self.agent.run("For the most recent year, how many employees work at the CFIA? answer only with the following number of FTE followed by the source of the information. brief machine-readable answer.")
        self.assertEqual(response['output'], '6,546 FTEs in 2021-2022, source: 2021 to 2022 CFIA full-time equivalents - Canadian Food Inspection Agency from https://inspection.canada.ca/about-cfia/transparency/regulatory-transparency-and-openness/inspection-capacity/2021-to-2022-cfia-full-time-equivalents/eng/1668618113194/1668618113538')