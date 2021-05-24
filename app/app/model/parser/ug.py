import re
from typing import Iterable, Optional

from ..Sentence import Sentence


class UGSentenceParser:
    FIELD_NAMES = ['UG', 'UG/UO', 'UO']
    RE_VALUE_EXTRACT = re.compile('^ ?(?P<value>(\d+[\d\.-]+)?\d+)')
    name = 'ug'

    def test(self, sentence: Sentence) -> bool:
        return sentence.field != None and sentence.field.upper() in self.FIELD_NAMES
    
    def parse(self, sentences: Iterable[Sentence]) -> Optional[str]:
        for sent in sentences:
            if self.test(sent):
                match = self.RE_VALUE_EXTRACT.search(sent.value)
                if match != None:
                    return match.group('value')
        return None