from .base_agent import BaseMonetizationAgent

class NFTTradingAgent(BaseMonetizationAgent):
    def __init__(self):
        super().__init__("NFTTrading")

    async def monitor(self):
        self.logger.info("Monitoring NFT floor prices...")
        return {"opportunities": []}

    async def execute(self, opportunity):
        pass
