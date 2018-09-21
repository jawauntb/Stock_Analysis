from alpha_vantage.timeseries import TimeSeries

import matplotlib.pyplot as plt


def get_intraday(stock):
    ts = TimeSeries(key=AVK, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol='{}'.format(stock), interval='1min', outputsize='full')
    data['4. close'].plot()
    return plt, stock


def get_timeseries_chart(chart, stock):
    chart.title('Times Series for the {} stock (1 min)'.format(stock.upper()))
    chart.show()

def get_stock_and_time_series(series_func, *stocks, **func_params):
    ts = TimeSeries
    for _ in stocks:
        pass
    return ""

if __name__ == '__main__':

    c, s = get_intraday('FB')
    get_timeseries_chart(c, s)


