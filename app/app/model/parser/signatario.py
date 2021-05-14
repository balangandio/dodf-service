import re
from functools import reduce
from unidecode import unidecode

from ..Sentence import Sentence


class SignatarioSentenceParser:
    FIELD_NAMES = ['ASSINANTES', 'SIGNATARIOS', 'NOME DOS SIGNATARIOS', 'REPRESENTANTES']
    RE_FIELD_NAME = re.compile('(?i)(PEL[AO]) (?P<entity>[^:]+): ?')
    RE_FIELD_EXTRACT = re.compile('(?i)(,? E )?(PEL[AO]) (?P<entity>(((?!PEL[AO])[^:])+:|[^,: ]+)),? ')
    name = 'signatarios'

    def test(self, sentence: Sentence):
        if sentence.field != None:
            if self._is_field_common_name(sentence.field):
                return True

            if self._is_field_accept_by_re(sentence.field):
                return True

        return False

    def parse(self, sentences: list):
        accepted = list(filter(lambda s : self.test(s), sentences))

        sents = []

        for sentence in accepted:
            if self._is_field_common_name(sentence.field):
                sents.append(sentence.value)
            elif self._is_field_accept_by_re(sentence.field):
                sents.append(sentence.sent)

        entities = []

        for sent in sents:
            matches = list(self.RE_FIELD_EXTRACT.finditer(sent))

            if len(matches) == 1:
                entities.append({
                    'entity': matches[0].group('entity'),
                    'agent': sent[matches[0].end():]
                })
            elif len(matches) > 1:
                def _extract_in_between(m1, m2):
                    entities.append({
                        'entity': m1.group('entity'),
                        'agent': sent[m1.end():m2.start()]
                    })
                    return m2
                reduce(_extract_in_between, matches)

                last_match = matches[len(matches) - 1]

                entities.append({
                    'entity': last_match.group('entity'),
                    'agent': sent[last_match.end():]
                })

        if len(entities) > 0:
            return entities

        return None

    def _is_field_common_name(self, field):
        field = unidecode(field).upper()
        return field in self.FIELD_NAMES
    
    def _is_field_accept_by_re(self, field):
        return self.RE_FIELD_NAME.search(field + ':') != None