import re
from typing import Iterable, Optional

from ..Sentence import Sentence


class EnvolvidosSentenceParser:
    FIELD_CONTRATANTE = 'CONTRATANTE'
    FIELD_CONTRATADA = 'CONTRATADA'
    FIELD_PARTES = 'PARTES'
    FIELD_CONTRATANTES = 'CONTRATANTES'
    FIELD_NOME_CONTRATANTES = 'NOME DOS CONTRATANTES'
    RE_CNPJ = re.compile('(?i)(,? inscrita [N].{0,2} )?([\.,-] )?\(?(CNPJ:? )?(N.{0,2} )?(?P<cnpj>\d{1,3}\.\d{3}\.\d{3}\/\d{4}-\d{1,2})\)?')
    RE_PARTES_SEP_BY_X = re.compile('(?i)(?P<prev>.+) X (?P<after>.+)')
    RE_PARTES_SEP_BY_AND = re.compile('^(o )?(?P<prev>((?![Pp]el[ao] [Cc]ontrata(nte|da)).)+) e (?P<after>((?![Pp]el[ao] [Cc]ontrata(nte|da)).)+)$')
    RE_PARTES_SEP_BY_AND_A = re.compile('^(o )?(?P<prev>((?![Pp]el[ao] [Cc]ontrata(nte|da)).)+) e a ([Ee]mpresa )?(?P<after>((?![Pp]el[ao] [Cc]ontrata(nte|da)).)+)$')
    RE_INLINE = re.compile('(?i) (?P<sent>(?P<field>PARTES|CONTRATANTES): (?P<value>.+))$')
    name = 'envolvidos'

    def parse(self, sentences: Iterable[Sentence]) -> Optional[Iterable[dict]]:
        strategies = [
            self._find_entities_contratante_contratada,
            self._find_entities_separated_by_x,
            self._find_entities_separated_by_and,
            self._find_entities_inline
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
        fields = [self.FIELD_CONTRATANTES, self.FIELD_PARTES, self.FIELD_NOME_CONTRATANTES]

        sentence = None

        for field in fields:
            sentence = self._find_by_field(field, sentences)
            if sentence != None:
                break

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
    
    def _find_entities_inline(self, sentences: Iterable[Sentence]) -> Iterable[dict]:
        sentences = filter(lambda s : s.value != None, sentences)
        matches = map(lambda s : list(self.RE_INLINE.finditer(s.value)), sentences)
        matches = filter(lambda m : len(m) == 1, matches)
        matches = map(lambda m : m[0], matches)

        strategies = [
            self._find_entities_separated_by_x,
            self._find_entities_separated_by_and
        ]
        
        for match in matches:
            sentence = Sentence(match.group('sent'), match.group('field'), match.group('value'))
            
            for st in strategies:
                result = st([sentence])
                if result != None:
                    return result

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
