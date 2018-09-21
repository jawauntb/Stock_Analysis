from urllib.parse import urlparse
from tempfile import NamedTemporaryFile
import requests
import os

os.environ['ALPHAVANTAGE_API_KEY'] = 'NMCLJKKUWHB5C7D8'


class AlphaAPIShortcut(object):

    def __init__(self):
        """ Initialize keys and url to manually make api calls"""
        self._avkey = os.environ.get('ALPHAVANTAGE_API_KEY')
        self._avurl = 'https://www.alphavantage.co/query?'
        self._api_params = {'apikey': self._avkey}
        self._response = None

    def get_api_params(self):
        """ Returns the dict of current api parameters"""
        print('getting current api params')
        return self._api_params

    def set_api_params(self, **kwargs):
        """ Sets the dict of args as the new parameters, replacing any old values."""
        print('setting new api params')
        self._api_params = kwargs

    def update_param(self, key, value):
        """ Allows you to update a single parameter with a new value if its key already exist in dict."""
        if key in self._api_params:
            self._api_params[key] = value
        else:
            print('Key cannot be updated because it is not an api param.')

    def update_api_params(self, **kwargs):
        """ Update multiple params with new values if their keys already exist in dict."""
        updating = kwargs.keys()
        print('doing an update on {}'.format(updating))
        for _ in updating:
            self.update_param(_, kwargs[_])
        print(self._api_params)

    def add_new_param(self, **kwargs):
        """ Adds a dict of key/val pair(s) to an existing set of parameters."""
        params = self._api_params
        params.update(kwargs)
        self._api_params = params

    def delete_param(self, key):
        """Deletes a single param if its key exists."""
        newparams = self._api_params
        if key in newparams:
            del newparams[key]
        self._api_params = newparams

    def delete_many_params(self, *args):
        """Deletes a several params if their keys exist."""
        for _ in args:
            self.delete_param(_)

    def get_api_request(self):
        """ Allows you to use any params directly in the api to bypass any limitations of the Python wrapped package."""
        self._response = requests.get(self._avurl, self._api_params)
        return self._response

    def get_response_text(self):
        """ Writes the text of the response to a request.methodcall() to a file and returns the name of the file."""
        res = self._response
        html = res.text
        current_url = urlparse(res.url)
        site_root = current_url.scheme + '://' + current_url.netloc

        html = html.replace('href="/', 'href="{}/'.format(site_root))
        html = html.replace('src="/', 'src="{}/'.format(site_root))

        with NamedTemporaryFile(delete=False, suffix='.html') as f:
            f.write(html.encode('UTF-8'))
            print(f.name)
            return f.name


if __name__ == '__main__':
    print('creating shortcut object')
    aas = AlphaAPIShortcut()
    print(aas._api_params)

    print('adding poop param')
    aas.set_api_params(**{'poop': 'monkey'})
    print(aas._api_params)

    print('changing poop param')
    aas.update_param('poop', 'more poop')
    print(aas.get_api_params())

    print('adding new params func and symbol')
    new_params = {'function': 'TIME_SERIES_DAILY', 'symbol': 'MSFT'}

    print(aas._api_params)
    aas.add_new_param(**new_params)
    print(aas.get_api_params())

    print('changing func and symbol values')
    aas.update_api_params(**{'function': 'TIME_SERIES_INTRADAY', 'symbol': 'GOOG'})
    print(aas.get_api_params())

    print('checking to see if duplicates are permitted, adding shit param')
    aas.add_new_param(**{'function': 'TIME_SERIES_DAILY', 'shit': 'gotem', 'trash': 'trashout'})
    print(aas.get_api_params())

    print('adding empty param')
    aas.add_new_param(**{'love': ''})
    print(aas.get_api_params())

    print('deleting unusable keys/values from param')
    aas.delete_param('shit')
    print(aas.get_api_params())
    aas.delete_many_params('poop', 'trash', 'love')
    print(aas.get_api_params())

    print('adding a dictionary of useful params to prepare request')

    DATA = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': 'FB',
        'outputsize': 'compact',
        'datatype': 'json',
        'interval': '1min',
        'apikey': os.environ.get('ALPHAVANTAGE_API_KEY')
    }

    aas.set_api_params(**DATA)
    print(aas.get_api_params())

    print('sending request')
    aas.get_api_request()

    print('checking response page of request')
    aas.get_response_text()
