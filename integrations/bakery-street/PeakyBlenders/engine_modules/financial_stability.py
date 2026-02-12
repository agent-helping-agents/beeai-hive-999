# ===== FINANCIAL STABILITY RISK ASSESSMENT MODULE =====
# Advanced Implementation for Systemic Risk Analysis
# Fire Sale Amplification, Liquidity Mismatch, and Procyclical Feedback

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

class FireSaleAmplificationAnalyzer:
    """
    Analyzes fire sale amplification risk in asset manager portfolios
    Based on: "BlackRock's universal ownership position creates correlated selling pressure during market stress"
    """

    def __init__(self):
        self.portfolio_data = {}
        self.market_conditions = {}
        self.correlation_matrix = None

    def assess_fire_sale_risk(self, portfolio_data, market_conditions):
        """
        Assess systemic risk from fire sale amplification
        Based on: "Fire Sale Amplification: BlackRock's universal ownership position creates correlated selling pressure"

        Args:
            portfolio_data: Dict containing portfolio holdings, AUM, and diversification metrics
            market_conditions: Dict containing market stress indicators and volatility measures

        Returns:
            Dict with comprehensive fire sale risk assessment
        """

        print("🔥 Analyzing Fire Sale Amplification Risk...")

        # Extract key portfolio metrics
        blackrock_aum = portfolio_data.get('aum', 12.5e12)  # $12.5T default
        holdings = portfolio_data.get('holdings', {})
        diversification = portfolio_data.get('diversification_score', 0.7)

        # Market stress indicators
        market_volatility = market_conditions.get('volatility_index', 20)
        market_stress_level = market_conditions.get('stress_level', 0.5)
        liquidity_conditions = market_conditions.get('liquidity_ratio', 1.0)

        # Calculate portfolio overlap and correlation
        portfolio_overlap = self._calculate_portfolio_overlap(holdings)

        # Assess forced selling pressure under stress
        selling_pressure = self._calculate_selling_pressure(
            blackrock_aum, market_stress_level, liquidity_conditions
        )

        # Calculate amplification through network effects
        amplification_factor = self._calculate_amplification_factor(
            portfolio_overlap, selling_pressure, diversification
        )

        # Estimate market impact
        market_impact = self._estimate_market_impact(
            amplification_factor, blackrock_aum, market_volatility
        )

        # Assess contagion potential
        contagion_risk = self._assess_contagion_potential(
            amplification_factor, holdings, market_conditions
        )

        # Generate risk assessment
        risk_assessment = {
            'amplification_factor': amplification_factor,
            'market_impact_estimate': market_impact,
            'contagion_potential': contagion_risk['potential'],
            'vulnerable_sectors': contagion_risk['vulnerable_sectors'],
            'selling_pressure_index': selling_pressure,
            'portfolio_overlap_score': portfolio_overlap,
            'risk_level': self._categorize_risk_level(amplification_factor),
            'stress_test_results': self._run_stress_tests(
                portfolio_data, market_conditions, amplification_factor
            ),
            'mitigation_recommendations': self._generate_mitigation_recommendations(
                amplification_factor, contagion_risk
            )
        }

        return risk_assessment

    def _calculate_portfolio_overlap(self, holdings):
        """
        Calculate portfolio overlap that could lead to correlated selling
        Higher overlap = higher amplification risk
        """
        if not holdings:
            return 0.5  # Default moderate overlap

        # Analyze sector concentration
        sector_holdings = {}
        for holding in holdings.values():
            sector = holding.get('sector', 'other')
            weight = holding.get('weight', 0)

            if sector not in sector_holdings:
                sector_holdings[sector] = 0
            sector_holdings[sector] += weight

        # Calculate Herfindahl-Hirschman Index (HHI) for sector concentration
        hhi = sum(weight**2 for weight in sector_holdings.values())

        # Convert HHI to overlap score (0-1 scale)
        # HHI ranges from 0 (perfect diversification) to 1 (complete concentration)
        overlap_score = min(1.0, hhi * 2)  # Scale for sensitivity

        return overlap_score

    def _calculate_selling_pressure(self, aum, market_stress, liquidity_ratio):
        """
        Calculate forced selling pressure under market stress
        Based on redemption flows and liquidity constraints
        """
        # Base selling pressure from market stress
        base_pressure = market_stress * 0.3  # 30% of stress converts to selling pressure

        # Adjust for liquidity conditions
        liquidity_factor = 1 / liquidity_ratio if liquidity_ratio > 0 else 2.0

        # AUM scale factor (larger AUM = higher market impact potential)
        scale_factor = min(1.0, np.log(aum / 1e12) / np.log(12.5))  # Normalized to $12.5T

        # Calculate total selling pressure index
        selling_pressure = base_pressure * liquidity_factor * scale_factor

        return min(1.0, selling_pressure)  # Cap at 100%

    def _calculate_amplification_factor(self, portfolio_overlap, selling_pressure, diversification):
        """
        Calculate amplification factor through network effects
        Amplification occurs when multiple institutions sell similar assets simultaneously
        """
        # Base amplification from portfolio overlap
        base_amplification = portfolio_overlap * 1.5  # 1.5x amplification from overlap

        # Network effect multiplier
        network_multiplier = 1 + (selling_pressure * 2)  # Up to 3x from selling pressure

        # Diversification dampening effect
        diversification_factor = 1 - (diversification * 0.3)  # Diversification reduces amplification

        # Calculate total amplification factor
        amplification_factor = base_amplification * network_multiplier * diversification_factor

        return amplification_factor

    def _estimate_market_impact(self, amplification_factor, aum, market_volatility):
        """
        Estimate market impact of amplified selling
        Returns impact as percentage of market value
        """
        # Base impact from AUM and amplification
        base_impact = (amplification_factor * aum) / 1e12  # Trillions of dollars

        # Adjust for market volatility
        volatility_multiplier = 1 + (market_volatility / 100)  # Volatility as percentage

        # Convert to market impact percentage
        market_cap_estimate = 50e12  # Approximate global equity market cap ($50T)
        market_impact_pct = (base_impact * volatility_multiplier) / market_cap_estimate

        # Convert to dollar terms
        market_impact_dollars = market_impact_pct * market_cap_estimate

        return {
            'impact_percentage': market_impact_pct * 100,
            'impact_dollars': market_impact_dollars,
            'volatility_adjusted': volatility_multiplier,
            'time_to_recovery': self._estimate_recovery_time(market_impact_pct)
        }

    def _estimate_recovery_time(self, impact_percentage):
        """Estimate market recovery time based on impact severity"""
        if impact_percentage < 1:
            return "1-2 days"
        elif impact_percentage < 5:
            return "1-2 weeks"
        elif impact_percentage < 10:
            return "1-2 months"
        else:
            return "3+ months"

    def _assess_contagion_potential(self, amplification_factor, holdings, market_conditions):
        """
        Assess contagion potential across different sectors and asset classes
        """
        vulnerable_sectors = []
        contagion_potential = 0

        if holdings:
            # Analyze sector vulnerability
            sector_analysis = {}
            for holding in holdings.values():
                sector = holding.get('sector', 'other')
                weight = holding.get('weight', 0)
                liquidity = holding.get('liquidity_score', 0.5)

                if sector not in sector_analysis:
                    sector_analysis[sector] = {'weight': 0, 'liquidity': 0, 'holdings': 0}

                sector_analysis[sector]['weight'] += weight
                sector_analysis[sector]['liquidity'] += liquidity * weight
                sector_analysis[sector]['holdings'] += 1

            # Calculate sector vulnerability scores
            for sector, data in sector_analysis.items():
                # Vulnerability = weight * (1 - liquidity) * amplification_factor
                vulnerability = data['weight'] * (1 - data['liquidity'] / data['weight']) * amplification_factor

                if vulnerability > 0.3:  # Threshold for vulnerability
                    vulnerable_sectors.append({
                        'sector': sector,
                        'vulnerability_score': vulnerability,
                        'exposure_weight': data['weight'],
                        'liquidity_score': data['liquidity'] / data['weight'],
                        'holding_count': data['holdings']
                    })

            # Sort by vulnerability
            vulnerable_sectors.sort(key=lambda x: x['vulnerability_score'], reverse=True)

            # Calculate overall contagion potential
            contagion_potential = min(1.0, len(vulnerable_sectors) * 0.1 + amplification_factor * 0.5)

        return {
            'potential': contagion_potential,
            'vulnerable_sectors': vulnerable_sectors[:5],  # Top 5 most vulnerable
            'contagion_level': self._categorize_contagion(contagion_potential)
        }

    def _categorize_risk_level(self, amplification_factor):
        """Categorize fire sale risk level"""
        if amplification_factor >= 2.0:
            return 'extreme_risk'
        elif amplification_factor >= 1.5:
            return 'high_risk'
        elif amplification_factor >= 1.0:
            return 'moderate_risk'
        elif amplification_factor >= 0.5:
            return 'low_risk'
        else:
            return 'minimal_risk'

    def _categorize_contagion(self, contagion_potential):
        """Categorize contagion potential"""
        if contagion_potential >= 0.8:
            return 'systemic_contagion'
        elif contagion_potential >= 0.6:
            return 'sector_contagion'
        elif contagion_potential >= 0.4:
            return 'limited_contagion'
        else:
            return 'contained'

    def _run_stress_tests(self, portfolio_data, market_conditions, amplification_factor):
        """Run stress tests under various market scenarios"""
        stress_scenarios = [
            {'name': 'Mild Stress', 'volatility': 25, 'liquidity': 0.9, 'stress_level': 0.3},
            {'name': 'Moderate Stress', 'volatility': 40, 'liquidity': 0.7, 'stress_level': 0.6},
            {'name': 'Severe Stress', 'volatility': 80, 'liquidity': 0.4, 'stress_level': 0.9},
            {'name': 'Extreme Stress', 'volatility': 150, 'liquidity': 0.2, 'stress_level': 1.0}
        ]

        stress_results = []

        for scenario in stress_scenarios:
            # Recalculate amplification under stress scenario
            stress_selling_pressure = self._calculate_selling_pressure(
                portfolio_data.get('aum', 12.5e12),
                scenario['stress_level'],
                scenario['liquidity']
            )

            stress_amplification = self._calculate_amplification_factor(
                self._calculate_portfolio_overlap(portfolio_data.get('holdings', {})),
                stress_selling_pressure,
                portfolio_data.get('diversification_score', 0.7)
            )

            stress_impact = self._estimate_market_impact(
                stress_amplification,
                portfolio_data.get('aum', 12.5e12),
                scenario['volatility']
            )

            stress_results.append({
                'scenario': scenario['name'],
                'amplification_factor': stress_amplification,
                'market_impact_percentage': stress_impact['impact_percentage'],
                'market_impact_dollars': stress_impact['impact_dollars'],
                'recovery_time': stress_impact['time_to_recovery'],
                'breach_threshold': stress_impact['impact_dollars'] > 350e9  # $350B threshold
            })

        return stress_results

    def _generate_mitigation_recommendations(self, amplification_factor, contagion_risk):
        """Generate recommendations to mitigate fire sale risk"""
        recommendations = []

        if amplification_factor >= 1.5:
            recommendations.extend([
                "Implement anti-dilution liquidity management tools",
                "Establish swing pricing mechanism for large redemptions",
                "Diversify portfolio across uncorrelated asset classes",
                "Implement position limits in systemically important sectors"
            ])

        if contagion_risk['potential'] >= 0.6:
            recommendations.extend([
                "Coordinate with other major asset managers on redemption policies",
                "Establish industry-wide liquidity buffers",
                "Implement sector-specific position limits",
                "Create market-wide stress testing protocols"
            ])

        recommendations.extend([
            "Regular portfolio overlap monitoring",
            "Enhanced liquidity risk management framework",
            "Stress testing integration into investment process"
        ])

        return recommendations

class LiquidityMismatchAnalyzer:
    """
    Analyzes liquidity mismatch risk in investment funds
    Based on: "Daily liquidity promises on illiquid underlying assets across $3.1 trillion fixed income holdings"
    """

    def __init__(self):
        self.fund_data = {}
        self.liquidity_metrics = {}

    def assess_liquidity_mismatch(self, fund_portfolio, redemption_patterns):
        """
        Assess liquidity mismatch between fund promises and underlying assets
        Based on: "Liquidity Mismatch Risk: Daily liquidity promises on illiquid underlying assets"

        Args:
            fund_portfolio: Dict containing asset holdings, liquidity classifications, and AUM
            redemption_patterns: Dict containing historical redemption data and patterns

        Returns:
            Dict with comprehensive liquidity mismatch assessment
        """

        print("💧 Analyzing Liquidity Mismatch Risk...")

        # Extract portfolio liquidity profile
        liquid_assets = fund_portfolio.get('liquid_assets_pct', 0.6)
        illiquid_assets = fund_portfolio.get('illiquid_assets_pct', 0.4)
        daily_redemptions = redemption_patterns.get('daily_redemption_rate', 0.02)  # 2% daily
        aum = fund_portfolio.get('aum', 3.1e12)  # $3.1T default

        # Calculate liquidity coverage ratio
        liquidity_coverage = self._calculate_liquidity_coverage(
            liquid_assets, illiquid_assets, daily_redemptions
        )

        # Assess redemption shock impact
        shock_impact = self._assess_redemption_shock(
            aum, daily_redemptions, liquid_assets, illiquid_assets
        )

        # Calculate fire sale potential under liquidity stress
        fire_sale_potential = self._calculate_fire_sale_potential(
            shock_impact, fund_portfolio
        )

        # Generate risk assessment
        risk_assessment = {
            'liquidity_coverage_ratio': liquidity_coverage['ratio'],
            'mismatch_severity': liquidity_coverage['severity'],
            'redemption_shock_impact': shock_impact,
            'fire_sale_potential': fire_sale_potential,
            'run_risk_probability': self._calculate_run_probability(
                liquidity_coverage, redemption_patterns
            ),
            'stress_test_results': self._run_liquidity_stress_tests(
                fund_portfolio, redemption_patterns
            ),
            'regulatory_compliance': self._assess_regulatory_compliance(
                liquidity_coverage, fund_portfolio
            ),
            'mitigation_strategies': self._generate_liquidity_mitigation(
                liquidity_coverage, shock_impact
            )
        }

        return risk_assessment

    def _calculate_liquidity_coverage(self, liquid_pct, illiquid_pct, daily_redemptions):
        """Calculate liquidity coverage ratio for fund"""
        # Liquidity coverage = liquid assets / expected daily redemptions
        expected_daily_outflow = daily_redemptions

        if expected_daily_outflow > 0:
            coverage_ratio = liquid_pct / expected_daily_outflow
        else:
            coverage_ratio = float('inf')

        # Assess severity
        if coverage_ratio < 1:
            severity = 'critical_mismatch'
            severity_score = 1.0
        elif coverage_ratio < 2:
            severity = 'high_mismatch'
            severity_score = 0.7
        elif coverage_ratio < 5:
            severity = 'moderate_mismatch'
            severity_score = 0.4
        elif coverage_ratio < 10:
            severity = 'low_mismatch'
            severity_score = 0.2
        else:
            severity = 'adequate_coverage'
            severity_score = 0.0

        return {
            'ratio': coverage_ratio,
            'severity': severity,
            'severity_score': severity_score,
            'liquid_assets_pct': liquid_pct,
            'expected_daily_outflow': expected_daily_outflow
        }

    def _assess_redemption_shock(self, aum, daily_redemptions, liquid_pct, illiquid_pct):
        """Assess impact of sudden redemption shock"""
        # Calculate maximum daily outflow the fund can handle
        max_daily_liquid_outflow = liquid_pct * aum

        # Calculate actual daily redemption amount
        actual_daily_redemptions = daily_redemptions * aum

        # Calculate shock impact
        if max_daily_liquid_outflow > 0:
            shock_ratio = actual_daily_redemptions / max_daily_liquid_outflow
        else:
            shock_ratio = float('inf')

        # Calculate forced selling of illiquid assets
        if shock_ratio > 1:
            forced_selling_amount = (shock_ratio - 1) * max_daily_liquid_outflow
            forced_selling_pct = forced_selling_amount / aum
        else:
            forced_selling_amount = 0
            forced_selling_pct = 0

        return {
            'shock_ratio': shock_ratio,
            'forced_selling_amount': forced_selling_amount,
            'forced_selling_percentage': forced_selling_pct * 100,
            'max_daily_capacity': max_daily_liquid_outflow,
            'actual_daily_redemptions': actual_daily_redemptions,
            'breach_capacity': shock_ratio > 1
        }

    def _calculate_fire_sale_potential(self, shock_impact, fund_portfolio):
        """Calculate potential for fire sales under liquidity stress"""
        forced_selling_pct = shock_impact['forced_selling_percentage'] / 100

        # Fire sale potential increases with forced selling percentage
        if forced_selling_pct > 10:
            fire_sale_probability = 0.9
            fire_sale_severity = 'extreme'
        elif forced_selling_pct > 5:
            fire_sale_probability = 0.7
            fire_sale_severity = 'high'
        elif forced_selling_pct > 2:
            fire_sale_probability = 0.5
            fire_sale_severity = 'moderate'
        elif forced_selling_pct > 0.5:
            fire_sale_probability = 0.3
            fire_sale_severity = 'low'
        else:
            fire_sale_probability = 0.1
            fire_sale_severity = 'minimal'

        # Calculate price impact of forced selling
        price_impact = self._estimate_price_impact(
            forced_selling_pct, fund_portfolio.get('market_impact_sensitivity', 0.5)
        )

        return {
            'probability': fire_sale_probability,
            'severity': fire_sale_severity,
            'price_impact_estimate': price_impact,
            'forced_selling_trigger': f"{forced_selling_pct:.1f}%",
            'market_disruption_potential': self._assess_market_disruption(price_impact)
        }

    def _estimate_price_impact(self, forced_selling_pct, sensitivity):
        """Estimate price impact of forced selling"""
        # Simplified price impact model
        base_impact = forced_selling_pct * 0.5  # 0.5% price impact per 1% forced selling
        sensitivity_adjustment = sensitivity * base_impact

        return base_impact + sensitivity_adjustment

    def _assess_market_disruption(self, price_impact):
        """Assess potential for market disruption from price impact"""
        if price_impact > 5:
            return 'severe_disruption'
        elif price_impact > 2:
            return 'moderate_disruption'
        elif price_impact > 0.5:
            return 'minor_disruption'
        else:
            return 'no_significant_disruption'

    def _calculate_run_probability(self, liquidity_coverage, redemption_patterns):
        """Calculate probability of fund run based on liquidity position"""
        base_probability = 0

        # Factor 1: Liquidity coverage
        if liquidity_coverage['severity'] == 'critical_mismatch':
            base_probability += 0.4
        elif liquidity_coverage['severity'] == 'high_mismatch':
            base_probability += 0.2
        elif liquidity_coverage['severity'] == 'moderate_mismatch':
            base_probability += 0.1

        # Factor 2: Historical redemption volatility
        redemption_volatility = redemption_patterns.get('volatility', 0.5)
        base_probability += redemption_volatility * 0.2

        # Factor 3: Market sentiment
        market_sentiment = redemption_patterns.get('market_sentiment', 0.5)
        base_probability += (1 - market_sentiment) * 0.1

        return min(1.0, base_probability)

    def _run_liquidity_stress_tests(self, fund_portfolio, redemption_patterns):
        """Run liquidity stress tests under various scenarios"""
        stress_scenarios = [
            {'name': 'Normal Conditions', 'redemption_multiplier': 1.0, 'liquidity_shock': 0},
            {'name': 'Elevated Redemptions', 'redemption_multiplier': 2.0, 'liquidity_shock': 0},
            {'name': 'Liquidity Crisis', 'redemption_multiplier': 5.0, 'liquidity_shock': 0.5},
            {'name': 'Extreme Stress', 'redemption_multiplier': 10.0, 'liquidity_shock': 0.8}
        ]

        stress_results = []

        for scenario in stress_scenarios:
            # Adjust redemption rate for scenario
            base_redemption_rate = redemption_patterns.get('daily_redemption_rate', 0.02)
            stress_redemption_rate = base_redemption_rate * scenario['redemption_multiplier']

            # Adjust liquidity for scenario
            base_liquid_pct = fund_portfolio.get('liquid_assets_pct', 0.6)
            stress_liquid_pct = base_liquid_pct * (1 - scenario['liquidity_shock'])

            # Recalculate liquidity coverage
            stress_coverage = self._calculate_liquidity_coverage(
                stress_liquid_pct,
                1 - stress_liquid_pct,
                stress_redemption_rate
            )

            # Recalculate shock impact
            stress_shock = self._assess_redemption_shock(
                fund_portfolio.get('aum', 3.1e12),
                stress_redemption_rate,
                stress_liquid_pct,
                1 - stress_liquid_pct
            )

            stress_results.append({
                'scenario': scenario['name'],
                'liquidity_coverage_ratio': stress_coverage['ratio'],
                'forced_selling_percentage': stress_shock['forced_selling_percentage'],
                'breach_capacity': stress_shock['breach_capacity'],
                'survival_probability': 1 - (stress_coverage['severity_score'] * scenario['redemption_multiplier'] * 0.1)
            })

        return stress_results

    def _assess_regulatory_compliance(self, liquidity_coverage, fund_portfolio):
        """Assess compliance with regulatory liquidity requirements"""
        compliance_status = {}

        # SEC Rule 22e-4 (Liquidity Risk Management)
        sec_compliance = self._check_sec_liquidity_rules(liquidity_coverage, fund_portfolio)
        compliance_status['sec_rule_22e4'] = sec_compliance

        # EU MMFR (Money Market Fund Regulation)
        eu_compliance = self._check_eu_liquidity_rules(liquidity_coverage, fund_portfolio)
        compliance_status['eu_mmfr'] = eu_compliance

        # Overall compliance
        overall_compliant = sec_compliance['compliant'] and eu_compliance['compliant']

        return {
            'overall_compliant': overall_compliant,
            'regulatory_status': compliance_status,
            'required_actions': self._generate_compliance_actions(compliance_status)
        }

    def _check_sec_liquidity_rules(self, liquidity_coverage, fund_portfolio):
        """Check compliance with SEC liquidity rules"""
        # Simplified SEC Rule 22e-4 compliance check
        required_liquidity = 0.10  # 10% minimum for 22e-4
        actual_liquidity = fund_portfolio.get('liquid_assets_pct', 0)

        return {
            'compliant': actual_liquidity >= required_liquidity,
            'required_minimum': required_liquidity,
            'actual_liquidity': actual_liquidity,
            'deficit': max(0, required_liquidity - actual_liquidity)
        }

    def _check_eu_liquidity_rules(self, liquidity_coverage, fund_portfolio):
        """Check compliance with EU liquidity rules"""
        # Simplified EU MMFR compliance check
        required_liquidity = 0.07  # 7% minimum for EU MMFR
        actual_liquidity = fund_portfolio.get('liquid_assets_pct', 0)

        return {
            'compliant': actual_liquidity >= required_liquidity,
            'required_minimum': required_liquidity,
            'actual_liquidity': actual_liquidity,
            'deficit': max(0, required_liquidity - actual_liquidity)
        }

    def _generate_compliance_actions(self, compliance_status):
        """Generate required compliance actions"""
        actions = []

        for regulation, status in compliance_status.items():
            if not status['compliant']:
                deficit_pct = status['deficit'] * 100
                actions.append(f"Address {deficit_pct:.1f}% liquidity shortfall for {regulation.upper()}")

        if actions:
            actions.append("Implement liquidity management program")
            actions.append("Regular liquidity stress testing")
            actions.append("Enhanced liquidity risk reporting")

        return actions

    def _generate_liquidity_mitigation(self, liquidity_coverage, shock_impact):
        """Generate liquidity risk mitigation strategies"""
        mitigation = []

        if liquidity_coverage['severity_score'] > 0.5:
            mitigation.extend([
                "Implement anti-dilution liquidity management tools",
                "Establish redemption gates for extreme stress",
                "Diversify into more liquid asset classes",
                "Implement swing pricing mechanism"
            ])

        if shock_impact['breach_capacity']:
            mitigation.extend([
                "Build strategic liquidity reserves",
                "Establish credit facilities for liquidity support",
                "Implement position limits on illiquid assets",
                "Create contingency funding plans"
            ])

        mitigation.extend([
            "Regular liquidity stress testing",
            "Enhanced liquidity risk monitoring",
            "Investor communication on liquidity risks"
        ])

        return mitigation

class ProcyclicalFeedbackAnalyzer:
    """
    Analyzes procyclical feedback loops in ESG investing
    Based on: "ESG mandate reversals during political pressure periods amplify market volatility"
    """

    def __init__(self):
        self.esg_data = {}
        self.market_data = {}
        self.feedback_loops = []

    def assess_procyclical_feedback(self, esg_portfolio, market_conditions, political_events):
        """
        Assess procyclical feedback loops in ESG investing
        Based on: "Procyclical Feedback Loops: ESG mandate reversals during political pressure periods"

        Args:
            esg_portfolio: Dict containing ESG holdings, mandate details, and investment strategy
            market_conditions: Dict containing market volatility and sentiment data
            political_events: Dict containing political pressure events and ESG policy changes

        Returns:
            Dict with procyclical feedback analysis
        """

        print("🔄 Analyzing Procyclical Feedback Loops...")

        # Analyze ESG mandate stability
        mandate_stability = self._assess_mandate_stability(esg_portfolio, political_events)

        # Calculate feedback amplification
        feedback_amplification = self._calculate_feedback_amplification(
            esg_portfolio, market_conditions, political_events
        )

        # Assess market volatility impact
        volatility_impact = self._assess_volatility_impact(
            feedback_amplification, esg_portfolio, market_conditions
        )

        # Analyze policy reversal patterns
        reversal_patterns = self._analyze_reversal_patterns(
            political_events, esg_portfolio
        )

        # Generate comprehensive assessment
        assessment = {
            'mandate_stability_score': mandate_stability['score'],
            'stability_rating': mandate_stability['rating'],
            'feedback_amplification_factor': feedback_amplification['factor'],
            'volatility_impact': volatility_impact,
            'reversal_patterns': reversal_patterns,
            'systemic_risk_contribution': self._calculate_systemic_contribution(
                feedback_amplification, volatility_impact
            ),
            'policy_pressure_analysis': self._analyze_policy_pressure(
                political_events, esg_portfolio
            ),
            'mitigation_strategies': self._generate_feedback_mitigation(
                mandate_stability, feedback_amplification
            )
        }

        return assessment

    def _assess_mandate_stability(self, esg_portfolio, political_events):
        """Assess stability of ESG investment mandates under political pressure"""
        # Base stability from portfolio characteristics
        base_stability = esg_portfolio.get('mandate_strength', 0.7)
        political_sensitivity = esg_portfolio.get('political_sensitivity', 0.4)

        # Adjust for political events
        political_pressure = len(political_events) * 0.1  # Each event reduces stability by 10%

        # Calculate adjusted stability
        adjusted_stability = base_stability * (1 - political_pressure) * (1 - political_sensitivity)

        # Rating system
        if adjusted_stability >= 0.8:
            rating = 'highly_stable'
        elif adjusted_stability >= 0.6:
            rating = 'moderately_stable'
        elif adjusted_stability >= 0.4:
            rating = 'vulnerable'
        elif adjusted_stability >= 0.2:
            rating = 'highly_vulnerable'
        else:
            rating = 'extremely_vulnerable'

        return {
            'score': adjusted_stability,
            'rating': rating,
            'base_stability': base_stability,
            'political_pressure_factor': political_pressure,
            'political_sensitivity': political_sensitivity
        }

    def _calculate_feedback_amplification(self, esg_portfolio, market_conditions, political_events):
        """Calculate feedback amplification from ESG mandate changes"""
        # ESG portfolio size and market influence
        esg_aum = esg_portfolio.get('aum', 2e12)  # $2T default for ESG portfolios
        market_influence = esg_portfolio.get('market_influence', 0.3)  # 30% market influence

        # Political pressure amplification
        political_amplification = len(political_events) * 0.15  # 15% amplification per event

        # Market volatility feedback
        volatility = market_conditions.get('volatility', 0.2)
        volatility_feedback = volatility * 0.5  # 50% feedback from volatility

        # Calculate total amplification factor
        base_amplification = market_influence * 2  # 2x base amplification
        total_amplification = base_amplification * (1 + political_amplification) * (1 + volatility_feedback)

        return {
            'factor': total_amplification,
            'base_amplification': base_amplification,
            'political_contribution': political_amplification,
            'volatility_contribution': volatility_feedback,
            'market_influence': market_influence
        }

    def _assess_volatility_impact(self, feedback_amplification, esg_portfolio, market_conditions):
        """Assess market volatility impact from feedback loops"""
        amplification_factor = feedback_amplification['factor']

        # Base market volatility
        base_volatility = market_conditions.get('volatility', 0.2)

        # ESG-specific volatility contribution
        esg_volatility_contribution = amplification_factor * 0.1  # 10% of amplification becomes volatility

        # Total volatility impact
        total_volatility = base_volatility * (1 + esg_volatility_contribution)

        # Calculate volatility spike potential
        spike_potential = esg_volatility_contribution * 100  # Percentage points

        return {
            'base_volatility': base_volatility,
            'esg_contribution': esg_volatility_contribution,
            'total_volatility': total_volatility,
            'volatility_spike_potential': spike_potential,
            'market_disruption_risk': self._assess_disruption_risk(spike_potential)
        }

    def _assess_disruption_risk(self, spike_potential):
        """Assess market disruption risk from volatility spikes"""
        if spike_potential > 20:
            return 'extreme_disruption'
        elif spike_potential > 10:
            return 'high_disruption'
        elif spike_potential > 5:
            return 'moderate_disruption'
        elif spike_potential > 2:
            return 'low_disruption'
        else:
            return 'minimal_disruption'

    def _analyze_reversal_patterns(self, political_events, esg_portfolio):
        """Analyze patterns in ESG mandate reversals during political pressure"""
        reversals = []

        for event in political_events:
            # Check if event triggered ESG reversal
            if 'esg_impact' in event:
                esg_impact = event['esg_impact']

                if esg_impact.get('mandate_reversal', False):
                    reversal = {
                        'event_date': event.get('date'),
                        'political_trigger': event.get('description', 'Unknown'),
                        'reversal_magnitude': esg_impact.get('reversal_magnitude', 0),
                        'time_to_reversal': esg_impact.get('time_to_reversal', 0),
                        'market_impact': esg_impact.get('market_impact', 0),
                        'recovery_time': esg_impact.get('recovery_time', 'Unknown')
                    }
                    reversals.append(reversal)

        # Analyze patterns
        if reversals:
            avg_magnitude = np.mean([r['reversal_magnitude'] for r in reversals])
            avg_market_impact = np.mean([r['market_impact'] for r in reversals])

            patterns = {
                'total_reversals': len(reversals),
                'average_magnitude': avg_magnitude,
                'average_market_impact': avg_market_impact,
                'most_common_triggers': self._identify_common_triggers(reversals),
                'temporal_patterns': self._analyze_temporal_patterns(reversals)
            }
        else:
            patterns = {
                'total_reversals': 0,
                'message': 'No ESG mandate reversals detected in analyzed period'
            }

        return patterns

    def _identify_common_triggers(self, reversals):
        """Identify most common political triggers for ESG reversals"""
        triggers = {}
        for reversal in reversals:
            trigger = reversal.get('political_trigger', 'Unknown')
            if trigger not in triggers:
                triggers[trigger] = 0
            triggers[trigger] += 1

        # Return top triggers
        sorted_triggers = sorted(triggers.items(), key=lambda x: x[1], reverse=True)
        return sorted_triggers[:3]

    def _analyze_temporal_patterns(self, reversals):
        """Analyze temporal patterns in reversals"""
        if len(reversals) < 2:
            return {'message': 'Insufficient data for temporal analysis'}

        # Calculate time between reversals
        dates = [pd.to_datetime(r['event_date']) for r in reversals if r.get('event_date')]
        if len(dates) >= 2:
            intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
            avg_interval = np.mean(intervals)
            interval_volatility = np.std(intervals)

            return {
                'average_interval_days': avg_interval,
                'interval_volatility': interval_volatility,
                'pattern_type': 'clustered' if interval_volatility < avg_interval * 0.5 else 'random'
            }
        else:
            return {'message': 'Insufficient temporal data'}

    def _calculate_systemic_contribution(self, feedback_amplification, volatility_impact):
        """Calculate contribution to systemic risk"""
        amplification_factor = feedback_amplification['factor']
        volatility_spike = volatility_impact['volatility_spike_potential']

        # Systemic contribution combines amplification and volatility impact
        systemic_contribution = (amplification_factor * 0.4 + volatility_spike * 0.6) / 10

        if systemic_contribution > 0.8:
            risk_level = 'extreme_systemic_contribution'
        elif systemic_contribution > 0.6:
            risk_level = 'high_systemic_contribution'
        elif systemic_contribution > 0.4:
            risk_level = 'moderate_systemic_contribution'
        elif systemic_contribution > 0.2:
            risk_level = 'low_systemic_contribution'
        else:
            risk_level = 'minimal_systemic_contribution'

        return {
            'contribution_score': systemic_contribution,
            'risk_level': risk_level,
            'amplification_component': amplification_factor * 0.4,
            'volatility_component': volatility_spike * 0.6
        }

    def _analyze_policy_pressure(self, political_events, esg_portfolio):
        """Analyze policy pressure effects on ESG mandates"""
        pressure_analysis = {
            'total_events': len(political_events),
            'pressure_intensity': 0,
            'policy_areas': {},
            'temporal_distribution': {},
            'esg_impact_assessment': {}
        }

        for event in political_events:
            # Analyze pressure intensity
            pressure_intensity = event.get('pressure_intensity', 0.5)
            pressure_analysis['pressure_intensity'] += pressure_intensity

            # Categorize by policy area
            policy_area = event.get('policy_area', 'general')
            if policy_area not in pressure_analysis['policy_areas']:
                pressure_analysis['policy_areas'][policy_area] = 0
            pressure_analysis['policy_areas'][policy_area] += 1

            # Temporal distribution
            year = str(pd.to_datetime(event.get('date', '2020-01-01')).year)
            if year not in pressure_analysis['temporal_distribution']:
                pressure_analysis['temporal_distribution'][year] = 0
            pressure_analysis['temporal_distribution'][year] += 1

        # Normalize pressure intensity
        pressure_analysis['pressure_intensity'] /= max(1, len(political_events))

        return pressure_analysis

    def _generate_feedback_mitigation(self, mandate_stability, feedback_amplification):
        """Generate strategies to mitigate procyclical feedback loops"""
        mitigation = []

        if mandate_stability['score'] < 0.6:
            mitigation.extend([
                "Strengthen ESG mandate governance framework",
                "Implement multi-year commitment periods for ESG investments",
                "Diversify ESG strategies across uncorrelated approaches",
                "Establish independent ESG oversight committees"
            ])

        if feedback_amplification['factor'] > 1.5:
            mitigation.extend([
                "Implement circuit breakers for rapid ESG position changes",
                "Establish gradual transition periods for mandate adjustments",
                "Monitor political sentiment indicators",
                "Create contingency plans for policy pressure scenarios"
            ])

        mitigation.extend([
            "Regular stress testing of ESG mandates",
            "Enhanced disclosure of ESG investment risks",
            "Investor education on ESG volatility risks",
            "Development of anti-procyclical ESG strategies"
        ])

        return mitigation

# ===== MAIN FINANCIAL STABILITY ENGINE =====

class FinancialStabilityRiskEngine:
    """
    Complete financial stability risk assessment engine
    Integrates fire sale, liquidity mismatch, and procyclical feedback analysis
    """

    def __init__(self):
        self.fire_sale_analyzer = FireSaleAmplificationAnalyzer()
        self.liquidity_analyzer = LiquidityMismatchAnalyzer()
        self.procycical_analyzer = ProcyclicalFeedbackAnalyzer()

    def comprehensive_stability_analysis(self, portfolio_data, fund_data, esg_data, market_conditions, political_events):
        """
        Run comprehensive financial stability risk analysis
        """

        print("🏦 Starting Comprehensive Financial Stability Analysis...")
        print("="*70)

        # 1. Fire Sale Amplification Analysis
        print("🔥 Analyzing Fire Sale Amplification...")
        fire_sale_risks = self.fire_sale_analyzer.assess_fire_sale_risk(
            portfolio_data, market_conditions
        )

        # 2. Liquidity Mismatch Analysis
        print("💧 Analyzing Liquidity Mismatch...")
        liquidity_risks = self.liquidity_analyzer.assess_liquidity_mismatch(
            fund_data, market_conditions
        )

        # 3. Procyclical Feedback Analysis
        print("🔄 Analyzing Procyclical Feedback Loops...")
        procyclical_risks = self.procycical_analyzer.assess_procyclical_feedback(
            esg_data, market_conditions, political_events
        )

        # 4. Composite Systemic Risk Assessment
        print("🔬 Calculating Composite Systemic Risk...")
        composite_risk = self._calculate_composite_systemic_risk(
            fire_sale_risks, liquidity_risks, procyclical_risks
        )

        # 5. Generate Final Report
        final_report = {
            'fire_sale_analysis': fire_sale_risks,
            'liquidity_mismatch_analysis': liquidity_risks,
            'procyclical_feedback_analysis': procyclical_risks,
            'composite_systemic_risk': composite_risk,
            'critical_vulnerabilities': self._identify_critical_vulnerabilities(
                fire_sale_risks, liquidity_risks, procyclical_risks
            ),
            'regulatory_implications': self._assess_regulatory_implications(composite_risk),
            'recommendations': self._generate_stability_recommendations(composite_risk)
        }

        print("✅ Financial Stability Analysis Complete!")
        print("="*70)

        return final_report

    def _calculate_composite_systemic_risk(self, fire_sale, liquidity, procyclical):
        """Calculate composite systemic risk score"""
        # Extract risk scores from each analysis
        fire_sale_score = self._extract_risk_score(fire_sale, 'amplification_factor', 1.5, 2.5)
        liquidity_score = self._extract_risk_score(liquidity, 'mismatch_severity_score', 0.5, 1.0)
        procyclical_score = self._extract_risk_score(procyclical, 'feedback_amplification_factor', 1.2, 2.0)

        # Weight the components (fire sale most critical)
        composite_score = (
            fire_sale_score * 0.4 +
            liquidity_score * 0.35 +
            procyclical_score * 0.25
        )

        # Determine risk level
        if composite_score >= 0.8:
            risk_level = 'extreme_systemic_risk'
        elif composite_score >= 0.6:
            risk_level = 'high_systemic_risk'
        elif composite_score >= 0.4:
            risk_level = 'moderate_systemic_risk'
        elif composite_score >= 0.2:
            risk_level = 'low_systemic_risk'
        else:
            risk_level = 'minimal_systemic_risk'

        return {
            'composite_score': composite_score,
            'risk_level': risk_level,
            'component_scores': {
                'fire_sale': fire_sale_score,
                'liquidity': liquidity_score,
                'procyclical': procyclical_score
            },
            'most_critical_component': max([
                ('fire_sale', fire_sale_score),
                ('liquidity', liquidity_score),
                ('procyclical', procyclical_score)
            ], key=lambda x: x[1])[0]
        }

    def _extract_risk_score(self, analysis, key, moderate_threshold, high_threshold):
        """Extract and normalize risk score from analysis"""
        if key in analysis:
            raw_score = analysis[key]

            # Normalize to 0-1 scale
            if raw_score >= high_threshold:
                normalized_score = 1.0
            elif raw_score >= moderate_threshold:
                normalized_score = 0.6
            elif raw_score >= moderate_threshold * 0.5:
                normalized_score = 0.3
            else:
                normalized_score = 0.1

            return normalized_score
        else:
            return 0.0

    def _identify_critical_vulnerabilities(self, fire_sale, liquidity, procyclical):
        """Identify the most critical vulnerabilities"""
        vulnerabilities = []

        # Fire sale vulnerabilities
        if fire_sale.get('risk_level') in ['extreme_risk', 'high_risk']:
            vulnerabilities.append({
                'type': 'fire_sale_amplification',
                'severity': fire_sale['risk_level'],
                'description': f"Amplification factor of {fire_sale['amplification_factor']:.2f}",
                'market_impact': fire_sale['market_impact_estimate']['impact_dollars']
            })

        # Liquidity vulnerabilities
        if liquidity.get('mismatch_severity') in ['critical_mismatch', 'high_mismatch']:
            vulnerabilities.append({
                'type': 'liquidity_mismatch',
                'severity': liquidity['mismatch_severity'],
                'description': f"Coverage ratio of {liquidity['liquidity_coverage_ratio']:.2f}",
                'fire_sale_potential': liquidity['fire_sale_potential']['probability']
            })

        # Procyclical vulnerabilities
        if procyclical.get('feedback_amplification_factor', 0) > 1.8:
            vulnerabilities.append({
                'type': 'procyclical_feedback',
                'severity': 'high',
                'description': f"Amplification factor of {procyclical['feedback_amplification_factor']:.2f}",
                'volatility_impact': procyclical['volatility_impact']['volatility_spike_potential']
            })

        # Sort by severity
        severity_order = {'extreme_risk': 4, 'critical_mismatch': 4, 'high': 3,
                         'high_risk': 3, 'high_mismatch': 2, 'moderate': 2, 'low': 1}

        vulnerabilities.sort(key=lambda x: severity_order.get(x['severity'], 0), reverse=True)

        return vulnerabilities[:3]  # Top 3 vulnerabilities

    def _assess_regulatory_implications(self, composite_risk):
        """Assess regulatory implications of systemic risk assessment"""
        implications = []

        risk_level = composite_risk['risk_level']

        if risk_level in ['extreme_systemic_risk', 'high_systemic_risk']:
            implications.extend([
                "Immediate SIFI designation consideration",
                "Enhanced capital requirements implementation",
                "Mandatory liquidity stress testing",
                "Regular regulatory supervision intensification",
                "Cross-border regulatory coordination requirements"
            ])
        elif risk_level == 'moderate_systemic_risk':
            implications.extend([
                "Enhanced monitoring and reporting requirements",
                "Regular stress testing implementation",
                "Liquidity management program requirements",
                "Risk management framework enhancement",
                "Investor disclosure improvements"
            ])
        else:
            implications.extend([
                "Standard regulatory oversight maintenance",
                "Periodic risk assessments",
                "Basic liquidity monitoring",
                "Standard disclosure requirements"
            ])

        return implications

    def _generate_stability_recommendations(self, composite_risk):
        """Generate comprehensive stability recommendations"""
        recommendations = {
            'immediate_actions': [],
            'regulatory_measures': [],
            'risk_management': [],
            'market_structure': []
        }

        risk_level = composite_risk['risk_level']

        if risk_level in ['extreme_systemic_risk', 'high_systemic_risk']:
            recommendations['immediate_actions'].extend([
                "Implement emergency liquidity facilities",
                "Establish position limits in critical sectors",
                "Activate systemic risk oversight committees",
                "Implement mandatory position reporting",
                "Coordinate with central banks for liquidity support"
            ])

            recommendations['regulatory_measures'].extend([
                "Implement comprehensive SIFI regulatory framework",
                "Establish asset manager resolution authority",
                "Create mandatory systemic risk assessments",
                "Implement cross-border regulatory coordination",
                "Establish industry-wide liquidity standards"
            ])

        elif risk_level == 'moderate_systemic_risk':
            recommendations['risk_management'].extend([
                "Enhance internal risk management frameworks",
                "Implement comprehensive stress testing programs",
                "Develop contingency funding plans",
                "Establish early warning systems",
                "Improve liquidity risk management"
            ])

            recommendations['market_structure'].extend([
                "Promote market-making activities in stressed conditions",
                "Develop central clearing for asset manager transactions",
                "Establish industry coordination mechanisms",
                "Improve transparency in asset manager activities",
                "Create market-wide stress testing protocols"
            ])

        return recommendations

print("🏦 Financial Stability Risk Assessment Module Ready")
print("   - Fire Sale Amplification Analysis")
print("   - Liquidity Mismatch Risk Assessment")
print("   - Procyclical Feedback Loop Analysis")
print("="*60)
