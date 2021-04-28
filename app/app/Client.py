import json
from functools import reduce

from HTTPConnection import HTTPConnection
from Page import PageCollection, Page


class Client:
    def __init__(self):
        self.host = 'dodf.df.gov.br'
        self.path = '/default/index/resultado-json'

    def request_all_pages(self, *params):
        connection = HTTPConnection(self.host, True)

        try:
            return self._request_params_list(connection, self._flat_args(params), True)
        finally:
            connection.close()

    def request_page(self, *params):
        connection = HTTPConnection(self.host, True)

        try:
            return self._request_params_list(connection, self._flat_args(params), False)
        finally:
            connection.close()

    def _request_params_list(self, conn, params_list, all_pages):
    	if len(params_list) == 1:
    		return self._request(conn, params_list[0], all_pages)

    	return reduce(
    		lambda prev, next : self._request(conn, prev, all_pages).extend(self._request(conn, next, all_pages)),
    		params_list
    	)

    def _request(self, connection, param_map, all_pages=False):
        response = connection.get(self.path, param_map.to_query_string())

        if response.status != 200:
            raise ValueError('Http request returned unsuccessful status code')

        if response.headers.get_content_type() != 'application/json':
            raise ValueError('Invalid content-type')

        content = response.read()

        json_result = json.loads(content)

        if 'type' in json_result and json_result['type'] == 'erro':
            error_msg = ('', ': ' + json_result['flashMsg'])['flashMsg' in json_result]
            raise ValueError('Service returned error' + error_msg)

        page = Page(json_result)

        if all_pages:
            collection = PageCollection([page])

            if page.details.is_last_page():
                return collection

            return collection.extend(self._request(connection, param_map.next_page(), all_pages))

        return page

    def _flat_args(self, args):
        args_list = []
        for arg in args:
        	if type(arg) == list:
        		args_list.extend(arg)
        	else:
        		args_list.append(arg)
        return args_list