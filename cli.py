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

    def __init__(self, url: str, entity: str = ''):
        self.url = url
        self.entity: str = entity

    @staticmethod
    def markdown_to_html(entity: str = '') -> str:
        return markdown.markdown(entity)

    @staticmethod
    def escape(entity: str = '') -> str:
        import re
        pattern = re.compile(r'(' + '|'.join(
            [*TransferSanitizer.special_chars.values(), *TransferSanitizer.special_chars.keys()]) + r')')
        return pattern.sub(lambda x: TransferSanitizer.special_chars[
            x.group()] if x.group() in TransferSanitizer.special_chars else x.group(), entity)

    @staticmethod
    def filter(escaped: str = '') -> str:
        return escaped

    @staticmethod
    def validate(filtered: str = '') -> str:
        return filtered

    @staticmethod
    def sanitize(entity: str = '') -> str:
        escaped = TransferSanitizer.escape(entity)
        filtered = TransferSanitizer.filter(escaped)
        sanitized = TransferSanitizer.validate(filtered)
        return sanitized

    @staticmethod
    def post_data(url: str, sanitized_entity: str) -> Dict[str, str]:
        if not url or not sanitized_entity:
            raise ValueError('url and sanitized_entity must be not null')
        return {
            'status': 'ok',
            'sanitized': sanitized_entity
        }

    def send(self) -> Dict[str, str]:
        return self.post_data(self.url, self.sanitize(self.markdown_to_html(self.entity)))


if __name__ == '__main__':
    url = 'https://my-json-server.typicode.com/softrebel/levelUpTask1/entity'
    transfer = TransferSanitizer(url)
    try:
        if len(sys.argv) > 1:
            transfer.entity = sys.argv[1]
        else:
            transfer.entity = input('Please Enter Your HTML/Markdown Body:\n')

        print(transfer.send())

    except ValueError as err:
        raise ValueError('argument mode must be integer')

    except Exception as err:
        raise Exception('Error on transferring body: {}'.format(err))
