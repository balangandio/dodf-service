import re
from unidecode import unidecode

from ..Sentence import Sentence


class ProcessoSentenceParser:
    RE_NUM_PROCESSO = re.compile('(?P<num>((\d+[-\.])+\d+|\d+)\/\d+([-\.]\d+)?)')
    RE_NUM_PROCESSO_INLINE = re.compile('(?i)Processo( N.?)? (?P<num>((\d+[-\.])+\d+|\d+)\/\d+([-\.]\d+)?)')
    FIELD_NAMES = ['PROCESSO', 'PROCESSO NO']
    name = 'numeroProcesso'

    def test(self, sentence: Sentence):
        if self._is_sentence_field_processo(sentence):
            return True

        if self._has_inline_num_processo(sentence):
            return True
        
        return False

    def parse(self, sentences: list):
        for sent in filter(lambda s : self._is_sentence_field_processo(s), sentences):
            match = self.RE_NUM_PROCESSO.search(sent.value)
            if match != None:
                return match.group('num')

        for sent in filter(lambda s : self._has_inline_num_processo(s), sentences):
            match = self.RE_NUM_PROCESSO_INLINE.search(sent.value)
            if match != None:
                return match.group('num')

        return None
    
    def _is_sentence_field_processo(self, sentence):
        if sentence.field is None or sentence.value is None:
            return False
        field = unidecode(sentence.field).upper()
        return field in self.FIELD_NAMES

    def _has_inline_num_processo(self, sentence):
        return sentence.value != None and self.RE_NUM_PROCESSO_INLINE.search(sentence.value) != None