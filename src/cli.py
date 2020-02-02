import sys
from typing import List, Dict, Pattern, KeysView, Iterator
import requests
import markdown


class TransferSanitizer:
    special_chars: Dict[str, str] = {
        '&': '&amp;',
        '"': '&quot;,',
        '\'': '&#39;',  # for more information, go to TOPICS.md
        '<': '&lt;',
        '>': '&gt;',
        '/': '&#47;'
    }

    def __init__(self, url: str, entity: str = ''):
        self.url: str = url
        self.entity: str = entity

    @staticmethod
    def markdown_to_html(entity: str = '') -> str:
        try:
            return markdown.markdown(entity, output_format='html5')
        except Exception as err:
            raise Exception('Error on markdown: {}'.format(err))

    @staticmethod
    def escape(entity: str = '', escape_chars: Dict[str, str] = None) -> str:
        try:
            escape_chars = escape_chars if escape_chars else TransferSanitizer.special_chars
            import re
            pattern: Pattern[str] = re.compile(r'(' + '|'.join(escape_chars.keys()) + r')')
            return pattern.sub(lambda x: escape_chars[
                x.group()] if x.group() in escape_chars else x.group(), entity)
        except Exception as err:
            raise Exception('Error on escape: {}'.format(err))

    @staticmethod
    def filter(escaped: str = '') -> str:
        try:
            # Todo: Implement filter methode
            return escaped
        except Exception as err:
            raise Exception('Error on escape: {}'.format(err))

    @staticmethod
    def validate(filtered: str = '') -> str:
        try:
            # Todo: Implement validation methode
            return filtered
        except Exception as err:
            raise Exception('Error on validate: {}'.format(err))

    @staticmethod
    def sanitize(entity: str = '', escape_chars: Dict[str, str] = None) -> str:
        try:
            escaped = TransferSanitizer.escape(entity, escape_chars=escape_chars)
            filtered = TransferSanitizer.filter(escaped)
            sanitized = TransferSanitizer.validate(filtered)
            return sanitized
        except Exception as err:
            raise Exception('Error on sanitization: {}'.format(err))

    @staticmethod
    def post_data(url: str, sanitized_entity: str) -> Dict[str, str]:
        try:
            if not url or not sanitized_entity:
                raise ValueError('url and sanitized_entity must be not null')
            res = requests.post(url, {'entity': sanitized_entity})
            status = 'success'
            if res.status_code != 201:
                status = 'failed'
            return {
                'status': status,
                'sanitized': sanitized_entity
            }
        except Exception as err:
            raise Exception('Error on post data: {}'.format(err))

    def send_to_api(self) -> Dict[str, str]:
        try:
            html: str = self.markdown_to_html(self.entity)
            # !important Only & is escaped in markdown library
            escape_chars: Dict[str, str] = {i: TransferSanitizer.special_chars[i] for i in
                                            TransferSanitizer.special_chars if i != '&'}
            return self.post_data(self.url, self.sanitize(html, escape_chars=escape_chars))
        except Exception as err:
            raise Exception('Error on send to APi: {}'.format(err))


if __name__ == '__main__':
    url = 'https://my-json-server.typicode.com/softrebel/levelUpTask1/entity'
    transfer = TransferSanitizer(url)
    try:
        if len(sys.argv) > 1:
            transfer.entity = sys.argv[1]
        else:
            transfer.entity = input('Please Enter Your HTML/Markdown Body:\n')

        print(transfer.send_to_api())

    except ValueError as err:
        raise ValueError('argument mode must be integer')

    except Exception as err:
        raise Exception('Error on transferring body: {}'.format(err))
