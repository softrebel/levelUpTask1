import unittest, sys, os

# region for
project_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_folder)
# endregion
from src.cli import TransferSanitizer


class TransferSanitizerTest(unittest.TestCase):
    def test_basic(self):
        url = 'https://my-json-server.typicode.com/softrebel/levelUpTask1/entity'
        entity = "#sal&m' "
        transfer = TransferSanitizer(url, entity)
        self.assertEqual(transfer.send_to_api(), {
            'status': 'success',
            'sanitized': '&lt;h1&gt;sal&amp;m&#39;&lt;&#47;h1&gt;'
        })

    def test_markdown(self):
        self.assertEqual(TransferSanitizer.markdown_to_html('# <h1> tag & <b> tag '),
                         '<h1><h1> tag &amp; <b> tag</h1>')

    def test_escape(self):
        self.assertEqual(TransferSanitizer.escape('<h1>&"</h1>'),
                         '&lt;h1&gt;&amp;&quot;,&lt;&#47;h1&gt;')

    def test_escape_with_other_escape_chars(self):
        self.assertEqual(TransferSanitizer.escape('<h1>&s</h1>', {'<': '<>', '&': 'amper', 's': 'sand'}),
                         '<>h1>ampersand<>/h1>')

    def test_post_data(self):
        url = 'https://my-json-server.typicode.com/softrebel/levelUpTask1/entitys'
        self.assertEqual(TransferSanitizer.post_data(url, '&lt;h1&gt;&amp;&quot;,&lt;&#47;h1&gt;'), {
            'status': 'failed',
            'sanitized': '&lt;h1&gt;&amp;&quot;,&lt;&#47;h1&gt;'
        })

    def test_filter(self):
        self.assertEqual(TransferSanitizer.filter('<script>alert("hi");</script>'), 'alert("hi");')

    def test_filter_with_other_remove_chars(self):
        self.assertEqual(TransferSanitizer.filter('<script>alert("hi");</script>', ['alert']),
                         '<script>("hi");</script>')

    def test_validate(self):
        pass

    def test_sanitize(self):
        self.assertEqual(TransferSanitizer.sanitize('<script>alert(" \'jAck\' & \'Jill\' ");</script>', priority='fe'),
                         'alert(&quot;, &#39;jAck&#39; &amp; &#39;Jill&#39; &quot;,);')

    def test_sanitize_with_remove_chars(self):
        self.assertEqual(TransferSanitizer.sanitize('<script>alert(" \'jAck\' & \'Jill\' ");</script>', priority='fe',
                                                    remove_chars=['alert']),
                         '&lt;script&gt;(&quot;, &#39;jAck&#39; &amp; &#39;Jill&#39; &quot;,);&lt;&#47;script&gt;')

    def test_sanitize_with_escape_chars(self):
        self.assertEqual(TransferSanitizer.sanitize('<script>alert(" \'jAck\' & \'Jill\' ");</script>', priority='ef',
                                                    escape_chars={'script': 'p', '\'': '&#39;'}),
                         '<p>alert(" &#39;jAck&#39; & &#39;Jill&#39; ");</p>')

    def test_sanitize_with_escape_remove_chars(self):
        self.assertEqual(TransferSanitizer.sanitize('<script>alert(" \'jAck\' & \'Jill\' ");</script>', priority='ef',
                                                    escape_chars={'script': 'p', '\'': '&#39;'},
                                                    remove_chars=['p', '\'']),
                         '<>alert(" &#39;jAck&#39; & &#39;Jill&#39; ");</>')


if __name__ == "__main__":
    unittest.main()
