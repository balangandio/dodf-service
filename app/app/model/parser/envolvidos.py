import re
from typing import Iterable, Optional

from ..Sentence import Sentence


class EnvolvidosSentenceParser:
    FIELD_CONTRATANTE = 'CONTRATANTE'
    FIELD_CONTRATADA = 'CONTRATADA'
    FIELD_PARTES = 'PARTES'
    FIELD_CONTRATANTES = 'CONTRATANTES'
    RE_CNPJ = re.compile('(?i)([\.,-] )?\(?(CNPJ:? )?(N.{0,2} )?(?P<cnpj>\d{1,3}\.\d{3}\.\d{3}\/\d{4}-\d{1,2})\)?')
    RE_PARTES_SEP_BY_X = re.compile('(?i)(?P<prev>.+) X (?P<after>.+)')
    RE_PARTES_SEP_BY_AND = re.compile('(?P<prev>.+) e (?P<after>.+)')
    RE_PARTES_SEP_BY_AND_A = re.compile('(?P<prev>.+) e a (?P<after>.+)')
    name = 'envolvidos'

    def parse(self, sentences: Iterable[Sentence]) -> Optional[Iterable[dict]]:
        strategies = [
            self._find_entities_contratante_contratada,
            self._find_entities_separated_by_x,
            self._find_entities_separated_by_and
        ]

        for st in strategies:
            result = st(sentences)
            if result != None:
                return result

        return None

    def _find_entities_contratante_contratada(self, sentences: Iterable[Sentence]) -> Iterable[dict]:
        contratante = self._find_by_field(self.FIELD_CONTRATANTE, sentences)
        contratada = self._find_by_field(self.FIELD_CONTRATADA, sentences)

        if contratante == None or contratada == None:
            return None
        
        return [
            self._parse_entities(contratante.value, 'contratante'),
            self._parse_entities(contratada.value, 'contratada')
        ]
    
    def _find_entities_separated_by_x(self, sentences: Iterable[Sentence]) -> Iterable[dict]:
        partes = self._find_by_field(self.FIELD_PARTES, sentences)

        if partes is None:
            return None

        matches = list(self.RE_PARTES_SEP_BY_X.finditer(partes.value))

        if len(matches) == 1:
            return [
                self._parse_entities(matches[0].group('prev')),
                self._parse_entities(matches[0].group('after'))
            ]
        
        return None

    def _find_entities_separated_by_and(self, sentences: Iterable[Sentence]) -> Iterable[dict]:
        sentence = self._find_by_field(self.FIELD_CONTRATANTES, sentences)

        if sentence is None:
            sentence = self._find_by_field(self.FIELD_PARTES, sentences)

        if sentence is None:
            return None

        for pattern in [ self.RE_PARTES_SEP_BY_AND_A, self.RE_PARTES_SEP_BY_AND ]:
            matches = list(pattern.finditer(sentence.value))

            if len(matches) == 1:
                return [
                    self._parse_entities(matches[0].group('prev')),
                    self._parse_entities(matches[0].group('after'))
                ]

        return None

    def _parse_entities(self, sent: str, role: Optional[str] = None) -> dict:
        matches = list(self.RE_CNPJ.finditer(sent))

        if len(matches) == 1:
            return {
                'role': role,
                'entity': sent[:matches[0].start()] + sent[matches[0].end():],
                'cnpj': matches[0].group('cnpj')
            }
        else:
            return {
                'role': role,
                'entity': sent
            }

    def _find_by_field(self, field: str, sentences: Iterable[Sentence]) -> Optional[Sentence]:
        accepted = list(filter(lambda sent : sent.field != None and sent.field.upper() == field, sentences))
        return accepted[0] if len(accepted) > 0 else None
