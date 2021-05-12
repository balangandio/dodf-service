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
    name = 'signatarios'

    def test(self, sentence: Sentence):
        if sentence.field != None:
            field = unidecode(sentence.field)

            if field in self.FIELD_NAMES:
                return True
            
            match = self.RE_FIELD_NAME.search(sentence.field + ':')

            if match != None and match.start() == 0:
                return True

        return False

    def parse(self, sentences: list):
        accepted = list(filter(lambda s : self.test(s), sentences))

        sents = []

        for sentence in accepted:
            field = unidecode(sentence.field)
            if field in self.FIELD_NAMES:
                sents.append(sentence.value)
            elif self.RE_FIELD_NAME.search(sentence.field + ':') != None:
                sents.append(sentence.sent)

        entities = []

        for sent in sents:
            search = self.RE_FIELD_NAME.search(sent)
            if search != None:
                entities.append({
                    'entity': search.group('entity'),
                    'agent': sent[search.end():]
                })
        
        if len(entities) > 0:
            return entities

        return None