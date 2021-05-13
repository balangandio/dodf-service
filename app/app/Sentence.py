from functools import reduce
import re
from nltk.text import Text
from unidecode import unidecode


class Sentence:
    RE_EXTRACT_FIELD_VALUE = re.compile('^([^:]+):(.+)$')

    def __init__(self, sent: str, field: str, value: str):
        self.sent = sent
        self.field = field
        self.value = value
    
    def is_empty(self):
        return self.field is None and self.value is None

    def append(self, part: str):
        self.sent += part
        if self.value != None:
            self.value += part
    
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


class ProcessoSentenceParser:
    RE_NUM_PROCESSO = re.compile('((\d+[-\.])+\d+\/\d+([-\.]\d+)?)')
    name = 'processo'

    def test(self, sentence: Sentence):
        return sentence.field != None and sentence.field.upper() == 'PROCESSO'

    def parse(self, sentences: list):
        accepted = list(filter(lambda s : self.test(s), sentences))

        if len(accepted) > 0:
            sentence_value = accepted[0].value
            if sentence_value != None:
                match = self.RE_NUM_PROCESSO.search(sentence_value)

                if match != None:
                    num_processo = match.group(1)
                    return {
                        'numero': num_processo
                    }

        return None


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