import re

from ..Sentence import Sentence


class ProcessoSentenceParser:
    RE_NUM_PROCESSO = re.compile('((\d+[-\.])+\d+\/\d+([-\.]\d+)?)')
    RE_NUM_PROCESSO_INLINE = re.compile('(?i)Processo ((\d+[-\.])+\d+\/\d+([-\.]\d+)?)')
    name = 'numeroProcesso'

    def test(self, sentence: Sentence):
        if self._is_sentence_field_processo(sentence):
            return True

        if self._has_inline_num_processo(sentence):
            return True
        
        return False

    def parse(self, sentences: list):
        accepted = list(filter(lambda s : self.test(s), sentences))

        for sent in filter(lambda s : self._is_sentence_field_processo(s), accepted):
            match = self.RE_NUM_PROCESSO.search(sent.value)
            if match != None:
                num_processo = match.group(1)
                return num_processo

        for sent in filter(lambda s : self._has_inline_num_processo(s), accepted):
            match = self.RE_NUM_PROCESSO_INLINE.search(sent.value)
            if match != None:
                num_processo = match.group(1)
                return num_processo

        return None
    
    def _is_sentence_field_processo(self, sentence):
        if sentence.field is None or sentence.value is None:
            return False
        return sentence.field.upper() == 'PROCESSO'

    def _has_inline_num_processo(self, sentence):
        return sentence.value != None and self.RE_NUM_PROCESSO_INLINE.search(sentence.value) != None