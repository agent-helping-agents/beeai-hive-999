"""
Mathematical Models Core Module
Advanced mathematical foundations for template optimization and evolution

Copyright (c) 2025 Kiliaan Walter Vanvoorden. All Rights Reserved.

This module implements state-of-the-art mathematical models including:
- Graph Theory for template dependency analysis
- Automata Theory for template lifecycle management
- Information Theory for content complexity scoring
- Markov Decision Processes for trend prediction

Author: Kiliaan Walter Vanvoorden
Contact: kiliaanv2@gmail.com

AI Development Credits:
- Grok AI (X.AI) - Prompt engineering and quantum consciousness concepts
- Leonardo AI - Psychedelic artwork generation
- Perplexity AI - Real-time cultural trend research
- Claude (Anthropic) - Development assistance

License: Proprietary - See LICENSE file
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum
import logging
from abc import ABC, abstractmethod
import json
import pickle
from collections import defaultdict, deque
import random
import math

logger = logging.getLogger(__name__)

class TemplateState(Enum):
    """Automata states for template lifecycle"""
    DRAFT = "draft"
    ACTIVE = "active"
    TRENDING = "trending"
    PEAK = "peak"
    DECLINING = "declining"
    ARCHIVED = "archived"
    EVOLVING = "evolving"

@dataclass
class TemplateNode:
    """Represents a template in the evolution graph"""
    id: str
    category: str
    trend_intensity: float
    energy_score: float
    dependencies: Set[str]
    metadata: Dict[str, Any]

class TemplateEvolutionGraph:
    """Graph theory implementation for template evolution optimization"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, TemplateNode] = {}
        
    def add_template(self, node: TemplateNode) -> None:
        """Add template to evolution graph"""
        self.nodes[node.id] = node
        self.graph.add_node(node.id, **node.metadata)
        logger.debug(f"Added template {node.id} to evolution graph")
    
    def add_evolution_link(self, source_id: str, target_id: str, similarity: float = 0.0) -> None:
        """Add evolution relationship between templates"""
        self.graph.add_edge(source_id, target_id, similarity=similarity)
        if source_id in self.nodes:
            self.nodes[source_id].dependencies.add(target_id)
    
    def find_evolution_opportunities(self) -> List[Tuple[str, str, float]]:
        """Find templates that should evolve based on graph analysis"""
        opportunities = []
        
        # Use centrality to find influential templates
        centrality = nx.betweenness_centrality(self.graph) if self.graph.nodes() else {}
        
        for node_id, score in centrality.items():
            if score > 0.5 and node_id in self.nodes:
                node = self.nodes[node_id]
                if node.trend_intensity > 70:
                    opportunities.append((node_id, "high_influence", score))
        
        return opportunities
    
    def optimize_template_mix(self) -> Dict[str, float]:
        """Optimize template portfolio using graph metrics"""
        if not self.graph.nodes():
            return {}
        
        pagerank = nx.pagerank(self.graph)
        
        # Normalize scores
        total = sum(pagerank.values())
        return {node_id: (score / total) * 100 
                for node_id, score in pagerank.items()}

class TemplateAutomaton:
    """Finite state automaton for template lifecycle management"""
    
    def __init__(self):
        self.current_state = TemplateState.DRAFT
        self.state_transitions = self._build_transition_table()
        self.state_history: List[TemplateState] = [TemplateState.DRAFT]
        
    def _build_transition_table(self) -> Dict[TemplateState, Set[TemplateState]]:
        """Build valid state transition table"""
        return {
            TemplateState.DRAFT: {TemplateState.ACTIVE},
            TemplateState.ACTIVE: {TemplateState.TRENDING, TemplateState.ARCHIVED},
            TemplateState.TRENDING: {TemplateState.PEAK, TemplateState.DECLINING},
            TemplateState.PEAK: {TemplateState.DECLINING, TemplateState.EVOLVING},
            TemplateState.DECLINING: {TemplateState.ARCHIVED, TemplateState.EVOLVING},
            TemplateState.EVOLVING: {TemplateState.ACTIVE},
            TemplateState.ARCHIVED: set()
        }
    
    def transition_to(self, new_state: TemplateState) -> bool:
        """Attempt state transition with validation"""
        if new_state not in self.state_transitions[self.current_state]:
            logger.error(f"Invalid transition from {self.current_state} to {new_state}")
            return False
        
        self.current_state = new_state
        self.state_history.append(new_state)
        return True
    
    def should_evolve(self, trend_intensity: float, energy_score: float) -> bool:
        """Determine if template should evolve based on metrics"""
        if self.current_state in [TemplateState.PEAK, TemplateState.DECLINING]:
            return trend_intensity < 50 or energy_score < 60
        return False

class ContentComplexityAnalyzer:
    """Information theory tools for content analysis"""
    
    @staticmethod
    def calculate_entropy(content: str) -> float:
        """Calculate Shannon entropy of content"""
        if not content:
            return 0.0
        
        char_counts = defaultdict(int)
        for char in content:
            char_counts[char] += 1
        
        total_chars = len(content)
        entropy = 0.0
        
        for count in char_counts.values():
            probability = count / total_chars
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    @staticmethod
    def content_complexity_score(content: str) -> Dict[str, float]:
        """Calculate comprehensive content complexity metrics"""
        if not content:
            return {'entropy': 0, 'lexical_diversity': 0, 'complexity_score': 0}
        
        entropy = ContentComplexityAnalyzer.calculate_entropy(content)
        
        words = content.lower().split()
        lexical_diversity = len(set(words)) / len(words) if words else 0
        
        return {
            'entropy': entropy,
            'lexical_diversity': lexical_diversity,
            'complexity_score': entropy * lexical_diversity
        }

class TrendPredictionMDP:
    """Markov Decision Process for trend prediction"""
    
    def __init__(self):
        self.states = ['low', 'medium', 'high', 'peak']
        self.actions = ['wait', 'boost', 'evolve']
        self.q_table = np.zeros((len(self.states), len(self.actions)))
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        
    def predict_next_trend(self, current_intensity: float) -> str:
        """Predict next trend state"""
        if current_intensity < 30:
            return 'low'
        elif current_intensity < 60:
            return 'medium'
        elif current_intensity < 85:
            return 'high'
        return 'peak'
    
    def recommend_action(self, state: str) -> str:
        """Recommend action based on current state"""
        state_idx = self.states.index(state) if state in self.states else 0
        action_idx = np.argmax(self.q_table[state_idx, :])
        return self.actions[action_idx]
