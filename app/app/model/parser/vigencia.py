import re
from typing import Iterable, Optional
from unidecode import unidecode

from ..Sentence import Sentence
from .objeto import ObjetoSentenceParser
from ...util.date import Parser, max_date


class VigenciaSentenceParser:
    RE_FIELD_NAME = re.compile('(?i)(VIGENCIA|PRAZO|PRORROGACAO)')
    RE_DURATION = re.compile('(?i)((?P<prev>[^ ]+) )?(?P<value>\d+) (\([^\(\)]+\) )?(?P<unit>(dias?|semanas?|m[eê]s(es)?|semestres?|anos?))')
    RE_DATE_INTERVAL = re.compile('(?i)(?P<start>(\d\d\/\d\d\/\d\d\d\d|\d{1,2}( de)? [^ ]{4,9}( de)? \d\d\d\d)) ([aà]|at[eé]) (?P<end>(\d\d\/\d\d\/\d\d\d\d|\d{1,2}( de)? [^ ]{4,9}( de)? \d\d\d\d))')
    RE_DATE_END = re.compile('(?i)(para|at[eé]|em) (?P<date>(\d\d\/\d\d\/\d\d\d\d|\d{1,2}( de)? [^ ]{4,9}( de)? \d\d\d\d))')
    RE_DATE_START = re.compile('(?i)a (partir|contar|vigorar) (de |do dia )?(?P<date>(\d\d\/\d\d\/\d\d\d\d|\d{1,2}( de)? [^ ]{4,9}( de)? \d\d\d\d))')
    RE_FIELD_OBJETO = re.compile('(?i)(prazo|vig[eê]ncia)')
    name = 'vigencia'

    def test(self, sentence: Sentence):
        if sentence.field != None and sentence.value != None:
            if self._is_field_common_name(sentence.field):
                return True

        return False

    def parse(self, sentences: Iterable[Sentence]) -> Optional[dict]:
        strategies = [
            lambda s : self.test(s),
            lambda s : self._is_field_common_name_objeto(s)
        ]

        for st in strategies:
            for sent in map(lambda s : s.value, filter(st, sentences)):
                result = self._try_parse_sent(sent)
                if result != None:
                    return result

        return None

    def _try_parse_sent(self, sent: str) -> Optional[dict]:
        sent = sent.replace('assinam em', 'assinam').replace('Assinam em', 'Assinam')
        interval = self._find_date_interval(sent)
        duration = self._find_duration(sent)

        return None if interval is None and duration is None else {
            'interval': interval,
            'duration': duration
        }

    def _find_date_interval(self, sent: str) -> Optional[dict]:
        match = self.RE_DATE_INTERVAL.search(sent)
        start = None
        end = None

        if match != None:
            start = Parser.parse_date(match.group('start'))
            end = Parser.parse_date(match.group('end'))

        if start is None:
            start = self._find_date_start(sent)
        if end is None:
            end = self._find_date_end(sent)

        if start != None and end != None and end <= start:
            end = None

        return None if start is None and end is None else {
            'start': None if start is None else start.strftime('%Y-%m-%d'),
            'end': None if end is None else end.strftime('%Y-%m-%d')
        }
    
    def _find_date_end(self, sent: str):
        dates = []
        for match in self.RE_DATE_END.finditer(sent):
            date = Parser.parse_date(match.group('date'))
            if date != None:
                dates.append(date)

        return max_date(dates)

    def _find_date_start(self, sent: str):
        dates = []
        for match in self.RE_DATE_START.finditer(sent):
            date = Parser.parse_date(match.group('date'))
            if date != None:
                dates.append(date)
    
        return max_date(dates)

    def _find_duration(self, sent: str) -> Optional[dict]:
        NOT_ALLOWED_PREV_TERM = ['EXPIRANDO']
        match = self.RE_DURATION.search(sent)

        if match != None:
            prev = match.group('prev')
            if prev != None and prev.upper() in NOT_ALLOWED_PREV_TERM:
                match = None

        return None if match is None else {
            'value': match.group('value'),
            'unit': match.group('unit')
        }

    def _is_field_common_name(self, field: str) -> bool:
        if field is None:
            return False
        field = unidecode(field).upper()
        return self.RE_FIELD_NAME.search(field) != None
    
    def _is_field_common_name_objeto(self, sentence: Sentence) -> bool:
        field = sentence.field
        value = sentence.value

        if field is None or value is None:
            return False

        if not unidecode(field).upper() in ObjetoSentenceParser.FIELD_NAMES:
            return False
        
        return self.RE_FIELD_OBJETO.search(value) != None
