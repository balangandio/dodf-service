from unidecode import unidecode

from ..Sentence import Sentence


class ObjetoSentenceParser:
    FIELD_NAMES = ['OBJETO', 'DO OBJETO', 'RESUMO DO OBJETO']
    name = 'objeto'

    def test(self, sentence: Sentence):
        if sentence.field != None:
            if self._is_field_common_name(sentence.field):
                return True

        return False

    def parse(self, sentences: list):
        accepted = list(filter(lambda s : self.test(s), sentences))
        values = list(map(lambda s : s.value, accepted))

        return None if len(values) == 0 else ' '.join(values)

    def _is_field_common_name(self, field):
        field = unidecode(field).upper()
        return field in self.FIELD_NAMES