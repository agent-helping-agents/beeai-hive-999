import numpy as np
from typing import Dict, List, Any

class ExplainableAI:
    """
    Explainable AI layer for cluster analysis and feature importance
    """
    def __init__(self):
        self.explanation_methods = {
            'feature_importance': self._compute_feature_importance,
            'timeline_evidence': self._extract_timeline_evidence,
            'counterfactual_analysis': self._generate_counterfactuals
        }

    def explain_cluster(self, cluster_data: Dict[str, Any], model_weights: Dict[str, float], anomalies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Main explanation pipeline for cluster analysis
        """
        # Compute feature importance
        feature_importance = self._compute_feature_importance(cluster_data, model_weights)

        # Extract timeline evidence
        timeline_evidence = self._extract_timeline_evidence(cluster_data, anomalies)

        # Generate counterfactual scenarios
        counterfactuals = self._generate_counterfactuals(cluster_data, feature_importance)

        # Calculate overall confidence
        confidence_score = self._calculate_confidence(cluster_data, feature_importance, timeline_evidence)

        return {
            'cluster_id': cluster_data.get('id', 'unknown'),
            'feature_importance': feature_importance,
            'timeline_evidence': timeline_evidence,
            'counterfactual_scenarios': counterfactuals,
            'confidence_score': confidence_score,
            'explanation_summary': self._generate_summary(feature_importance, timeline_evidence)
        }

    def _compute_feature_importance(self, cluster_data: Dict[str, Any], model_weights: Dict[str, float]) -> Dict[str, float]:
        """
        Compute feature importance scores
        """
        features = cluster_data.get('features', np.array([]))
        feature_names = ['regulatory_capture', 'political_connections', 'financial_flows',
                        'market_dominance', 'media_influence']

        importance_scores = {}

        if len(features) > 0:
            # Normalize features
            normalized_features = (features - np.min(features)) / (np.max(features) - np.min(features) + 1e-8)

            for i, feature_name in enumerate(feature_names):
                if i < len(normalized_features):
                    # Combine feature value with model weight
                    weight = model_weights.get(feature_name, 0.1)
                    importance = normalized_features[i] * weight
                    importance_scores[feature_name] = float(importance)
                else:
                    importance_scores[feature_name] = 0.0
        else:
            # Default importance if no features provided
            for feature_name in feature_names:
                importance_scores[feature_name] = model_weights.get(feature_name, 0.1)

        # Normalize to sum to 1
        total_importance = sum(importance_scores.values())
        if total_importance > 0:
            importance_scores = {k: v / total_importance for k, v in importance_scores.items()}

        return importance_scores

    def _extract_timeline_evidence(self, cluster_data: Dict[str, Any], anomalies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract relevant timeline evidence from cluster data
        """
        timeline_data = cluster_data.get('temporal_data', [])
        evidence = []

        for event in timeline_data:
            # Check if event is relevant to anomalies
            relevant_anomalies = [
                anomaly for anomaly in anomalies
                if event.get('type', '') in anomaly.get('type', '') or
                any(keyword in event.get('description', '').lower()
                    for keyword in ['appointment', 'meeting', 'policy', 'regulation'])
            ]

            if relevant_anomalies or event.get('importance', 0) > 0.7:
                evidence.append({
                    'timestamp': event.get('timestamp', 'unknown'),
                    'type': event.get('type', 'event'),
                    'description': event.get('description', ''),
                    'importance': event.get('importance', 0.5),
                    'related_anomalies': len(relevant_anomalies),
                    'confidence': min(event.get('importance', 0.5) + 0.2 * len(relevant_anomalies), 1.0)
                })

        # Sort by importance
        evidence.sort(key=lambda x: x['importance'], reverse=True)

        return evidence[:5]  # Return top 5 evidence items

    def _generate_counterfactuals(self, cluster_data: Dict[str, Any], feature_importance: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Generate counterfactual scenarios
        """
        counterfactuals = []

        # Identify most important features
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]

        for feature_name, importance in top_features:
            # What-if scenario: reduce this feature
            reduced_impact = importance * 0.3  # 70% reduction

            counterfactuals.append({
                'scenario': f"What if {feature_name.replace('_', ' ')} was reduced by 70%",
                'affected_feature': feature_name,
                'impact_change': -reduced_impact,
                'description': f"Reducing {feature_name} would decrease cluster significance by {reduced_impact:.2f}",
                'likelihood': 0.8
            })

            # What-if scenario: increase this feature
            increased_impact = importance * 0.5  # 50% increase

            counterfactuals.append({
                'scenario': f"What if {feature_name.replace('_', ' ')} was increased by 50%",
                'affected_feature': feature_name,
                'impact_change': increased_impact,
                'description': f"Increasing {feature_name} would boost cluster significance by {increased_impact:.2f}",
                'likelihood': 0.6
            })

        return counterfactuals[:4]  # Return top 4 counterfactuals

    def _calculate_confidence(self, cluster_data: Dict[str, Any], feature_importance: Dict[str, float], timeline_evidence: List[Dict[str, Any]]) -> float:
        """
        Calculate overall explanation confidence
        """
        # Base confidence from feature consistency
        feature_consistency = 1.0 - np.std(list(feature_importance.values()))

        # Evidence strength
        evidence_strength = min(len(timeline_evidence) / 5, 1.0)

        # Data quality factor
        data_quality = 1.0 if cluster_data.get('features') is not None else 0.7

        confidence = (feature_consistency * 0.4 + evidence_strength * 0.4 + data_quality * 0.2)

        return min(float(confidence), 1.0)

    def _generate_summary(self, feature_importance: Dict[str, float], timeline_evidence: List[Dict[str, Any]]) -> str:
        """
        Generate human-readable explanation summary
        """
        top_feature = max(feature_importance.items(), key=lambda x: x[1])

        summary = f"This cluster is primarily characterized by {top_feature[0].replace('_', ' ')} "
        f"(importance: {top_feature[1]:.2f}). "

        if timeline_evidence:
            summary += f"Key evidence includes {len(timeline_evidence)} significant events, "
            f"with the most important being: {timeline_evidence[0]['description'][:50]}..."

        return summary