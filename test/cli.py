import unittest
from src.cli import TransferSanitizer


class TransferSanitizerTest(unittest.TestCase):
    def test_basic(self):
        url = 'https://my-json-server.typicode.com/softrebel/levelUpTask1/entity'
        entity = "#sal&m' "
        transfer = TransferSanitizer(url, entity)
        self.assertEqual(transfer.sendToApi(), {
            'status': 'success',
            'sanitized': '&lt;h1&gt;sal&amp;m&#39;&lt;&#x2F;h1&gt;'
        })


if __name__ == "__main__":
    unittest.main()
