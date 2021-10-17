from decimal import Decimal
from datetime import date, datetime

import talib as ta
import numpy as np

from src.entities.mercadobitcoin import MBTrader
from src.entities.mercadobitcoin import MBInfo
from src.settings import OrderType
from src.settings import Pair
from src.settings import PORTFOLIO_INVESTMENT_PERCENTAGE
from src.settings import MAX_ORDERS_PER_DAY


class TraderEngine:

    def __init__(self, coin):
        self.MB = MBTrader()
        self.INFO = MBInfo()
        self.coin = coin
        self.pair = f'BRL{coin}'
        self.account_info = self.MB.get_account_info()

    async def completed_orders_quantity(self):
        """Returns a boolean after verifying order quantities and checking with bank management."""

        orders = self.MB.list_orders()['response_data']
        orders = orders.get('orders', None)[:3]

        count_orders = 0
        for order in orders[:6]:
            order_date = int(order['created_timestamp'])
            order_date = datetime.fromtimestamp(order_date).date()
            if order_date == date.today():
                count_orders += 1

        return count_orders == MAX_ORDERS_PER_DAY

    async def has_open_orders(self, coin):
        """Verify if has open orders. Not yet executed."""
        open_orders = self.account_info['response_data']['balances'][coin.name.lower()]['amount_open_orders'] > 0
        return open_orders

    async def get_last_candles(self):
        """Candles from Mercado Bitcoin API V4"""

        now = int(datetime.now().timestamp())
        past = now - (24 * 3600)
        response = self.INFO(self.coin).get_candles_1h(past, now)
        candles = [candle['close'] for candle in response['candles']]
        return candles

    async def calculate_ema(self, candles):
        """
        Calculate the Exponetial Moving Average for 9 and 21 periods
        """
        nine_periods = ta.EMA(np.array(candles, dtype=float), timeperiod=9)
        twenty_one_periods = ta.EMA(np.array(candles, dtype=float), timeperiod=21)

        return nine_periods[-1], twenty_one_periods[-1]

    async def make_technical_analysis(self):
        """
        Analyzes the EMA and returns a verdict on the
        action to be taken
        """
        tickers = self.get_last_candles()
        last_candle = tickers[-1]
        candles = tickers[:len(tickers) - 1]
        last_candle_analyzed = candles[-1]

        short_EMA, long_EMA = self.calculate_ema(candles)
        if short_EMA > long_EMA and last_candle > last_candle_analyzed:
            print("\nGolden cross identified")
            return OrderType.BUY
        elif short_EMA < long_EMA and last_candle < last_candle_analyzed:
            print("\nDeath cross identified")
            return OrderType.SELL
        else:
            print("\nTechnical analysis did not identify any crossing of moving averages."
                  "Waiting for the next candlestick.")
            return None

    async def get_max_investment(self):
        """Returns the maximum value in BRL for the buy or sell order."""
        brl_balance = self.account_info['response_data']['balances']['brl']['available']
        max_investiment = float(brl_balance) * PORTFOLIO_INVESTMENT_PERCENTAGE
        return max_investiment

    async def take_decision(self):
        """Choose between buy/sell/wait next candle"""
        print("\nInitializing analysis")

        trader_decision = self.make_technical_analysis()

        if trader_decision and not self.has_open_orders():
            investment = self.get_max_investment()
            limit_price = self.INFO.ticker(self.coin)['ticker'][trader_decision.value]

            if trader_decision == OrderType.SELL:
                print("\nChecking Sell order possibility.")
                quantity = ""  # quantidade total da coin no MongoDB
                if Decimal(quantity) <= 0:
                    print(f"\nNo {self.coin} amount for sell order.")
                    return None

            elif investment >= 50 and not self.completed_orders_quantity():
                print("\nMaking Buy order.")

                quantity = Decimal(investment / float(limit_price))
                quantity = "{:.8f}".format(quantity)

            response = self.MB.make_order(trader_decision, Pair[self.pair], quantity, limit_price)

            if response['response_data']['status_code'] == 100:
                # grava a quantidade comprada/vendida no banco
                print(f"\n*** {trader_decision.value} order executed. ***")
            else:
                print(f"\n*** There was a problem with the {self.coin} order. Please check the reason for the error. ***")

        print("\nNo Order defined. We will wait next candle.")
