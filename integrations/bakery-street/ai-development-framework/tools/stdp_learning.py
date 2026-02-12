#!/usr/bin/env python3
"""
STDP Learning Implementation
Based on research from binds.cs.umass.edu/pdfs/stdp.pdf
"""
import numpy as np

class STDPLearning:
    """Spike-timing dependent plasticity learning rule"""
    
    def __init__(self, A_plus=0.1, A_minus=0.12, tau_plus=20.0, tau_minus=20.0):
        self.A_plus = A_plus
        self.A_minus = A_minus
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        
    def update_weight(self, delta_t: float, current_weight: float) -> float:
        """Update synaptic weight based on spike timing difference"""
        if delta_t > 0:  # Post after pre (LTP)
            dw = self.A_plus * np.exp(-delta_t / self.tau_plus)
        else:  # Pre after post (LTD)
            dw = -self.A_minus * np.exp(delta_t / self.tau_minus)
            
        new_weight = np.clip(current_weight + dw, 0, 1)
        return new_weight

if __name__ == "__main__":
    print("=== STDP Learning Demonstration ===")
    
    stdp = STDPLearning()
    
    scenarios = [
        (10, "Post 10ms after pre (LTP)"),
        (-10, "Pre 10ms after post (LTD)"), 
        (50, "Post 50ms after pre (weak LTP)"),
        (-50, "Pre 50ms after post (weak LTD)")
    ]
    
    initial_weight = 0.5
    print(f"Initial weight: {initial_weight}")
    
    for delta_t, description in scenarios:
        new_weight = stdp.update_weight(delta_t, initial_weight)
        change = new_weight - initial_weight
        print(f"{description}: {new_weight:.4f} (Δw = {change:+.4f})")
    
    print("✓ STDP learning demonstration complete")
