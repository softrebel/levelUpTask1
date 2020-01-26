import requests
from typing import List, Dict
import sys
import markdown


class TransferSanitizer:
    special_chars: Dict[str, str] = {
        '&': '&amp;',
        '"': '&quot;,',
        '\'': '&#x27;',
        '<': '&lt;',
        '>': '&gt;',
        '/': '&#x2F;'
    }

    def __init__(self, entity: str = ''):
        self.entity: str = entity

    @staticmethod
    def sanitize(entity: str = '') -> str:
        import re
        pattern = re.compile(r'\b(' + '|'.join(
            [*TransferSanitizer.special_chars.values(), *TransferSanitizer.special_chars.keys()]) + r')\b')
        return pattern.sub(lambda x: TransferSanitizer.special_chars[
            x.group()] if x.group() in TransferSanitizer.special_chars else x.group(), entity)

    @staticmethod
    def post_data(url: str, sanitized_entity: str) -> Dict[str, str]:
        if not url or not sanitized_entity:
            raise ValueError('url and sanitized_entity must be not null')
        return {
            'status': 'ok'
        }

    def send(self) -> Dict[str, str]:
        return TransferSanitizer.post_data(TransferSanitizer.sanitize(self.entity))


if __name__ == '__main__':

    html = markdown.markdown('<b>sal&am"dwd"\'')

    print(TransferSanitizer.sanitize(html))
    quit()

    transfer = TransferSanitizer()
    try:
        if len(sys.argv) > 1:
            transfer.entity = sys.argv[1]
        else:
            transfer.entity = input('Please Enter Your HTML/Markdown Body:\n')
    except Exception as err:
        raise Exception('Error on transferring body: ' + err)
