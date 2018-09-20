from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import requests
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile
import os


os.environ['ALPHAVANTAGE_API_KEY'] = 'NMCLJKKUWHB5C7D8'
AVK = os.environ.get('ALPHAVANTAGE_API_KEY')
API_URL = 'https://www.alphavantage.co/query?'


def update_api_params(current_params=None, **kwargs):
    """ update the data params with new values. """
    updating = kwargs.keys()
    for _ in updating:
        if has_key(_, **current_params):
            current_params[_] = kwargs[_]
        else:
            print('Keys cannot be updated because they are not in params.')


def has_key(key, **kwargs):
    """ Checks a dictionary to make sure the key is there"""
    haskey = False
    for akey in kwargs.keys():
        if akey == key:
            haskey = True
    return haskey


def get_response_page(self):
    """ Writes the page source of the response to a file and returns the name of the file. """
    html = self.text
    current_url = urlparse(self.url)
    site_root = current_url.scheme + '://' + current_url.netloc

    html = html.replace('href="/', 'href="{}/'.format(site_root))
    html = html.replace('src="/', 'src="{}/'.format(site_root))

    with NamedTemporaryFile(delete=False, suffix='.html') as f:
        f.write(html.encode('UTF-8'))
        print(f.name)
        return f.name


def get_api_response(api_url, **params):
    """allows you to use any params directly in the api to bypass any limitations of the Python wrapped package"""
    response = requests.get(api_url, params=params)
    return response


def get_intraday(symbol):
    ts = TimeSeries(key=AVK, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol='{}'.format(symbol), interval='1min', outputsize='full')
    data['4. close'].plot()
    return plt, symbol


def get_timeseries_chart(chart, symbol):
    chart.title('Times Series for the {} stock (1 min)'.format(symbol.upper()))
    chart.show()


if __name__ == '__main__':

    c, s = get_intraday('FB')
    get_timeseries_chart(c, s)

    DATA = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': 'MSFT',
        'outputsize': 'compact',
        'datatype': 'json',
        'interval': '1min',
        'apikey': AVK,
    }

    get_response_page(get_api_response(API_URL, **DATA))
    update_api_params(**{'symbol': 'FB'}, current_params=DATA)
    get_api_response(API_URL, **DATA)
    print(DATA['symbol'])
