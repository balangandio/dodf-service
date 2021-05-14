import re
from functools import reduce
from unidecode import unidecode

from ..Sentence import Sentence


class ValorSentenceParser:
    FIELD_NAMES = ['VALOR', 'PRECO/VALOR', 'VALOR TOTAL']
    RE_FIELD_EXTRACT = re.compile('(?P<field>R\$ ?(?P<value>[\d\.]+(,\d*)?))')
    name = 'valor'

    def test(self, sentence: Sentence):
        if sentence.field != None:
            if self._is_field_common_name(sentence.field):
                return True

        return False

    def parse(self, sentences: list):
        accepted = list(filter(lambda s : self.test(s), sentences))
        sent_values = list(map(lambda s : s.value, accepted))

        values = []

        for sent_value in sent_values:
            for match in self.RE_FIELD_EXTRACT.finditer(sent_value):
                try:
                    number = float(match.group('value').replace('.', '').replace(',', '.'))
                    values.append(number)
                except ValueError:
                    pass
        
        max_value = None if len(values) == 0 else reduce(lambda p, n : n if n > p else p, values)

        return None if max_value is None else {
            'currency': 'R$',
            'value': max_value
        }

    def _is_field_common_name(self, field):
        field = unidecode(field).upper()
        return field in self.FIELD_NAMES