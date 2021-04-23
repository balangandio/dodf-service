import http.client
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class HTTPConnection:
    def __init__(self, host, secure=False):
        self._connection = (http.client.HTTPConnection, http.client.HTTPSConnection)[secure](host)

    def get(self, path, query_params=None):
        if query_params is not None:
            path += '?' + query_params

        self._connection.request('GET', path)

        return self._connection.getresponse()

    def close(self):
        try:
            if self._connection is not None:
                self._connection.close()
        except:
            pass