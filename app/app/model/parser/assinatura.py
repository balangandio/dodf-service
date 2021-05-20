import re
from unidecode import unidecode
from typing import Iterable, Optional
from datetime import datetime

from ..Sentence import Sentence
from ...util.date import Month


class AssinaturaSentenceParser:
    FIELD_NAMES = ['ASSINATURA', 'DATA DA ASSINATURA', 'DATA DE ASSINATURA']
    RE_INLINE = re.compile('(?i)[\.,;-–] assinam em (?P<date>(\d\d\/\d\d\/\d\d\d\d|\d{1,2} de [^ ]{4,9} de \d\d\d\d))')
    RE_SHORT_DATE = re.compile('(?P<date>\d\d\/\d\d\/\d\d\d\d)')
    RE_LONG_DATE = re.compile('(?P<day>\d{1,2}) de (?P<month>[^ ]{4,9}) de (?P<year>\d\d\d\d)')
    name = 'assinatura'

    def test(self, sentence: Sentence):
        if sentence.field != None and sentence.value != None:
            if self._is_field_common_name(sentence.field):
                return True

        return False

    def parse(self, sentences: list):
        strategies = [self._find_with_common_field, self._find_inline_assinatura]

        for st in strategies:
            result = st(sentences)
            if result != None:
                return result

        return None
    
    def _find_with_common_field(self, sentences: Iterable[Sentence]) -> Optional[str]:
        accepted = filter(lambda s : self.test(s), sentences)
        sents = map(lambda s : s.value, accepted)

        for sent in sents:
            result = self._try_parse_date(sent)
            if result != None:
                return result

        return None
    
    def _find_inline_assinatura(self, sentences: Iterable[Sentence]) -> Optional[str]:
        for sent in sentences:
            if sent.value != None:
                match = self.RE_INLINE.search(sent.value)

                if match != None:
                    result = self._try_parse_date(match.group('date'))
                    if result != None:
                        return result
        
        return None

    def _try_parse_date(self, date_str: str) -> Optional[str]:
        strategies = [self._try_parse_short_date, self._try_parse_long_date]

        for st in strategies:
            result = st(date_str)
            if result != None:
                return result

        return None

    def _try_parse_short_date(self, date_str: str) -> Optional[str]:
        match = self.RE_SHORT_DATE.search(date_str.replace(' ', ''))

        if match != None:
            try:
                date = datetime.strptime(match.group('date'), '%d/%m/%Y')
                return date.strftime('%Y-%m-%d')
            except:
                pass
        return None
    
    def _try_parse_long_date(self, date_str: str) -> Optional[str]:
        match = self.RE_LONG_DATE.search(date_str)

        if match != None:
            day = match.group('day')
            month = Month.parse_str(match.group('month'))
            year = match.group('year')

            if month != None:
                month = month.month_of_the_year()
                try:
                    date = datetime.strptime('{}/{}/{}'.format(day, month, year), '%d/%m/%Y')
                    return date.strftime('%Y-%m-%d')
                except:
                    pass
        return None

    def _is_field_common_name(self, field: str) -> bool:
        field = unidecode(field).upper()
        return field in self.FIELD_NAMES
    