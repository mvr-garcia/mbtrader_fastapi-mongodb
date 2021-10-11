import talib as ta

from src.entities.mercadobitcoin import MBTrader
from src.entities.mercadobitcoin import MBInfo
from src.config.settings import OrderType


class TraderEngine:

    def __init__(self):
        self.MB = MBTrader()
        self.INFO = MBInfo()

    async def can_invest(self):
        """Método para analisar o número de ordens diárias e retornar um boolean
        se pode ou não fazer um novo investimento."""
        pass

    async def get_last_candles(self):
        """Vai na Api no MB e pega os cancles dos ultimos n periodos"""
        pass

    async def calculate_ema(self, ticker_closes):
        """
        Calculate the Exponetial Moving Average for 9 and 21 periods
        """
        nine_periods = ta.EMA(ticker_closes, timeperiod=9)
        twenty_one_periods = ta.EMA(ticker_closes, timeperiod=21)
        return nine_periods, twenty_one_periods

    async def analysis_ema(self, tickers):
        """
        Analyzes the EMA and returns a verdict on the
         action to be taken
        """
        short_EMA, long_EMA = self.calculate_ema(tickers)
        if short_EMA > long_EMA:
            return OrderType.BUY
        else:
            return OrderType.SELL

    async def get_max_investment(self):
        """pega o valor máximo para uma ordem com base na gestão de investimento"""

        pass

    async def take_decision(self):
        """Toma a decisão entre compra/venda/continue"""
        pass
