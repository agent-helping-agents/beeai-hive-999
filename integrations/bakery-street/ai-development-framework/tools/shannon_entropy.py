#!/usr/bin/env python3
"""
Shannon Entropy Analysis for Neuromorphic Computing
Based on research from PMC11592492 and arXiv papers
"""
import numpy as np
import json
import os

def shannon_entropy(data: np.ndarray) -> float:
    """Calculate Shannon entropy: H = -∑ pᵢ log₂ pᵢ"""
    data_nonzero = data[data > 0]
    if len(data_nonzero) == 0:
        return 0.0
    
    _, counts = np.unique(data_nonzero, return_counts=True)
    probabilities = counts / counts.sum()
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-12))
    return entropy

def analyze_spike_patterns(spike_train: np.ndarray, bin_size_ms: float = 1.0) -> dict:
    """Analyze entropy in neuronal spike patterns"""
    max_time = int(np.max(spike_train)) + 1
    bins = np.arange(0, max_time, bin_size_ms)
    binary_pattern, _ = np.histogram(spike_train, bins=bins)
    binary_pattern = (binary_pattern > 0).astype(int)
    
    spike_entropy = shannon_entropy(binary_pattern)
    
    return {
        'spike_entropy': spike_entropy,
        'spike_count': int(np.sum(binary_pattern)),
        'firing_rate': float(np.sum(binary_pattern) / (len(binary_pattern) * bin_size_ms / 1000))
    }

if __name__ == "__main__":
    print("=== Shannon Entropy Analysis Tool ===")
    
    # Generate sample spike data
    np.random.seed(42)
    spike_times = np.sort(np.random.exponential(10, 100))
    spike_times = np.cumsum(spike_times)
    
    # Analyze patterns
    results = analyze_spike_patterns(spike_times)
    
    print(f"Spike Entropy: {results['spike_entropy']:.3f} bits")
    print(f"Firing Rate: {results['firing_rate']:.2f} Hz")
    print(f"Total Spikes: {results['spike_count']}")
    print("✓ Shannon entropy analysis complete")
