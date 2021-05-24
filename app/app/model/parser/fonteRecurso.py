import re
from typing import Iterable, Optional

from ..Sentence import Sentence


class FonteRecursoSentenceParser:
    RE_FIELD_NAME = re.compile('(?i)FONTES? DE RECURSOS?')
    RE_VALUES_EXTRACT = re.compile('^(?i) ?(?P<values>\d+(( e |\/)\d+)?)')
    RE_SENTENCE_EXTRACT = re.compile('(?i)fontes?( de recursos?)?:? (CT )?(?P<values>\d+(( e |\/)\d+)?)')
    RE_NUMERIC = re.compile('\d+')
    name = 'fonteRecurso'

    def test(self, sentence: Sentence) -> bool:
        if sentence.field != None:
            return self.RE_FIELD_NAME.search(sentence.field) != None
        return False

    def parse(self, sentences: Iterable[Sentence]) -> Optional[dict]:
        values = []

        for strategy in [self._find_by_field, self._find_in_sentence]:
            values += strategy(sentences)

        return None if len(values) == 0 else list(set(values))

    def _find_by_field(self, sentences: Iterable[Sentence]) -> list:
        values = []

        for sentence in filter(lambda s : self.test(s), sentences):
            match = self.RE_VALUES_EXTRACT.search(sentence.value)
            if match != None:
                values += self._parse_value(match.group('values'))

        return values
    
    def _find_in_sentence(self, sentences: Iterable[Sentence]) -> list:
        values = []

        for sentence in filter(lambda s : s.value != None, sentences):
            for match in self.RE_SENTENCE_EXTRACT.finditer(sentence.value):
                values += self._parse_value(match.group('values'))
  
        return values

    def _parse_value(self, value: str) -> list:
        return self.RE_NUMERIC.findall(value)