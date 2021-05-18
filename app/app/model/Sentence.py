import re


class Sentence:
    RE_EXTRACT_FIELD_VALUE = re.compile('^([^:]+): ?(.+)$')

    def __init__(self, sent: str, field: str, value: str):
        self.sent = sent
        self.field = field
        self.value = value
    
    def is_empty(self):
        return self.field is None and self.value is None

    def append(self, part: str):
        self.sent += ' ' + part
        if self.value != None:
            self.value += ' ' + part
    
    @staticmethod
    def parse_sentence(sentence: str):
        ( field, value ) = Sentence._extract_field_value_by_re(sentence)
        return Sentence(sentence, field, value)

    @staticmethod
    def _extract_field_value_by_re(sentence: str):
        search = Sentence.RE_EXTRACT_FIELD_VALUE.search(sentence)
        field = None
        value = None

        if search is not None:
            if len(search.group(1).split()) <= 5:
                field = search.group(1)
                value = search.group(2)

        return (field, value)