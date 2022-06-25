# crypto-historical-data
Collection of python test scripts to generate historical data

`NOTE`: Create a auth_keys.py file containing the API_KEY and API_SECRET variables. Get this from the Binance site.

**hist_prices_to_csv.py**
  1. Follow the prompts on the terminal.
  2. CSV file will be automatically generated on the same directory

**streamer.py**
  1. This is a websocket based kline generator. You can edit the interval and the pair in line 5.
  2. Crypto data is printed on the terminal every second

**pricegen.py**
  This script contains the following functions:
      - getPriceData --> Main generating function of this script, saves the output on a CSV file
      - get_top_coins --> Fetches the top n pairs sorted by 24H trading volume. 

  `Usage`
  
  ```python
  from pricegen import *
  
  client = init()
  
  top_coins = get_top_coins(5)    # parameter works like the pandas head() function.
  top_coins_tickers = top_coins.symbol.to_list()
  
  # Loop through the top tickers and generate one year worth of daily candles in a CSV format.
  for ticker in top_coins_tickers():
      getPriceData(ticker, '1d', '1 year ago')
  ```
