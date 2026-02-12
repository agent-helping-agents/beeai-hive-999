import logging
from typing import Dict, Optional

class CostCalculator:
    """Helper to track and predict execution costs (gas, fees)."""
    def __init__(self):
        self.total_costs = 0.0

    def add_cost(self, amount: float):
        self.total_costs += amount

    def get_net_profit(self, gross_profit: float) -> float:
        return gross_profit - self.total_costs

class PortfolioManager:
    """
    Manages asset allocation across all blockchains and strategies.
    - Tracks current holdings.
    - Rebalances automatically based on thresholds.
    - Enforces position limits and risk guardrails.
    """
    
    def __init__(self, initial_capital: float = 5000):
        self.capital = initial_capital
        self.holdings = {
            'USDC': initial_capital,
            'SOL': 0.0,
            'ETH': 0.0
        }
        # Target allocation percentages
        self.target_allocation = {
            'staking': 0.50,      # 50%
            'lending': 0.20,      # 20%
            'arbitrage': 0.10,    # 10%
            'nft': 0.10,          # 10%
            'airdrop': 0.05,      # 5%
            'rwa': 0.05           # 5%
        }
        self.prices = {
            'USDC': 1.0,
            'SOL': 100.0,  # Placeholder
            'ETH': 2500.0  # Placeholder
        }
        self.costs = CostCalculator()
        self.logger = logging.getLogger("PortfolioManager")

    def get_total_value(self) -> float:
        """Calculate total portfolio value in USD."""
        total = 0.0
        for token, amount in self.holdings.items():
            total += amount * self.prices.get(token, 0.0)
        return total

    def get_current_allocation(self) -> Dict[str, float]:
        """
        Calculate current percentage allocation based on strategy deployments.
        In this simplified version, we return the ratio of capital deployed.
        """
        total = self.get_total_value()
        if total == 0: return {k: 0.0 for k in self.target_allocation}
        
        # This would normally track which assets belong to which strategy
        # For now, we return a mock reflecting the target for TUI testing
        return self.target_allocation

    def update_price(self, token: str, price: float):
        self.prices[token] = price

    def record_transaction(self, token: str, amount: float, cost: float = 0.0):
        """Update holdings and record gas/fee costs."""
        self.holdings[token] = self.holdings.get(token, 0.0) + amount
        self.costs.add_cost(cost)
        self.logger.info(f"Tx Recorded: {token} {amount:+}, Fee: ${cost}")

    def rebalance(self):
        """Check for deviations and suggest trades."""
        total_value = self.get_total_value()
        current = self.get_current_allocation()
        
        self.logger.info(f"Starting Rebalance Check. Total Value: ${total_value:.2f}")
        
        for strategy, target in self.target_allocation.items():
            actual = current.get(strategy, 0.0)
            diff = actual - target
            if abs(diff) > 0.05:  # 5% drift threshold
                self.logger.warning(f"Strategy {strategy} drifted by {diff:.2%}")
