import auth_keys
import csv, datetime
from binance.client import Client   

client = Client(auth_keys.API_KEY, auth_keys.API_SECRET)
interval = ''

def all_tickers():
    tickers = client.get_all_tickers()
    ticker_list = [ticker['symbol'] for ticker in tickers]
    return(ticker_list)

def get_data(ticker):
    global interval
    start = input('Please enter start date (format: 1 Jan 2020):  ')
    end = input('Please enter end date (format: 1 Jan 2020):  ')
    interval = input('Please enter interval:  ')

    raw_data = client.get_historical_klines(ticker, interval, start, end)
   
    return(raw_data)

def main():
    print("Binance Historical Price Generator 1.0\n")

    while True:
        ticker = input("Please input the ticker (ex. BTCUSDT, XRPUSDT, etc.)")
        ticker_list = all_tickers()
        
        if ticker not in ticker_list:
            print("Incorrect entry! Please see ticker list:")
            print(ticker_list)
            return False
        else:
            data = get_data(ticker)
            x = datetime.datetime.now()
            filename = interval + ticker + x.strftime('%m%d%y%H%M') + '.csv'
            

            with open(filename, 'w', newline='') as file:
                cwriter = csv.writer(file)
                cwriter.writerow(["**To convert back to readable time, divide by 1000 and 86400, then Add 25,569 from the UNIX time "])
                cwriter.writerow(['Open Time','Open','High','Low','Close','Vol','Close Time','Quote Asset Vol','Trades','Base AV','Quote AV','X'])
                for item in data:
#                   item[0] = (item[0] / 1000 // 86400) + 25569
                    cwriter.writerow(item)

if __name__ == "__main__":
    main()
