from bs4 import BeautifulSoup
import nltk
from nltk import TokenSearcher
from nltk.text import Text


class Context:
    def __init__(self, document):
        self.document = document

    def document_text(self):
        content = self.document.texto
        soup = BeautifulSoup(content, 'html.parser')

        strings = []
        for string in soup.stripped_strings:
            strings.append(repr(string))

        return ' '.join(strings)

    def sentences(self):
        content = self.document_text()
        return nltk.sent_tokenize(content)

    def sentences_fields(self):
        sents = self.sentences()
        sents_fields = []
        
        for sent in sents:
            tokens = nltk.word_tokenize(sent)
            text = Text(tokens)
            ts = TokenSearcher(text)

            field = ts.findall('(<.+>)<:><.+>{1,}')
            value = ts.findall('<.+><:>(<.+>{1,})')

            field = ' '.join(field[0]) if len(field) > 0 else None
            value = ' '.join(value[0]) if len(value) > 0 else None

            sents_fields.append({
                'sentence': sent,
                'field': field,
                'value': value
            })
        
        return sents_fields

class ContratoContext(Context):
    def __init__(self, document):
        super().__init__(document)
    
    def to_dict(self):
        sents_fields = self.sentences_fields()

        return {
            'sentences': sents_fields
        }

