"""
Backend Configuration Manager

Manages switching between BeeAI (local) and LangChain (cloud) backends.
Provides runtime configuration and environment variable management.
"""

import os
import json
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict


CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    "..", "config", "backend_config.json"
)


class AgentBackend(Enum):
    """Backend choice for agents."""
    BEEAI_LOCAL = "beeai_local"      # Ollama + BeeAI Framework
    LANGCHAIN_CLOUD = "langchain_cloud"  # LangChain + APIs
    HYBRID = "hybrid"                # Queen: BeeAI, Workers: LangChain


@dataclass
class BackendConfig:
    """Configuration for the LLM backend."""
    
    # Backend selection
    agent_backend: str = "beeai_local"
    
    # Queen Bee model selection
    queen_use_reasoning: bool = False  # Use marco-o1/Claude-3 instead of granite3.3/GPT-4
    
    # Worker/Drone/Forager model
    worker_use_cloud: bool = False  # Use GPT-3.5 instead of llama3.1
    
    # Cloud API keys (loaded from env by default)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    langsmith_api_key: Optional[str] = None
    
    # LangSmith settings
    langsmith_project: str = "beeai-hive-999"
    langsmith_tracing: bool = True
    
    # Performance settings
    request_timeout: float = 30.0
    max_retries: int = 3
    
    def __post_init__(self):
        """Load API keys from environment if not set."""
        if self.openai_api_key is None:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.anthropic_api_key is None:
            self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.langsmith_api_key is None:
            self.langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
    
    def is_cloud_available(self) -> bool:
        """Check if cloud APIs are configured."""
        return bool(self.openai_api_key or self.anthropic_api_key)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excluding sensitive keys)."""
        data = asdict(self)
        # Mask API keys
        if data.get('openai_api_key'):
            data['openai_api_key'] = '***' + data['openai_api_key'][-4:]
        if data.get('anthropic_api_key'):
            data['anthropic_api_key'] = '***' + data['anthropic_api_key'][-4:]
        if data.get('langsmith_api_key'):
            data['langsmith_api_key'] = '***' + data['langsmith_api_key'][-4:]
        return data
    
    def save(self):
        """Save configuration to file."""
        # Don't save API keys to file
        data = {
            "agent_backend": self.agent_backend,
            "queen_use_reasoning": self.queen_use_reasoning,
            "worker_use_cloud": self.worker_use_cloud,
            "langsmith_project": self.langsmith_project,
            "langsmith_tracing": self.langsmith_tracing,
            "request_timeout": self.request_timeout,
            "max_retries": self.max_retries,
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls) -> "BackendConfig":
        """Load configuration from file."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
            return cls(**data)
        return cls()  # Return defaults
    
    def apply_env(self):
        """Apply configuration to environment variables."""
        if self.agent_backend == "langchain_cloud":
            os.environ["HIVE_USE_CLOUD"] = "true"
        else:
            os.environ["HIVE_USE_CLOUD"] = "false"


# Global config instance
_config: Optional[BackendConfig] = None


def get_config() -> BackendConfig:
    """Get the global configuration."""
    global _config
    if _config is None:
        _config = BackendConfig.load()
    return _config


def set_config(config: BackendConfig):
    """Set the global configuration."""
    global _config
    _config = config
    config.apply_env()


def switch_backend(backend: AgentBackend):
    """
    Switch the active backend at runtime.
    
    Args:
        backend: The backend to switch to
    """
    config = get_config()
    config.agent_backend = backend.value
    config.apply_env()
    config.save()
    
    # Force reimport of router
    import backend.llm_router as router_module
    router_module.router.default_backend = (
        router_module.BackendType.LANGCHAIN 
        if backend == AgentBackend.LANGCHAIN_CLOUD 
        else router_module.BackendType.OLLAMA
    )


def print_status():
    """Print current backend status."""
    config = get_config()
    
    print("=" * 50)
    print("HIVE 999 BACKEND STATUS")
    print("=" * 50)
    print(f"\nActive Backend: {config.agent_backend}")
    print(f"Cloud Available: {config.is_cloud_available()}")
    print(f"Queen Reasoning: {'marco-o1/Claude-3' if config.queen_use_reasoning else 'granite3.3/GPT-4'}")
    print(f"Workers: {'GPT-3.5 (cloud)' if config.worker_use_cloud else 'llama3.1 (local)'}")
    print(f"\nLangSmith:")
    print(f"  Project: {config.langsmith_project}")
    print(f"  Tracing: {config.langsmith_tracing}")
    print("=" * 50)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            print_status()
        
        elif command == "switch":
            if len(sys.argv) > 2:
                backend_name = sys.argv[2]
                try:
                    backend = AgentBackend(backend_name)
                    switch_backend(backend)
                    print(f"Switched to {backend.value}")
                except ValueError:
                    print(f"Unknown backend: {backend_name}")
                    print(f"Options: {', '.join(b.value for b in AgentBackend)}")
            else:
                print("Usage: python config_manager.py switch <backend>")
                print(f"Options: {', '.join(b.value for b in AgentBackend)}")
        
        elif command == "config":
            config = get_config()
            print(json.dumps(config.to_dict(), indent=2))
    
    else:
        print_status()
        print("\nCommands:")
        print("  python config_manager.py status")
        print("  python config_manager.py switch <beeai_local|langchain_cloud|hybrid>")
        print("  python config_manager.py config")
