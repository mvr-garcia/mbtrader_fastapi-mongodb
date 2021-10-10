from src.entities.mercadobitcoin import MB


class TraderEngine:

    def __init__(self):
        self.mb = MB()

    async def can_invest(self):
        pass

    async def get_last_candles(self):
        pass

    async def analysis_sme(self):
        pass

    async def get_minimal_investment(self):
        pass
