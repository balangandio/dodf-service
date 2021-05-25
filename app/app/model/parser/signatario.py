import re
from functools import reduce
from unidecode import unidecode

from ..Sentence import Sentence


class SignatarioSentenceParser:
    FIELD_NAMES = ['ASSINATURAS', 'ASSINANTES', 'SIGNATARIOS', 'NOME DOS SIGNATARIOS', 'REPRESENTANTES', 'PARTES']
    RE_FIELD_NAME = re.compile('(?i)(PEL[AO] |P\/)(?P<entity>[^:]+): ?')
    RE_FIELD_EXTRACT = re.compile('(?i)(,? E,? )?(PEL[AO] |P/)(?P<entity>(DISTRITO FEDERAL|COMODANTE|CONTRATAD[AO]|((?!PEL[AO])[^,:])+:|[^,: ]+)),? ')
    name = 'signatarios'

    def test(self, sentence: Sentence):
        if sentence.field != None:
            if self._is_field_common_name(sentence.field):
                return True

            if self._is_field_accept_by_re(sentence.field):
                return True

            if self._try_inline_extract(sentence.value) != None:
                return True

        return False

    def parse(self, sentences: list):
        sents = []

        for sentence in sentences:
            if sentence.field != None:
                if self._is_field_common_name(sentence.field):
                    sents.append(sentence.value)
                elif self._is_field_accept_by_re(sentence.field):
                    sents.append(sentence.sent)
                else:
                    inline_extract = self._try_inline_extract(sentence.value)
                    if inline_extract != None:
                        sents.append(inline_extract)

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

        for ent in entities:
            if ent['entity'].endswith(':'):
                ent['entity'] = ent['entity'][:len(ent['entity']) - 1]

        return None if len(entities) == 0  else entities

    def _is_field_common_name(self, field):
        field = unidecode(field).upper()
        return field in self.FIELD_NAMES
    
    def _is_field_accept_by_re(self, field):
        return self.RE_FIELD_NAME.search(field + ':') != None

    def _try_inline_extract(self, sent: str):
        search = re.search('(?i)(\.|,|;| –| -) ?(?P<sent>(?P<field>[^:; ]{1,20}) )PEL[AO] ', sent)

        if search != None:
            if unidecode(search.group('field')).upper() in self.FIELD_NAMES:
                return sent[search.end('field'):]

        return None