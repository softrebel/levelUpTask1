import sys
from typing import List, Dict, Pattern, Union, Collection
import requests
import markdown


class TransferSanitizer:
    escape_chars: Dict[str, str] = {
        '&': '&amp;',
        '"': '&quot;,',
        '\'': '&#39;',  # for more information, go to TOPICS.md
        '<': '&lt;',
        '>': '&gt;',
        '/': '&#47;'
    }
    remove_chars: List[str] = [
        '<script>',
        '</script>',
    ]

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
            escaped: Dict[str, str] = escape_chars if escape_chars else TransferSanitizer.escape_chars
            import re
            pattern: Pattern[str] = re.compile(r'(' + '|'.join(escaped.keys()) + r')')
            return pattern.sub(lambda x: escaped[
                x.group()] if x.group() in escaped.keys() else x.group(), entity)
        except Exception as err:
            raise Exception('Error on escape: {}'.format(err))

    @staticmethod
    def filter(entity: str = '', remove_chars: List[str] = None) -> str:
        try:
            import re
            removed: List[str] = remove_chars if remove_chars else TransferSanitizer.remove_chars
            pattern: Pattern[str] = re.compile(r'{}'.format('|'.join(removed)))
            return pattern.sub('', entity)
        except Exception as err:
            raise Exception('Error on escape: {}'.format(err))

    @staticmethod
    def validate(entity: str = '', validation_rules: Dict[str, str] = None) -> str:
        try:
            # Todo: Implement validation methode
            return entity
        except Exception as err:
            raise Exception('Error on validate: {}'.format(err))

    @staticmethod
    def sanitize(entity: str = '', escape_chars: Dict[str, str] = None, remove_chars: List[str] = None,
                 validation_rules: Dict[str, str] = None,
                 priority: str = "fev") -> str:
        try:
            priority_operations: str = priority
            sanitized: str = entity
            for action in list(priority_operations)[:2]:
                if action == 'e':
                    sanitized = TransferSanitizer.escape(sanitized, escape_chars=escape_chars)
                elif action == 'f':
                    sanitized = TransferSanitizer.filter(sanitized, remove_chars=remove_chars)
                elif action == 'v':
                    sanitized = TransferSanitizer.validate(sanitized, validation_rules=validation_rules)
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
            escape_chars: Dict[str, str] = {i: TransferSanitizer.escape_chars[i] for i in
                                            TransferSanitizer.escape_chars if i != '&'}
            return self.post_data(self.url, self.sanitize(html, escape_chars=escape_chars, priority='fe'))
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
