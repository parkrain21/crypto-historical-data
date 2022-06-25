from binance.client import Client
from binance.enums import HistoricalKlinesType
from binance.exceptions import BinanceAPIException
from numpy import iterable
from keys import *
import os, time
import pandas as pd


pd.set_option('display.max_columns', None)

def init():
    client = Client(B_API_KEY,B_API_SECRET)
    return client


def getPriceData(pair, interval, window, sf='SPOT') -> pd.DataFrame:
    """ 
    Fetches the historical candlestick data using the specified pair, interval, and lookback period.
    
    :param str pair: Asset ticker/pair (e.g. BTCUSDT, ETHUSDT, etc.)
    :param str interval: timeframe used for the query (eg. 1m, 3m, 1h, 1d, etc.)
    :param str window: date range (e.g 3 days ago, 1 year ago, etc.)
    :return dataframe: time-indexed OHLCV dataframe

    """

    if sf == 'SPOT': 
        sf = HistoricalKlinesType.SPOT
    if sf == 'FUTURES': 
        sf = HistoricalKlinesType.FUTURES

    try:
        df = pd.DataFrame(client.get_historical_klines(pair, interval, window, klines_type=sf))
    except BinanceAPIException as e:
        print(e.message)
        time.sleep(60)
        df = pd.DataFrame(client.get_historical_klines(pair, interval, window, klines_type=sf))
    df = df.iloc[:,:6]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')
    df.set_index('Time', inplace=True)
    df = df.astype(float)

    #export the data to a .csv format inside 'prices' folder
    if not os.path.exists('prices'):
        os.makedirs('prices')
    # df.to_csv(f'prices/{pair}_{interval}_{str(int(time.time()))}.csv')
    df.to_csv(f'prices/{pair}.csv')

    # Return the trimmed dataframe containing only the OHLCV values + time as index.
    return df

def get_top_coins(limit=None, pair='USDT'):
    """ 
    Fetches the top n pairs sorted by 24H trading volume. 
    
    :param int limit: fetches only the top n rows
    :param str pair: Only returns the matching pairs for this string. 
                    Example: pair = 'USDT'  --> Only returns all USDT pairs (BTCUSDT, ETHUSDT, etc.)  

    """
    # Fetches all the crypto tickers from the Binance API.
    all_tickers = pd.DataFrame(client.get_ticker())
    usdt_tickers = all_tickers.loc[all_tickers['symbol'].str.contains(f'{pair}$', regex=True)]
    usdt_tickers = usdt_tickers.loc[~all_tickers['symbol'].str.contains('UP|DOWN', regex=True)]
    usdt_tickers = usdt_tickers.loc[~all_tickers['symbol'].str.contains('^BUSD|USDC|UST', regex=True)]
    
    for column in usdt_tickers.iloc[:, 1:16].columns:
        usdt_tickers[column] = pd.to_numeric(usdt_tickers[column])

    # openTime and closeTime should only have 10 digits to be converted
    usdt_tickers['openTime'] = pd.to_datetime(usdt_tickers['openTime'], unit='ms')
    usdt_tickers['closeTime'] = pd.to_datetime(usdt_tickers['closeTime'], unit='ms')

    # Sort the whole DF by highest USDT trading volume first
    usdt_tickers.sort_values('quoteVolume', ascending=False, inplace=True)
    usdt_tickers.set_index(usdt_tickers['symbol'], inplace=True)

    if limit == None:
        # Return the whole dataframe
        return usdt_tickers
    else:
        return usdt_tickers.iloc[:limit]


if __name__ == '__main__':
    client = init()
    # top_coins = get_top_coins(5)
    # top_coins_tickers = top_coins.symbol.to_list()
    # print(top_coins_tickers)
