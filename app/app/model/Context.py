import re
import nltk
from functools import reduce
from bs4 import BeautifulSoup
from unidecode import unidecode

from .Sentence import Sentence
from .parser.processo import ProcessoSentenceParser
from .parser.signatario import SignatarioSentenceParser
from .parser.objeto import ObjetoSentenceParser
from .parser.valor import ValorSentenceParser
from .parser.nota_empenho import NotaEmpenhoSentenceParser
from .parser.envolvidos import EnvolvidosSentenceParser
from .parser.assinatura import AssinaturaSentenceParser
from .parser.vigencia import VigenciaSentenceParser
from .parser.adicionais import AdicionaisSentenceParser


class Context:
    def __init__(self, document, language='portuguese'):
        self.document = document
        self.language = language

    def document_text(self):
        content = self.document.texto
        soup = BeautifulSoup(content, 'html.parser')

        strings = []
        for string in soup.stripped_strings:
            strings.append(string)

        return ' '.join(strings)

    def sentences(self):
        content = self.document_text()
        return nltk.sent_tokenize(content, self.language)


class ContratoContext(Context):
    EXTRA_ABBREVIATIONS = ['art', 'doc', 'n', 'nº']
    IGNORED_FIELDS = ['CNPJ']
    RE_NOT_PUNCTUATED_SENTENCE_FIELD = re.compile('(\. |, |; | – | - )(?P<field_sent>(?P<field>[^:;]{1,30}): ?)')
    COMMON_EXTENDED_SENTENCE = [
        { 'separator': ', ', 'fields': ['CONTRATADO', 'CONTRATADA', 'CONTRATANTE', 'PELA CONTRATADA', 'PELO CONTRATADO', 'PELO CONTRATANTE', 'OBJETO', 'ASSINATURA'] }
    ]

    def __init__(self, document):
        super().__init__(document)
        self._sentence_tokenizer_optimed = False

    def sentences(self):
        content = self.document_text()
        tokenizer = self._load_sentence_tokenizer()
        sentences = tokenizer.tokenize(content)

        return self._expand_sentences(sentences)
    
    def to_dict(self):
        field_list = []
        sentences = self.parsed_sentences()

        parsers = [
            ProcessoSentenceParser(),
            SignatarioSentenceParser(),
            ObjetoSentenceParser(),
            ValorSentenceParser(),
            NotaEmpenhoSentenceParser(),
            EnvolvidosSentenceParser(),
            AssinaturaSentenceParser(),
            VigenciaSentenceParser(),
            AdicionaisSentenceParser()
        ]

        fields = map(lambda p : (p.name, p.parse(sentences)), parsers)
        fields = filter(lambda field : field[1] is not None, fields)
        def _acc_dict(acc, field):
            acc.update({ field[0]: field[1] })
            return acc
        fields = reduce(_acc_dict, fields, dict())

        fields.update({ 'dataPublicacao': self.document.dt_previsao_publicacao })

        for sentence in sentences:
            field_list.append({
                'sentence': sentence.sent,
                'field': sentence.field,
                'value': sentence.value
            })

        return {
            'sentences': field_list,
            'fields': fields
        }

    def parsed_sentences(self):
        sents = self.sentences()
        sentence_list = []
        
        for sent in sents:
            sentence = Sentence.parse_sentence(sent)

            if sentence.is_empty() and len(sentence_list) > 0:
                last_one: Sentence = sentence_list[len(sentence_list) - 1]
                last_one.append(sent)
            else:
                sentence_list.append(sentence)
        
        return sentence_list

    def _load_sentence_tokenizer(self):
        language = self.language

        tokenizer = nltk.data.load("tokenizers/punkt/{0}.pickle".format(language))

        if not self._sentence_tokenizer_optimed:
            tokenizer._params.abbrev_types.update(self.EXTRA_ABBREVIATIONS)
            self._sentence_tokenizer_optimed = True

        return tokenizer
    
    def _expand_sentences(self, sentences):
        expanded_list = []

        for sent in sentences:
            matches = list(self.RE_NOT_PUNCTUATED_SENTENCE_FIELD.finditer(sent))

            def _is_match_accepted(match):
                separator = match.group(1)
                field = match.group(3)

                for ef in self.COMMON_EXTENDED_SENTENCE:
                    if separator == ef['separator']:
                        if not unidecode(field).upper() in ef['fields']:
                            return False

                return not match.group('field').upper() in self.IGNORED_FIELDS
            
            matches = list(filter(_is_match_accepted, matches))

            if len(matches) == 0:
                expanded_list.append(sent)
            else:
                sents_in_between = []

                first_match = matches[0]
                sents_in_between.append(sent[:first_match.start()])

                if len(matches) > 1:
                    def _extract_in_between(m1, m2):
                        sents_in_between.append(sent[m1.start('field_sent'):m2.start()])
                        return m2
                    reduce(_extract_in_between, matches)
                
                last_match = matches[len(matches) - 1]
                sents_in_between.append(sent[last_match.start('field_sent'):])

                expanded_list.extend(sents_in_between)

        return expanded_list
