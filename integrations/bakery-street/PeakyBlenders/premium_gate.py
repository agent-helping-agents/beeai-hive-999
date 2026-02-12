# PeakyBlenders Premium Feature Gate System
# Manages subscription tiers and feature access control

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

class SubscriptionManager:
    def __init__(self, license_file: str = 'license.json'):
        self.license_file = license_file
        self.license_data = self._load_license()

    def _load_license(self) -> Dict:
        """Load license information from file"""
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass

        # Return default free tier
        return {
            'tier': 'free',
            'expires': (datetime.now() + timedelta(days=365*100)).isoformat(),
            'features': ['basic_scanning', 'community_support'],
            'limits': {
                'monthly_scans': 100,
                'api_calls': 1000,
                'data_retention_days': 30
            },
            'usage': {
                'scans_this_month': 0,
                'api_calls_today': 0,
                'last_reset': datetime.now().isoformat()
            }
        }

    def save_license(self):
        """Save license data to file"""
        with open(self.license_file, 'w') as f:
            json.dump(self.license_data, f, indent=2)

    def get_tier(self) -> str:
        """Get current subscription tier"""
        return self.license_data.get('tier', 'free')

    def is_premium(self) -> bool:
        """Check if user has premium subscription"""
        return self.get_tier() in ['pro', 'enterprise']

    def is_enterprise(self) -> bool:
        """Check if user has enterprise subscription"""
        return self.get_tier() == 'enterprise'

    def check_feature_access(self, feature: str) -> bool:
        """Check if user has access to a specific feature"""
        features = self.license_data.get('features', [])
        return feature in features

    def check_limit(self, limit_type: str, increment: int = 0) -> bool:
        """Check if user is within usage limits"""
        limits = self.license_data.get('limits', {})
        usage = self.license_data.get('usage', {})

        if limit_type not in limits:
            return True  # No limit set

        current_usage = usage.get(limit_type, 0) + increment
        return current_usage <= limits[limit_type]

    def increment_usage(self, usage_type: str, amount: int = 1):
        """Increment usage counter"""
        if 'usage' not in self.license_data:
            self.license_data['usage'] = {}

        self.license_data['usage'][usage_type] = self.license_data['usage'].get(usage_type, 0) + amount
        self.save_license()

    def get_remaining_usage(self, limit_type: str) -> int:
        """Get remaining usage for a limit type"""
        limits = self.license_data.get('limits', {})
        usage = self.license_data.get('usage', {})

        if limit_type not in limits:
            return float('inf')  # Unlimited

        return max(0, limits[limit_type] - usage.get(limit_type, 0))

    def upgrade_license(self, new_tier: str, duration_days: int = 30):
        """Upgrade user to a new subscription tier"""
        tier_configs = {
            'free': {
                'features': ['basic_scanning', 'community_support'],
                'limits': {'monthly_scans': 100, 'api_calls': 1000, 'data_retention_days': 30}
            },
            'pro': {
                'features': ['basic_scanning', 'advanced_analytics', 'real_time_monitoring',
                           'priority_support', 'custom_dashboards', 'api_access'],
                'limits': {'monthly_scans': 10000, 'api_calls': 100000, 'data_retention_days': 365}
            },
            'enterprise': {
                'features': ['basic_scanning', 'advanced_analytics', 'real_time_monitoring',
                           'priority_support', 'custom_dashboards', 'api_access',
                           'white_label_solution', 'dedicated_support', 'custom_integrations',
                           'on_premise_deployment'],
                'limits': {'monthly_scans': -1, 'api_calls': -1, 'data_retention_days': -1}  # Unlimited
            }
        }

        if new_tier not in tier_configs:
            raise ValueError(f"Invalid tier: {new_tier}")

        self.license_data.update({
            'tier': new_tier,
            'expires': (datetime.now() + timedelta(days=duration_days)).isoformat(),
            'features': tier_configs[new_tier]['features'],
            'limits': tier_configs[new_tier]['limits']
        })

        self.save_license()
        return f"Successfully upgraded to {new_tier} tier!"

# Global subscription manager instance
subscription_manager = SubscriptionManager()

# Feature gate decorators
def require_premium(func):
    """Decorator to require premium subscription"""
    def wrapper(*args, **kwargs):
        if not subscription_manager.is_premium():
            raise PermissionError(
                "🎫 This feature requires a premium subscription!\n"
                "Upgrade to Pro or Enterprise at: https://github.com/sponsors/Bakery-street-projct\n"
                "Or visit: https://patreon.com/BakeryStreetProject"
            )
        return func(*args, **kwargs)
    return wrapper

def require_enterprise(func):
    """Decorator to require enterprise subscription"""
    def wrapper(*args, **kwargs):
        if not subscription_manager.is_enterprise():
            raise PermissionError(
                "🏢 This feature requires an enterprise subscription!\n"
                "Contact us for enterprise solutions: enterprise@bakery-street-project.com"
            )
        return func(*args, **kwargs)
    return wrapper

def check_usage_limit(limit_type: str):
    """Decorator to check usage limits"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not subscription_manager.check_limit(limit_type, 1):
                remaining = subscription_manager.get_remaining_usage(limit_type)
                tier = subscription_manager.get_tier()
                raise PermissionError(
                    f"🚫 Usage limit exceeded for {limit_type}!\n"
                    f"Current tier: {tier}\n"
                    f"Remaining: {remaining}\n"
                    "Upgrade your plan at: https://github.com/sponsors/Bakery-street-projct"
                )

            # Increment usage
            subscription_manager.increment_usage(limit_type, 1)

            return func(*args, **kwargs)
        return wrapper
    return decorator

# Utility functions for monetization
def show_subscription_status():
    """Display current subscription status"""
    tier = subscription_manager.get_tier()
    features = subscription_manager.license_data.get('features', [])
    limits = subscription_manager.license_data.get('limits', {})

    print("🎫 PeakyBlenders Subscription Status"    print(f"Tier: {tier.upper()}")
    print(f"Features: {', '.join(features)}")
    print("Limits:"
    for limit, value in limits.items():
        remaining = subscription_manager.get_remaining_usage(limit)
        if value == -1:
            print(f"  {limit}: Unlimited")
        else:
            print(f"  {limit}: {remaining}/{value}")

    if not subscription_manager.is_premium():
        print("
💡 Upgrade for premium features!"        print("  GitHub Sponsors: https://github.com/sponsors/Bakery-street-projct")
        print("  Patreon: https://patreon.com/BakeryStreetProject")

def generate_upgrade_prompt():
    """Generate upgrade prompt for locked features"""
    return """
🔒 PREMIUM FEATURE LOCKED
This advanced feature is available to Pro and Enterprise subscribers only!

🎯 Current Benefits:
• Advanced AI analysis
• Real-time monitoring
• Priority support
• API access
• Custom dashboards

💰 Upgrade Options:
• Pro (.99/mo): Full access to all features
• Enterprise (.99/mo): White-label + dedicated support

🛒 Upgrade Now:
• GitHub Sponsors: https://github.com/sponsors/Bakery-street-projct
• Patreon: https://patreon.com/BakeryStreetProject
• PayPal: https://paypal.me/BakeryStreetProject

Questions? Contact: support@bakery-street-project.com
"""

# Export functions for use in other modules
__all__ = [
    'subscription_manager',
    'require_premium',
    'require_enterprise',
    'check_usage_limit',
    'show_subscription_status',
    'generate_upgrade_prompt'
]