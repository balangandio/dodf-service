from datetime import datetime
from functools import reduce


class PeriodParameter:
    def __init__(self, year, params_dic = None):
        self.params = dict() if params_dic is None else params_dic
        self.set_ano(year)

    def set_ano(self, year):
        self.params['ano'] = year
        return self

    def set_inicio(self, day_of_the_year):
        self.params['dtInicial'] = datetime.strptime(day_of_the_year, '%d/%m').strftime('%d/%m')
        return self

    def set_final(self, day_of_the_year):
        self.params['dtFinal'] = datetime.strptime(day_of_the_year, '%d/%m').strftime('%d/%m')
        return self


class ParameterMap:
    def __init__(self, termo=None):
        self.params = dict()
        if termo is not None:
        	self.set_termo(termo)
        self.set_tipo_busca()
        self.set_tipo_secao()
        self.set_tipo_jornal()
        self.set_tipo_local_busca()
        self.set_pagina()

    def set_termo(self, termo):
        self.params['termo'] = termo
        return self

    def set_tipo_busca(self, tipo = 'Contexto'):
        self.params['tpBusca'] = tipo
        return self

    def set_tipo_secao(self, tipo = 'Todas'):
        self.params['tpSecao'] = tipo
        return self

    def set_tipo_jornal(self, tipo = 'Todos'):
        self.params['tpJornal'] = tipo
        return self

    def set_tipo_local_busca(self, tipo = 'tudo'):
        self.params['tpLocalBusca'] = tipo
        return self

    def set_pagina(self, page = 1):
        self.params['pagina'] = page
        return self

    def periodo(self, ano):
        return PeriodParameter(ano, self.params)

    def next_page(self):
        if 'pagina' in self.params:
            self.set_pagina(self.params['pagina'] + 1)
        else:
            self.set_pagina(1)
        return self

    def to_query_string(self):
        params = list(map(lambda p : p[0] + '=' + str(p[1]), self.params.items()))
        return reduce(lambda p, n : p + '&' + n, params)

    def set_params(self, params_dic):
    	self.params = params_dic
    	return self

    def copy(self, period=None):
    	new_one = ParameterMap()
    	new_one.set_params(self.params.copy())

    	if period is not None:
    		for item in period.params.items():
    			new_one.params[item[0]] = item[1]

    	return new_one


def spread_params_in_periods(param_map, start_date, end_date):
	periods = periods_in_between(start_date, end_date)

	return list(map(lambda period : param_map.copy(period), periods))


def periods_in_between(start_date, end_date):
    if start_date > end_date:
        raise ValueError('Start date should not be greater than end date')

    if start_date.year == end_date.year:
        return [
            PeriodParameter(start_date.year)
                .set_inicio(start_date.strftime('%d/%m'))
                .set_final(end_date.strftime('%d/%m'))
        ]

    periods = []

    for year in range(start_date.year, end_date.year + 1):
        if year == start_date.year:
            periods.append(
                PeriodParameter(start_date.year)
                    .set_inicio(start_date.strftime('%d/%m'))
                    .set_final('31/12')
            )
        elif year == end_date.year:
            periods.append(
                PeriodParameter(end_date.year)
                    .set_inicio('01/01')
                    .set_final(end_date.strftime('%d/%m'))
            )
        else:
            periods.append(
                PeriodParameter(year)
                    .set_inicio('01/01')
                    .set_final('31/12')
            )

    return periods