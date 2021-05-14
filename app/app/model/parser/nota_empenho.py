import re
from unidecode import unidecode

from ..Sentence import Sentence


class NotaEmpenhoSentenceParser:
    FIELD_NAMES = ['NOTA DE EMPENHO', 'NOTAS DE EMPENHO', 'NUMEROS DA NOTA DE EMPENHO', 'NUMEROS DA NOTAS DE EMPENHO', 'RECURSOS', 'VALOR']
    RE_FIELD_EXTRACT = re.compile('(\d{4,4}NE\d{2,8})')
    name = 'notaEmpenho'

    def test(self, sentence: Sentence):
        if self._is_field_common_name(sentence.field):
            return True
        return False

    def parse(self, sentences: list):
        accepted = list(filter(lambda s : self.test(s), sentences))
        accepted.sort(key=self._field_name_order)

        values = None

        for sent in accepted:
            matches = list(self.RE_FIELD_EXTRACT.finditer(sent.value))
            if len(matches) > 0:
                values = list(map(lambda match : match.group(1), matches))
                break

        return values

    def _is_field_common_name(self, field):
        if field != None:
            field = unidecode(field).upper()
            return field in self.FIELD_NAMES
        return False

    def _field_name_order(self, sentence):
        field_names = self.FIELD_NAMES
        field = sentence.field
        if field == None:
            return len(field_names)
        field = unidecode(field).upper()
        if field not in field_names:
            return len(field_names)
        return field_names.index(field)