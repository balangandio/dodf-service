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
