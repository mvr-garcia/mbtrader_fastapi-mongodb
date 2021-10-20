import requests
import csv
from datetime import datetime

import numpy as np
import talib as ta

from src.settings import OrderType


def get_last_candles(coin):
    """Candles from Mercado Bitcoin API V4"""

    now = int(datetime.now().timestamp())
    past = now - (365 * 86400)
    url = f"https://mobile.mercadobitcoin.com.br/v4/BRL{coin}/candle?from={past}&to={now}&precision=1h"
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0"}
    response = requests.get(url, headers=headers)
    response = response.json()
    candles = [candle['close'] for candle in response['candles']]
    return candles


def calculate_ema(candles):
    """
    Calculate the Exponetial Moving Average for 9 and 21 periods
    """
    nine_periods = ta.EMA(np.array(candles, dtype=float), timeperiod=9)
    twenty_one_periods = ta.EMA(np.array(candles, dtype=float), timeperiod=21)

    # smoothes the result with the SMA of the last three EMA
    nine_periods = list(nine_periods[-3:])
    twenty_one_periods = list(twenty_one_periods[-3:])

    nine_periods = ta.SMA(np.array(nine_periods, dtype=float), 3)
    twenty_one_periods = ta.SMA(np.array(twenty_one_periods, dtype=float), 3)

    return nine_periods[-1], twenty_one_periods[-1]


def make_technical_analysis():
    """
    Analyzes the EMA and returns a verdict on the
    action to be taken
    """
    previous = ""
    for coin in ['BTC', 'ETH']:
        tickers = get_last_candles(coin)
        with open('backtest.csv', 'w') as file:
            writer = csv.writer(file, delimiter='\t', lineterminator='\n',)
            i = 0
            while i < 9000:
                close = tickers[i:i + 24]
                last_candle = close[-1]
                candles = close[:len(close) - 1]
                last_candle_analyzed = candles[-1]

                short_EMA, long_EMA = calculate_ema(candles)
                if short_EMA > long_EMA and last_candle > last_candle_analyzed:
                    if previous != 'buy':
                        previous = 'buy'
                        writer.writerow([i, OrderType.BUY.value, last_candle])
                elif short_EMA < long_EMA and last_candle < last_candle_analyzed:
                    if previous != 'sell':
                        previous = 'sell'
                        writer.writerow([i, OrderType.SELL.value, last_candle])
                else:
                    print("Wait next analysis")

                i += 1
