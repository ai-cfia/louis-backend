import unittest
import dotenv

from louis.agent.chain import ChainAgent

dotenv.load_dotenv()

class TestChainAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = ChainAgent()

    def test_basic_query(self):
        retvalue = self.agent.run("What does the acronym CFIA stand for? Only answer with the expanded acronym.")
        self.assertEqual(retvalue, 'Canadian Food Inspection Agency')

    def test_name(self):
        retvalue = self.agent.run("In 2023, who is the president of the CFIA? Name only in the answer.")
        self.assertEqual(retvalue, 'Dr. Harpreet S. Kochhar')