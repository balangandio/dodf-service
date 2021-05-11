import re
import nltk
from functools import reduce
from bs4 import BeautifulSoup
from nltk import TokenSearcher
from nltk.text import Text


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
    RE_NOT_PUNCTUATED_SENTENCE_FIELD = re.compile('(; | – | - )(?P<field_sent>(?P<field>[^:]{1,30}): )')
    RE_EXTRACT_FIELD_VALUE = re.compile('^([^:]+):(.+)$')

    def __init__(self, document):
        super().__init__(document)
        self._sentence_tokenizer_optimed = False

    def sentences(self):
        content = self.document_text()
        tokenizer = self._load_sentence_tokenizer()
        sentences = tokenizer.tokenize(content)
        
        return self._expand_sentences(sentences)
    
    def to_dict(self):
        sents_fields = self.sentences_fields()

        return {
            'sentences': sents_fields
        }

    def sentences_fields(self):
        sents = self.sentences()
        sents_fields = []
        
        for sent in sents:
            (field, value) = self._extract_field_value_by_re(sent)

            if field is None and value is None and len(sents_fields) > 0:
                last_sent = sents_fields[len(sents_fields) - 1]
                last_sent['sentence'] += ' ' + sent

                if last_sent['value'] is not None:
                    last_sent['value'] += ' ' + sent
            else:
                sents_fields.append({
                    'sentence': sent,
                    'field': field,
                    'value': value
                })
        
        return sents_fields

    def _extract_field_value_by_re(self, sentence):
        search = self.RE_EXTRACT_FIELD_VALUE.search(sentence)
        field = None
        value = None

        if search is not None:
            if len(search.group(1).split()) <= 5:
                field = search.group(1)
                value = search.group(2)

        return (field, value)
    
    def _extract_field_value_by_ts(self, sentence):
        tokens = nltk.word_tokenize(sentence, self.language)
        text = Text(tokens)
        ts = TokenSearcher(text)

        field = ts.findall('(<.+>{1,})<:><.+>{1,}')
        value = ts.findall('<.+>{1,}<:>(<.+>{1,})')

        field = ' '.join(field[0]) if len(field) > 0 else None
        value = ' '.join(value[0]) if len(value) > 0 else None

        return (field, value)

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
            matches = list(filter(lambda match : not match.group('field').upper() in self.IGNORED_FIELDS, matches))

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
