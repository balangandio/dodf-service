import nltk
from bs4 import BeautifulSoup
from nltk.text import Text
from nltk import TokenSearcher

from ..model.Parameter import ParameterMap, spread_params_in_periods
from .Client import Client


class Service:
    def search(self, term, start_date, end_date):
        client = Client()

        parameters = ParameterMap(term)
        params = spread_params_in_periods(parameters, start_date, end_date)

        collection = client.request_all_pages(params)

        return {
            'term': term,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'result': collection.to_dict()
        }


def extract_text(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    strings = []
    for string in soup.stripped_strings:
        strings.append(repr(string))

    return strings

def concordance(text, term):
    text = Text(tokenize(text))
    return text.concordance_list(term)

def concordanceIndex(text, term):
    index = nltk.text.ConcordanceIndex(tokenize(text))
    return index.find_concordance(term)

def findall(text, regex):
    text = Text(tokenize(text))
    ts = TokenSearcher(text)
    return ts.findall(regex)

def sentences(text):
    return nltk.sent_tokenize(text)

def tokenize(text):
    return nltk.word_tokenize(text)

def strings_to_text(strings):
    return ' '.join(strings)