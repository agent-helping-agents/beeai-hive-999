"""
Hybrid LLM Router - Local vs Cloud Backend Selector

The Hive 999 now supports DUAL backend architecture:

LOCAL (Ollama) - Privacy, no API costs, works offline:
  • granite3.3:8b    - General purpose, Queen Bee primary
  • marco-o1:latest  - Reasoning tasks, complex analysis
  • deepseek-r1:8b   - Deep reasoning, alternative to marco-o1
  • llama3.1:8b      - Fast responses, Workers/Drones/Foragers
  • nomic-embed-text - Embeddings

CLOUD (LangChain/LangSmith) - Speed, scale, monitoring:
  • OpenAI GPT-4     - When speed is critical
  • Claude 3         - Long context analysis
  • LangSmith        - Tracing, monitoring, evaluation

ROUTING STRATEGY:
  • Use LOCAL for: Privacy-sensitive, offline, cost-conscious
  • Use CLOUD for: Production scale, latency-critical, monitored
  
WORKER OPTIMIZATION:
  The user is CORRECT - LangChain agents with cloud APIs can be faster
  for simple Worker/Drone tasks due to:
  1. No local GPU loading overhead
  2. Optimized inference infrastructure
  3. Parallelization through LangSmith
"""

import os
from enum import Enum
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass


class BackendType(Enum):
    """Available backend types."""
    OLLAMA = "ollama"
    LANGCHAIN = "langchain"
    AUTO = "auto"  # Route based on task complexity


class ModelRole(Enum):
    """Model roles in the Hive."""
    QUEEN_PRIMARY = "queen_primary"      # granite3.3:8b / GPT-4
    QUEEN_REASONING = "queen_reasoning"  # marco-o1 / Claude-3-Opus
    WORKER_FAST = "worker_fast"          # llama3.1:8b / GPT-3.5
    WORKER_DEEP = "worker_deep"          # deepseek-r1:8b / GPT-4
    EMBEDDING = "embedding"              # nomic-embed-text / OpenAI-ada-002


@dataclass
class ModelConfig:
    """Configuration for a model."""
    name: str
    backend: BackendType
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: float = 30.0


# ============================================================================
# LOCAL (OLLAMA) CONFIGURATION
# ============================================================================

OLLAMA_MODELS = {
    ModelRole.QUEEN_PRIMARY: ModelConfig(
        name="granite3.3:8b",
        backend=BackendType.OLLAMA,
        temperature=0.7,
        timeout=60.0
    ),
    ModelRole.QUEEN_REASONING: ModelConfig(
        name="marco-o1:latest",  # NEW: Alibaba reasoning model
        backend=BackendType.OLLAMA,
        temperature=0.8,
        timeout=120.0  # Reasoning takes longer
    ),
    ModelRole.WORKER_FAST: ModelConfig(
        name="llama3.1:8b",  # Your existing model
        backend=BackendType.OLLAMA,
        temperature=0.6,
        timeout=30.0
    ),
    ModelRole.WORKER_DEEP: ModelConfig(
        name="deepseek-r1:8b",  # NEW: Deep reasoning
        backend=BackendType.OLLAMA,
        temperature=0.7,
        timeout=60.0
    ),
    ModelRole.EMBEDDING: ModelConfig(
        name="nomic-embed-text",
        backend=BackendType.OLLAMA,
        temperature=0.0,
        timeout=10.0
    ),
}


# ============================================================================
# CLOUD (LANGCHAIN) CONFIGURATION
# ============================================================================

LANGCHAIN_MODELS = {
    ModelRole.QUEEN_PRIMARY: ModelConfig(
        name="gpt-4",
        backend=BackendType.LANGCHAIN,
        temperature=0.7,
        timeout=30.0
    ),
    ModelRole.QUEEN_REASONING: ModelConfig(
        name="claude-3-opus-20240229",
        backend=BackendType.LANGCHAIN,
        temperature=0.8,
        timeout=60.0
    ),
    ModelRole.WORKER_FAST: ModelConfig(
        name="gpt-3.5-turbo",
        backend=BackendType.LANGCHAIN,
        temperature=0.6,
        timeout=15.0  # Much faster than local
    ),
    ModelRole.WORKER_DEEP: ModelConfig(
        name="gpt-4-turbo-preview",
        backend=BackendType.LANGCHAIN,
        temperature=0.7,
        timeout=30.0
    ),
    ModelRole.EMBEDDING: ModelConfig(
        name="text-embedding-3-small",
        backend=BackendType.LANGCHAIN,
        temperature=0.0,
        timeout=5.0
    ),
}


# ============================================================================
# ROUTER CLASS
# ============================================================================

class LLMRouter:
    """
    Intelligent router for LLM backends.
    
    Usage:
        router = LLMRouter()  # Defaults to OLLAMA
        
        # Or specify backend
        router = LLMRouter(default_backend=BackendType.LANGCHAIN)
        
        # Get model for specific role
        config = router.get_config(ModelRole.WORKER_FAST)
        
        # Auto-route based on task
        config = router.route_task(
            task_complexity="high",
            privacy_required=True,
            latency_sensitivity="low"
        )
    """
    
    def __init__(
        self,
        default_backend: BackendType = BackendType.OLLAMA,
        langsmith_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
    ):
        self.default_backend = default_backend
        self.langsmith_api_key = langsmith_api_key or os.getenv("LANGSMITH_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        
        # Check cloud availability
        self.cloud_available = all([
            self.langsmith_api_key,
            self.openai_api_key or self.anthropic_api_key
        ])
        
    def get_config(self, role: ModelRole, force_backend: Optional[BackendType] = None) -> ModelConfig:
        """Get model configuration for a role."""
        backend = force_backend or self.default_backend
        
        if backend == BackendType.LANGCHAIN and not self.cloud_available:
            print(f"[LLMRouter] Cloud not configured, falling back to Ollama for {role.value}")
            backend = BackendType.OLLAMA
        
        if backend == BackendType.LANGCHAIN:
            return LANGCHAIN_MODELS[role]
        else:
            return OLLAMA_MODELS[role]
    
    def route_task(
        self,
        task_complexity: str = "medium",  # low, medium, high
        privacy_required: bool = True,
        latency_sensitivity: str = "medium",  # low, medium, high
        cost_sensitive: bool = True,
    ) -> tuple[ModelRole, ModelConfig]:
        """
        Intelligently route a task to the optimal model.
        
        Returns:
            Tuple of (ModelRole, ModelConfig)
        """
        # Decision matrix
        if privacy_required:
            # Must use local
            if task_complexity == "high":
                return ModelRole.QUEEN_REASONING, OLLAMA_MODELS[ModelRole.QUEEN_REASONING]
            elif task_complexity == "medium":
                return ModelRole.WORKER_DEEP, OLLAMA_MODELS[ModelRole.WORKER_DEEP]
            else:
                return ModelRole.WORKER_FAST, OLLAMA_MODELS[ModelRole.WORKER_FAST]
        
        # Can use cloud - optimize for speed/cost
        if not self.cloud_available:
            # Fall back to local
            if task_complexity == "high":
                return ModelRole.QUEEN_REASONING, OLLAMA_MODELS[ModelRole.QUEEN_REASONING]
            else:
                return ModelRole.WORKER_FAST, OLLAMA_MODELS[ModelRole.WORKER_FAST]
        
        # Use cloud for speed
        if latency_sensitivity == "high":
            return ModelRole.WORKER_FAST, LANGCHAIN_MODELS[ModelRole.WORKER_FAST]
        
        if cost_sensitive and task_complexity == "low":
            return ModelRole.WORKER_FAST, LANGCHAIN_MODELS[ModelRole.WORKER_FAST]
        
        if task_complexity == "high":
            return ModelRole.QUEEN_REASONING, LANGCHAIN_MODELS[ModelRole.QUEEN_REASONING]
        
        return ModelRole.WORKER_DEEP, LANGCHAIN_MODELS[ModelRole.WORKER_DEEP]
    
    def get_chat_model(self, role: ModelRole, force_backend: Optional[BackendType] = None):
        """
        Get an initialized chat model for the specified role.
        
        Returns either:
        - beeai_framework.backend.ChatModel (for Ollama)
        - langchain_core.language_models.ChatOpenAI/ChatAnthropic (for LangChain)
        """
        config = self.get_config(role, force_backend)
        
        if config.backend == BackendType.OLLAMA:
            from beeai_framework.backend import ChatModel
            return ChatModel.from_name(f"ollama:{config.name}"), config
        
        elif config.backend == BackendType.LANGCHAIN:
            # Import here to avoid dependency if not using
            try:
                if "claude" in config.name:
                    from langchain_anthropic import ChatAnthropic
                    return ChatAnthropic(
                        model=config.name,
                        temperature=config.temperature,
                        timeout=config.timeout,
                        api_key=self.anthropic_api_key,
                    ), config
                else:
                    from langchain_openai import ChatOpenAI
                    return ChatOpenAI(
                        model=config.name,
                        temperature=config.temperature,
                        timeout=config.timeout,
                        api_key=self.openai_api_key,
                    ), config
            except ImportError as e:
                print(f"[LLMRouter] LangChain not installed: {e}")
                print("[LLMRouter] Falling back to Ollama...")
                return self.get_chat_model(role, BackendType.OLLAMA)
        
        else:
            raise ValueError(f"Unknown backend: {config.backend}")


# ============================================================================
# GLOBAL ROUTER INSTANCE
# ============================================================================

# Default to Ollama (local), can be overridden via env vars
default_backend = BackendType.OLLAMA
if os.getenv("HIVE_USE_CLOUD", "").lower() in ("true", "1", "yes"):
    default_backend = BackendType.LANGCHAIN

router = LLMRouter(default_backend=default_backend)


def get_model_for_agent(agent_type: str, specialization: Optional[str] = None) -> tuple[Any, ModelConfig]:
    """
    Convenience function to get the right model for an agent.
    
    Args:
        agent_type: "queen", "worker", "drone", "forager", "mantis"
        specialization: e.g., "reasoning", "fast", "deep"
    
    Returns:
        Tuple of (model_instance, config)
    """
    if agent_type == "queen":
        if specialization == "reasoning":
            return router.get_chat_model(ModelRole.QUEEN_REASONING)
        return router.get_chat_model(ModelRole.QUEEN_PRIMARY)
    
    elif agent_type in ("worker", "drone", "forager"):
        if specialization == "deep":
            return router.get_chat_model(ModelRole.WORKER_DEEP)
        return router.get_chat_model(ModelRole.WORKER_FAST)
    
    elif agent_type == "mantis":
        return router.get_chat_model(ModelRole.WORKER_FAST)
    
    else:
        return router.get_chat_model(ModelRole.WORKER_FAST)


if __name__ == "__main__":
    # Test the router
    print("=== LLM Router Test ===\n")
    
    print("Available Models:")
    print("\nLOCAL (Ollama):")
    for role, config in OLLAMA_MODELS.items():
        print(f"  {role.value:<20} → {config.name}")
    
    print("\nCLOUD (LangChain):")
    for role, config in LANGCHAIN_MODELS.items():
        print(f"  {role.value:<20} → {config.name}")
    
    print(f"\nDefault Backend: {router.default_backend.value}")
    print(f"Cloud Available: {router.cloud_available}")
    
    # Test routing
    print("\n=== Task Routing Examples ===")
    
    scenarios = [
        ("high", True, "low", True),    # Private, complex
        ("low", False, "high", False),  # Cloud, fast
        ("medium", False, "medium", True),  # Cloud, cost-sensitive
    ]
    
    for complexity, privacy, latency, cost in scenarios:
        role, config = router.route_task(complexity, privacy, latency, cost)
        print(f"\nTask: complexity={complexity}, privacy={privacy}, latency={latency}")
        print(f"  → Routed to: {role.value} ({config.backend.value})")
