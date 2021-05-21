import re
from typing import Iterable, Optional
from datetime import datetime
from functools import reduce


MONTHS_NAMES = [
    'janeiro',
    'fevereiro',
    'março',
    'abril',
    'maio',
    'junho',
    'julho',
    'agosto',
    'setembro',
    'outubro',
    'novembro',
    'dezembro'
]
MONTHS_SHORT_NAMES = [
    'jan',
    'fev',
    'mar',
    'abr',
    'maio',
    'jun',
    'jul',
    'ago',
    'set',
    'out',
    'nov',
    'dez'
]

class Month:
    def __init__(self, index: int):
        self.index = index

    def description(self):
        return MONTHS_NAMES[self.index]

    def short_description(self):
        return MONTHS_SHORT_NAMES[self.index]
    
    def month_of_the_year(self):
        return self.index + 1

    @staticmethod
    def parse_str(month: str):
        if month is None:
            return None

        month = month.strip().lower().replace('.', '')

        try:
            return Month(MONTHS_NAMES.index(month))
        except ValueError:
            pass

        try:
            return Month(MONTHS_SHORT_NAMES.index(month))
        except ValueError:
            pass
    
        return None


class Parser:
    RE_SHORT_DATE = re.compile('(?P<date>\d\d\/\d\d\/\d\d\d\d)')
    RE_LONG_DATE = re.compile('(?i)(?P<day>\d{1,2})( de)? (?P<month>[^ ]{4,9})( de)? (?P<year>\d\d\d\d)')

    def parse_short_date(self, date_str: str) -> Optional[datetime]:
        match = self.RE_SHORT_DATE.search(date_str.replace(' ', ''))

        if match != None:
            try:
                return datetime.strptime(match.group('date'), '%d/%m/%Y')
            except:
                pass
        return None

    def parse_long_date(self, date_str: str) -> Optional[datetime]:
        match = self.RE_LONG_DATE.search(date_str)

        if match != None:
            day = match.group('day')
            month = Month.parse_str(match.group('month'))
            year = match.group('year')

            if month != None:
                month = month.month_of_the_year()
                try:
                    return datetime.strptime('{}/{}/{}'.format(day, month, year), '%d/%m/%Y')
                except:
                    pass
        return None

    @staticmethod   
    def parse_date(date_str: str) -> Optional[datetime]:
        parser = Parser()
        strategies = [parser.parse_short_date, parser.parse_long_date]

        for st in strategies:
            result = st(date_str)
            if result != None:
                return result

        return None


def max_date(dates: Iterable[datetime]) -> Optional[datetime]:
    return None if len(dates) == 0 else reduce(lambda p, n : n if n > p else p, dates)
