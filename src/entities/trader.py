from decimal import Decimal
from datetime import datetime

import talib as ta
import numpy as np
from src.database.db import DB

from src.entities.mercadobitcoin import MBTrader
from src.entities.mercadobitcoin import MBInfo
from src.entities.user import UserMongo
from src.settings import Coin, OrderType
from src.settings import Pair
from src.settings import PORTFOLIO_INVESTMENT_PERCENTAGE


class Trader:

    def __init__(self, user, coin):
        self.MB = MBTrader()
        self.INFO = MBInfo(coin)
        self.user = UserMongo(user)
        self.coin = coin
        self.pair = f'BRL{coin}'
        self.account_info = self.MB.get_account_info()

    def has_open_orders(self):
        """Verify if has open orders. Not yet executed."""
        open_orders = self.account_info['response_data']['balance'][self.coin.lower()]['amount_open_orders'] > 0
        return open_orders

    def get_last_candles(self):
        """Candles from Mercado Bitcoin API V4"""

        now = int(datetime.now().timestamp())
        past = now - (24 * 3600)
        response = self.INFO.get_candles_1h(past, now)
        candles = [candle['close'] for candle in response['candles']]
        return candles

    def calculate_ema(self, candles):
        """
        Calculate the Exponetial Moving Average for 9 and SMA for 21 periods
        """
        nine_periods = ta.EMA(np.array(candles, dtype=float), timeperiod=9)
        twenty_one_periods = ta.SMA(np.array(candles, dtype=float), timeperiod=21)

        # smoothes the result with the SMA of the last three results
        nine_periods = list(nine_periods[-3:])
        twenty_one_periods = list(twenty_one_periods[-3:])

        nine_periods = ta.SMA(np.array(nine_periods, dtype=float), 3)
        twenty_one_periods = ta.SMA(np.array(twenty_one_periods, dtype=float), 3)

        return nine_periods[-1], twenty_one_periods[-1]

    def make_technical_analysis(self):
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
            print("\nTechnical analysis did not identify any crossing of moving averages. "
                  "Waiting for the next candlestick.")
            return None

    def get_max_investment(self, balance):
        """Returns the maximum value in BRL for the buy or sell order."""
        return float(balance) * PORTFOLIO_INVESTMENT_PERCENTAGE

    def take_decision(self):
        """Choose between buy/sell/wait next candle"""
        print("\nInitializing analysis")

        trader_decision = self.make_technical_analysis()

        if trader_decision and not self.has_open_orders():

            user = self.user.get()
            investment = self.get_max_investment(user['balance_brl'])
            limit_price = self.INFO.ticker()['ticker'][trader_decision.value]

            if trader_decision == OrderType.SELL:
                print("\nChecking Sell order possibility.")

                quantity = user[f"balance_{self.coin.lower()}"]

                if Decimal(quantity) <= 0:
                    print(f"\nNo {self.coin} amount for sell order.")
                    return None

            elif investment >= 50:
                print("\nMaking Buy order.")

                if Decimal(user[f"balance_{self.coin.lower()}"]) > 0:
                    print(f"\nWe already have {self.coin}. Buy order aborted")
                    return None

                quantity = Decimal(investment / float(limit_price))
                quantity = "{:.8f}".format(quantity)

            response = self.MB.make_order(trader_decision, Pair[self.pair], quantity, limit_price)

            if response['status_code'] == 100:

                limit_price = response["response_data"]["order"]["executed_price_avg"]
                quantity = response["response_data"]["order"]["executed_quantity"]
                fee = response["response_data"]["order"]["fee"]
                net_quantity = Decimal(quantity) - Decimal(fee)
                brl_amount = round(float(net_quantity * Decimal(limit_price)), 2)

                if trader_decision == OrderType.SELL:
                    user["balance_brl"] = user["balance_brl"] + brl_amount
                    user[f"balance_{self.coin.lower()}"] = "0"

                elif trader_decision == OrderType.BUY:
                    user["balance_brl"] = user["balance_brl"] - brl_amount
                    balance = str(Decimal(user[f"balance_{self.coin.lower()}"]) + net_quantity)
                    user[f"balance_{self.coin.lower()}"] = balance

                self.user.update(user)
                order = {
                    "user_id": user["id"],
                    "fiat": "Reais",
                    "symbol": Coin[self.coin].value,
                    "price": limit_price,
                    "pair": self.pair,
                    "order_type": trader_decision.value,
                    "quantity": quantity,
                    "fee": fee,
                    "net_quantity": str(net_quantity),
                    "created": datetime.now().isoformat()
                }
                DB.trader.order.insert_one(order)
                print(f"\n*** {trader_decision.value} order executed. ***")
            else:
                print(f"\n*** There was a problem with the {self.coin} order. "
                      f"Error: {response['error_message']}***")

        print("\nNo Order defined. We will wait next candle.")
