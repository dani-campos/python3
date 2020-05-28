from io import StringIO
import sys
import unittest
from contextlib import redirect_stdout
from authorizer.authorizer import Authorizer

INPUT_1 = """{"transaction": {"merchant": "McDonald's", "amount": 31.5, "time": "2019-02-13T09:00:00.000Z"}}
{"account": {"active-card": true, "available-limit": 100}}
{"account": {"active-card": false, "available-limit": 100}}
{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}
{"transaction": {"merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:00:00.000Z"}}
{"transaction": {"merchant": "Bob's Paulista", "amount": 10, "time": "2019-02-13T12:00:00.000Z"}}
{"transaction": {"merchant": "Bob's Consolacao", "amount": 10, "time": "2019-02-13T12:00:02.000Z"}}
{"transaction": {"merchant": "Bob's Metrô", "amount": 10, "time": "2019-02-13T12:00:04.000Z"}}
{"transaction": {"merchant": "Bob's Metrô", "amount": 10, "time": "2019-02-13T12:00:05.000Z"}}
{"transaction": {"merchant": "Bob's Rodoviaria", "amount": 10, "time": "2019-02-13T12:01:59.000Z"}}"""

OUTPUT_1 = """{"account": null, "violations": ["account-not-initialized"]}
{"account": {"active-card": true, "available-limit": 100}, "violations": []}
{"account": {"active-card": true, "available-limit": 100}, "violations": ["account-already-initialized"]}
{"account": {"active-card": true, "available-limit": 80}, "violations": []}
{"account": {"active-card": true, "available-limit": 80}, "violations": ["insufficient-limit"]}
{"account": {"active-card": true, "available-limit": 70}, "violations": []}
{"account": {"active-card": true, "available-limit": 60}, "violations": []}
{"account": {"active-card": true, "available-limit": 50}, "violations": []}
{"account": {"active-card": true, "available-limit": 50}, "violations": ["high-frequency-small-interval", "doubled-transaction"]}
{"account": {"active-card": true, "available-limit": 50}, "violations": ["high-frequency-small-interval"]}"""

INPUT_CARD_NOT_ACTIVE = """{"account": {"active-card": false, "available-limit": 100}}
{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}"""

OUTPUT_CARD_NOT_ACTIVE = """{"account": {"active-card": false, "available-limit": 100}, "violations": []}
{"account": {"active-card": false, "available-limit": 100}, "violations": ["card-not-active"]}"""


class TestAuthorizerIntegration(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.auth = Authorizer()
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.maxDiff = None
        sys.stdin = StringIO(initial_value=INPUT_1)
        self.captured_output = StringIO()
        self.expected_output_1 = OUTPUT_1

    def test_run_authorizer_whole_output(self):
        with redirect_stdout(self.captured_output):
            self.auth.run()
        self.assertEqual(self.captured_output.getvalue().strip(),
                         self.expected_output_1)
        

class TestAuthorizerIntegrationForCardNotActive(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.auth = Authorizer()
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.maxDiff = None
        sys.stdin = StringIO(initial_value=INPUT_CARD_NOT_ACTIVE)
        self.captured_output = StringIO()
        self.expected_output_2 = OUTPUT_CARD_NOT_ACTIVE

    def test_run_authorizer_whole_output(self):
        with redirect_stdout(self.captured_output):
            self.auth.run()
        self.assertEqual(self.captured_output.getvalue().strip(),
                         self.expected_output_2)


if __name__ == "__main__":
    unittest.main()