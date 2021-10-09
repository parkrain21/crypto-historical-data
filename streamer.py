import websocket, json, csv
import pandas as pd

# ticker is always lowercase
socket = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
prices = []

def on_message(ws, message):
    m = json.loads(message)
    candles = m['k']

    if candles['x'] == True:
        prices.append([candles['o'],candles['h'],candles['l'],candles['c'],candles['v']])
        print(prices)

def on_close(ws):
    print("Socket Closed!")

ws = websocket.WebSocketApp(socket,
                            on_message=on_message,
                            on_close=on_close)
ws.run_forever()