import logging
from typing import Dict, List, Optional

class ThresholdChecker:
    """Helper to check values against defined thresholds."""
    def __init__(self, thresholds: Dict[str, float]):
        self.thresholds = thresholds

    def is_exceeded(self, key: str, value: float) -> bool:
        if key not in self.thresholds:
            return False
        return value > self.thresholds[key]

    def get_deviation(self, key: str, value: float) -> float:
        if key not in self.thresholds:
            return 0.0
        return value - self.thresholds[key]

class RiskCalculator:
    """
    Calculates risk metrics and enforces safety guardrails.
    - Value at Risk (VaR).
    - Max position sizes.
    - Liquidation risk alerts.
    - Outcome simulations.
    """
    
    def __init__(self, thresholds: Optional[Dict[str, float]] = None):
        self.logger = logging.getLogger("RiskCalculator")
        # Default thresholds
        default_thresholds = {
            'max_va_r': 0.15,          # 15% Max Value at Risk
            'liquidation_danger': 0.80, # 80% health factor threshold
            'max_drawdown': 0.10       # 10% max drawdown before freeze
        }
        self.checker = ThresholdChecker(thresholds or default_thresholds)

    def calculate_va_r(self, portfolio: Dict) -> float:
        """
        Calculate the Value at Risk for the current portfolio.
        Currently using a simplified model based on asset volatility.
        """
        self.logger.info("Calculating portfolio VaR...")
        # Simplified: weighted average of assumed asset risks
        # In production, this would use historical price data
        va_r = 0.05 
        if self.checker.is_exceeded('max_va_r', va_r):
            self.logger.warning(f"VaR {va_r} exceeds threshold!")
        return va_r

    def get_max_position_size(self, strategy_capital: float, risk_score: float = 1.0) -> float:
        """
        Calculate the maximum allowed position size for a strategy.
        strategy_capital: Capital allocated to this specific strategy.
        risk_score: A multiplier based on market conditions (0.0 to 1.0).
        """
        # Rule: Never deploy more than 80% of strategy capital at once
        base_limit = strategy_capital * 0.8
        return base_limit * risk_score

    def check_liquidation_risk(self, position: Dict) -> float:
        """
        Evaluate the risk of liquidation for a leveraged position.
        Returns a risk score from 0.0 to 1.0.
        """
        # Example position: {'collateral': 1000, 'debt': 500, 'threshold': 0.8}
        if 'debt' not in position or position['debt'] == 0:
            return 0.0
            
        current_ratio = position['debt'] / position['collateral']
        liquidation_threshold = position.get('threshold', 0.8)
        
        risk_score = current_ratio / liquidation_threshold
        
        if self.checker.is_exceeded('liquidation_danger', risk_score):
            self.logger.critical(f"LIQUIDATION RISK DETECTED: {risk_score:.2f}")
            
        return min(risk_score, 1.0)
