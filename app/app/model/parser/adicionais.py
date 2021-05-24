from functools import reduce
from typing import Iterable, Optional, Tuple

from .fonteRecurso import FonteRecursoSentenceParser
from .naturezaDepesa import NaturezaDespesaSentenceParser
from .ug import UGSentenceParser
from .programaTrabalho import ProgramaTrabalhoSentenceParser
from ..Sentence import Sentence


class AdicionaisSentenceParser:
    PARSERS = [
        FonteRecursoSentenceParser(),
        NaturezaDespesaSentenceParser(),
        UGSentenceParser(),
        ProgramaTrabalhoSentenceParser()
    ]
    name = 'adicionais'

    def parse(self, sentences: Iterable[Sentence]) -> Optional[dict]:
        fields = map(lambda p : (p.name, p.parse(sentences)), self.PARSERS)
        fields = list(filter(lambda field : field[1] is not None, fields))

        def _acc_dict(acc: dict, field: Tuple):
            acc.update({ field[0]: field[1] })
            return acc

        return None if len(fields) == 0 else reduce(_acc_dict, fields, dict())