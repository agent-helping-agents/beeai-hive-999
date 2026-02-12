# PeakyBlenders Premium Features Configuration
# Subscription tiers and feature access levels

PREMIUM_TIERS = {
    'free': {
        'name': 'Free',
        'price': 0,
        'features': [
            'basic_anomaly_detection',
            'standard_reporting',
            'community_support'
        ],
        'limits': {
            'monthly_scans': 100,
            'api_calls': 1000,
            'data_retention_days': 30
        }
    },
    'pro': {
        'name': 'Pro',
        'price': 29.99,
        'features': [
            'basic_anomaly_detection',
            'advanced_analytics',
            'real_time_monitoring',
            'priority_support',
            'custom_dashboards',
            'api_access'
        ],
        'limits': {
            'monthly_scans': 10000,
            'api_calls': 100000,
            'data_retention_days': 365
        }
    },
    'enterprise': {
        'name': 'Enterprise',
        'price': 99.99,
        'features': [
            'basic_anomaly_detection',
            'advanced_analytics',
            'real_time_monitoring',
            'priority_support',
            'custom_dashboards',
            'api_access',
            'white_label_solution',
            'dedicated_support',
            'custom_integrations',
            'on_premise_deployment'
        ],
        'limits': {
            'monthly_scans': -1,  # unlimited
            'api_calls': -1,      # unlimited
            'data_retention_days': -1  # unlimited
        }
    }
}

FEATURE_DESCRIPTIONS = {
    'basic_anomaly_detection': 'Core SNN/GNN anomaly detection engine',
    'advanced_analytics': 'Advanced temporal pattern analysis and forecasting',
    'real_time_monitoring': 'Real-time threat monitoring and alerts',
    'custom_dashboards': 'Customizable analytics dashboards',
    'api_access': 'Full REST API access with webhooks',
    'white_label_solution': 'White-label deployment option',
    'dedicated_support': 'Dedicated technical support team',
    'custom_integrations': 'Custom integration development',
    'on_premise_deployment': 'On-premise deployment support'
}

SUBSCRIPTION_BENEFITS = {
    'free': [
        'Community support via GitHub Issues',
        'Basic documentation access',
        'Monthly security updates'
    ],
    'pro': [
        'Email support with 24h response',
        'Advanced documentation and tutorials',
        'Priority feature requests',
        'Monthly webinars and updates',
        'Pro-only Discord channel'
    ],
    'enterprise': [
        'Dedicated Slack channel',
        'Phone/video support',
        'Custom SLA agreements',
        'On-site training sessions',
        'Annual security audit reports'
    ]
}