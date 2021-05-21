import re
from functools import reduce
from typing import Iterable, Optional
from unidecode import unidecode

from ..Sentence import Sentence


class ValorSentenceParser:
    FIELD_NAMES = ['VALOR', 'PRECO/VALOR', 'VALOR TOTAL']
    RE_INLINE_FIELD = re.compile('^((RESUMO )?(D[AO]S? .+)|OBJETO)')
    RE_FIELD_EXTRACT = re.compile('(?P<field>R\$ ?(?P<value>[\d\.]+(,\d*)?))')
    RE_INLINE_EXTRACT = [
        re.compile('(?i) valor (total |global )(do contrato )?é de (?P<field>R\$ ?(?P<value>[\d\.]+(,\d*)?))'),
        re.compile('(?i) atualizando o valor (total |global )?(do contrato )?para (?P<field>R\$ ?(?P<value>[\d\.]+(,\d*)?))'),
        re.compile('(?i) passando (o contrato )?a ter o valor (total |global )?de (?P<field>R\$ ?(?P<value>[\d\.]+(,\d*)?))'),
        re.compile('(?i) valor .{1,200} (passa|passará) a ser (de )?(?P<field>R\$ ?(?P<value>[\d\.]+(,\d*)?))'),
        re.compile('(?i) valor (total |global |anual )?(do contrato )?(passa|passará) de .{1,200} para (?P<field>R\$ ?(?P<value>[\d\.]+(,\d*)?))')
    ]
    name = 'valor'

    def test(self, sentence: Sentence) -> bool:
        if sentence.field != None:
            if self._is_field_common_name(sentence.field):
                return True

        return False

    def parse(self, sentences: Iterable[Sentence]) -> Optional[float]:
        strategies = [self._find_common_field_value, self._find_inline_value]
        values = []

        for st in strategies:
            number = st(sentences)
            if number != None:
                values.append(number)

        max_value = None if len(values) == 0 else reduce(lambda p, n : n if n > p else p, values)

        return None if max_value is None else {
            'currency': 'R$',
            'value': max_value
        }
    
    def _find_common_field_value(self, sentences: Iterable[Sentence]) -> Optional[float]:
        accepted = filter(lambda s : self.test(s), sentences)
        sent_values = map(lambda s : s.value, accepted)

        values = []

        for sent_value in sent_values:
            for match in self.RE_FIELD_EXTRACT.finditer(sent_value):
                number = self._parse_value(match.group('value'))
                if number != None:
                    values.append(number)
        
        return None if len(values) == 0 else reduce(lambda p, n : n if n > p else p, values)
    
    def _find_inline_value(self, sentences: Iterable[Sentence]) -> Optional[float]:
        values = []

        for sentence in sentences:
            if self._is_field_of_inline_sentence(sentence.field):
                for pattern in self.RE_INLINE_EXTRACT:
                    for match in pattern.finditer(sentence.value):
                        number = self._parse_value(match.group('value'))
                        if number != None:
                            values.append(number)

        return None if len(values) == 0 else reduce(lambda p, n : n if n > p else p, values)

    def _is_field_common_name(self, field: str) -> bool:
        field = unidecode(field).upper()
        return field in self.FIELD_NAMES or field.startswith('VALOR')
    
    def _is_field_of_inline_sentence(self, field: str) -> bool:
        if field is None:
            return False
        field = unidecode(field).upper()
        return self.RE_INLINE_FIELD.search(field) != None
    
    def _parse_value(self, value_str: str) -> Optional[float]:
        try:
            return float(value_str.replace('.', '').replace(',', '.'))
        except ValueError:
            return None