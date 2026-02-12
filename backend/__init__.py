"""BeeAI Hive 999 - Hybrid LLM Backend

Supports both local (Ollama) and cloud (LangChain/LangSmith) backends
with configurable routing for optimal performance.
"""

from .llm_router import (
    LLMRouter,
    BackendType,
    ModelRole,
    ModelConfig,
    router,
    get_model_for_agent,
    OLLAMA_MODELS,
    LANGCHAIN_MODELS,
)

__all__ = [
    "LLMRouter",
    "BackendType", 
    "ModelRole",
    "ModelConfig",
    "router",
    "get_model_for_agent",
    "OLLAMA_MODELS",
    "LANGCHAIN_MODELS",
]
