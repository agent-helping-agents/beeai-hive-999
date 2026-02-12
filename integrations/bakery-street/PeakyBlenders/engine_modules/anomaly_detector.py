import numpy as np
from typing import Dict, List, Any

class AnomalyDetector:
    """
    Predictive Anomaly Detection for causal spikes and statistical outliers
    """
    def __init__(self):
        self.detection_methods = {
            'causal_spike': self._detect_causal_spikes,
            'statistical_outlier': self._detect_statistical_outliers,
            'temporal_pattern': self._detect_temporal_patterns
        }

    def detect_anomalies(self, graph_data: Dict[str, Any], entity_events: Dict[str, List]) -> List[Dict[str, Any]]:
        """
        Main anomaly detection pipeline
        """
        anomalies = []

        # Causal spike detection
        causal_anomalies = self._detect_causal_spikes(graph_data, entity_events)
        anomalies.extend(causal_anomalies)

        # Statistical outlier detection
        outlier_anomalies = self._detect_statistical_outliers(graph_data)
        anomalies.extend(outlier_anomalies)

        # Temporal pattern detection
        temporal_anomalies = self._detect_temporal_patterns(entity_events)
        anomalies.extend(temporal_anomalies)

        return anomalies

    def _detect_causal_spikes(self, graph_data: Dict[str, Any], entity_events: Dict[str, List]) -> List[Dict[str, Any]]:
        """
        Detect causal spikes in entity relationships
        """
        anomalies = []
        adjacency = graph_data['adjacency']

        for entity_idx, entity in enumerate(graph_data['entities']):
            # Calculate connection strength changes
            connections = adjacency[entity_idx]
            avg_strength = np.mean(connections[connections > 0])

            # Check for events that might cause spikes
            for event_name, event_timeline in entity_events.items():
                if entity.lower() in event_name.lower():
                    spike_strength = np.max(event_timeline)
                    if spike_strength > 0.8:  # High spike threshold
                        anomalies.append({
                            'type': 'causal_spike',
                            'entity': f"{entity}-{event_name}",
                            'strength': spike_strength,
                            'description': f"Causal spike detected for {entity} during {event_name}",
                            'confidence': min(spike_strength, 0.95)
                        })

        return anomalies

    def _detect_statistical_outliers(self, graph_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect statistical outliers in graph metrics
        """
        anomalies = []
        adjacency = graph_data['adjacency']
        features = graph_data['features']

        # Node degree outliers
        degrees = adjacency.sum(axis=1)
        degree_mean = np.mean(degrees)
        degree_std = np.std(degrees)

        for i, degree in enumerate(degrees):
            z_score = (degree - degree_mean) / degree_std if degree_std > 0 else 0
            if abs(z_score) > 2.0:  # Z-score threshold
                anomalies.append({
                    'type': 'statistical_outlier',
                    'entity': graph_data['entities'][i],
                    'metric': 'node_degree',
                    'value': degree,
                    'z_score': z_score,
                    'description': f"Unusual node degree for {graph_data['entities'][i]}",
                    'confidence': min(abs(z_score) / 3, 0.95)
                })

        # Feature outliers
        for feature_idx in range(features.shape[1]):
            feature_values = features[:, feature_idx]
            feature_mean = np.mean(feature_values)
            feature_std = np.std(feature_values)

            for i, value in enumerate(feature_values):
                z_score = (value - feature_mean) / feature_std if feature_std > 0 else 0
                if abs(z_score) > 2.5:  # Higher threshold for features
                    anomalies.append({
                        'type': 'statistical_outlier',
                        'entity': graph_data['entities'][i],
                        'metric': f'feature_{feature_idx}',
                        'value': value,
                        'z_score': z_score,
                        'description': f"Outlier in feature {feature_idx} for {graph_data['entities'][i]}",
                        'confidence': min(abs(z_score) / 3, 0.95)
                    })

        return anomalies

    def _detect_temporal_patterns(self, entity_events: Dict[str, List]) -> List[Dict[str, Any]]:
        """
        Detect anomalous temporal patterns
        """
        anomalies = []

        for event_name, timeline in entity_events.items():
            # Calculate rate of change
            if len(timeline) > 1:
                changes = np.diff(timeline)
                max_change = np.max(np.abs(changes))

                if max_change > 0.5:  # Significant change threshold
                    peak_idx = np.argmax(np.abs(changes))
                    anomalies.append({
                        'type': 'temporal_pattern',
                        'entity': event_name,
                        'timestamp': peak_idx,
                        'significance': max_change,
                        'description': f"Sudden change in {event_name} at time {peak_idx}",
                        'confidence': min(max_change, 0.9)
                    })

            # Detect acceleration patterns
            if len(timeline) > 2 and 'changes' in locals():
                accelerations = np.diff(changes)
                max_acceleration = np.max(np.abs(accelerations))

                if max_acceleration > 0.3:  # Acceleration threshold
                    acc_idx = np.argmax(np.abs(accelerations))
                    anomalies.append({
                        'type': 'temporal_pattern',
                        'entity': event_name,
                        'timestamp': acc_idx,
                        'significance': max_acceleration,
                        'description': f"Accelerating pattern in {event_name}",
                        'confidence': min(max_acceleration * 2, 0.95)
                    })

        return anomalies