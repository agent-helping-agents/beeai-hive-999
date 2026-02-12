"""
BeeAI Hive 999 - Comprehensive Configuration System

Provides:
- YAML-based configuration with environment overrides
- Settings UI within TUI
- Profile management
- Validation and defaults
"""

import os
import json
import yaml
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
from enum import Enum
from pathlib import Path


class BackendType(Enum):
    LOCAL = "local"
    CLOUD = "cloud"
    HYBRID = "hybrid"


class Theme(Enum):
    HONEY = "honey"
    DARK = "dark"
    LIGHT = "light"
    MATRIX = "matrix"


@dataclass
class ModelConfig:
    """Configuration for a specific model."""

    name: str
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: float = 60.0
    enabled: bool = True


@dataclass
class OllamaConfig:
    """Ollama-specific configuration."""

    host: str = "http://localhost:11434"
    models: Dict[str, ModelConfig] = field(default_factory=dict)
    keep_alive: int = 5

    def __post_init__(self):
        if not self.models:
            self.models = {
                "granite3.3:8b": ModelConfig("granite3.3:8b", 0.7, 4096, 60.0),
                "marco-o1:latest": ModelConfig("marco-o1:latest", 0.8, 8192, 120.0),
                "deepseek-r1:8b": ModelConfig("deepseek-r1:8b", 0.7, 8192, 90.0),
                "llama3.1:8b": ModelConfig("llama3.1:8b", 0.6, 4096, 30.0),
                "llama3.2:3b": ModelConfig("llama3.2:3b", 0.6, 2048, 20.0),
                "qwen2.5-coder:32b": ModelConfig("qwen2.5-coder:32b", 0.2, 4096, 90.0),
                "deepseek-coder-v2:16b": ModelConfig(
                    "deepseek-coder-v2:16b-instruct", 0.3, 4096, 90.0
                ),
                "codellama:34b": ModelConfig("codellama:34b", 0.4, 4096, 60.0),
                "nomic-embed-text": ModelConfig("nomic-embed-text", 0.0, 8192, 30.0),
            }


@dataclass
class CloudConfig:
    """Cloud (LangChain) configuration."""

    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    langsmith_api_key: Optional[str] = None
    langsmith_project: str = "beeai-hive-999"
    tracing_enabled: bool = True

    def is_configured(self) -> bool:
        return bool(self.openai_api_key or self.anthropic_api_key)


@dataclass
class AgentDefaults:
    """Default configurations for agents."""

    queen_model: str = "granite3.3:8b"
    queen_reasoning_model: str = "marco-o1:latest"
    worker_model: str = "llama3.1:8b"
    drone_model: str = "llama3.1:8b"
    forager_model: str = "llama3.1:8b"
    coding_model: str = "qwen2.5-coder:32b"
    embedding_model: str = "nomic-embed-text"
    max_history: int = 1000
    system_prompt: str = "beeai"


@dataclass
class UISettings:
    """TUI appearance and behavior settings."""

    theme: str = "honey"
    color_scheme: str = "digital_root_9"
    show_timestamps: bool = True
    show_scrollbar: bool = True
    show_typing_indicator: bool = True
    animation_speed: str = "normal"
    font_size: str = "normal"
    sidebar_width: int = 22
    context_panel: bool = True
    auto_scroll: bool = True
    syntax_highlighting: bool = True
    ansi_art_support: bool = True


@dataclass
class NotificationSettings:
    """Notification preferences."""

    enabled: bool = True
    duration: float = 3.0
    sounds: bool = False
    desktop: bool = False
    show_system: bool = True
    show_errors: bool = True
    show_success: bool = True


@dataclass
class HiveConfig:
    """Main configuration for BeeAI Hive 999."""

    version: str = "1.0.0"

    backend: str = "local"
    environment: str = "development"

    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    cloud: CloudConfig = field(default_factory=CloudConfig)
    agents: AgentDefaults = field(default_factory=AgentDefaults)
    ui: UISettings = field(default_factory=UISettings)
    notifications: NotificationSettings = field(default_factory=NotificationSettings)

    matrix: Dict[str, Any] = field(
        default_factory=lambda: {"dimensions": 9, "total_nodes": 729, "digital_root": 9}
    )

    def __post_init__(self):
        self._load_env_overrides()

    def _load_env_overrides(self):
        """Load configuration from environment variables."""
        env_mappings = {
            "HIVE_BACKEND": ("backend", str),
            "HIVE_ENVIRONMENT": ("environment", str),
            "OLLAMA_HOST": ("ollama.host", str),
            "OPENAI_API_KEY": ("cloud.openai_api_key", str),
            "ANTHROPIC_API_KEY": ("cloud.anthropic_api_key", str),
            "LANGSMITH_API_KEY": ("cloud.langsmith_api_key", str),
            "HIVE_THEME": ("ui.theme", str),
            "HIVE_SHOW_TIMESTAMPS": ("ui.show_timestamps", bool),
            "HIVE_SYNTAX_HIGHLIGHT": ("ui.syntax_highlighting", bool),
        }

        for env_key, (path, type_func) in env_mappings.items():
            value = os.getenv(env_key)
            if value is not None:
                if type_func == bool:
                    value = value.lower() in ("true", "1", "yes")
                self._set_nested(path, value)

    def _set_nested(self, path: str, value: Any):
        """Set a nested configuration value."""
        parts = path.split(".")
        obj = self
        for part in parts[:-1]:
            obj = getattr(obj, part)
        setattr(obj, parts[-1], value)

    def get_nested(self, path: str, default: Any = None) -> Any:
        """Get a nested configuration value."""
        parts = path.split(".")
        obj = self
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return default
        return obj

    def is_cloud_available(self) -> bool:
        """Check if cloud backend is configured."""
        return self.cloud.is_configured()

    def get_current_model(self, agent_type: str) -> str:
        """Get the current model for an agent type."""
        models = {
            "queen": self.agents.queen_model,
            "queen_reasoning": self.agents.queen_reasoning_model,
            "worker": self.agents.worker_model,
            "drone": self.agents.drone_model,
            "forager": self.agents.forager_model,
            "coding": self.agents.coding_model,
            "embedding": self.agents.embedding_model,
        }
        return models.get(agent_type, self.agents.worker_model)

    def to_dict(self, mask_secrets: bool = True) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        data = asdict(self)

        if mask_secrets:
            if data.get("cloud", {}).get("openai_api_key"):
                data["cloud"]["openai_api_key"] = (
                    "***" + data["cloud"]["openai_api_key"][-4:]
                )
            if data.get("cloud", {}).get("anthropic_api_key"):
                data["cloud"]["anthropic_api_key"] = (
                    "***" + data["cloud"]["anthropic_api_key"][-4:]
                )
            if data.get("cloud", {}).get("langsmith_api_key"):
                data["cloud"]["langsmith_api_key"] = (
                    "***" + data["cloud"]["langsmith_api_key"][-4:]
                )

        return data

    def save(self, path: Optional[str] = None):
        """Save configuration to file."""
        config_path = Path(path or self.get_config_path())
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            yaml.dump(
                self.to_dict(mask_secrets=True), f, default_flow_style=False, indent=2
            )

    def get_config_path(self) -> str:
        """Get the configuration file path."""
        return os.environ.get(
            "HIVE_CONFIG_PATH",
            os.path.join(os.path.dirname(__file__), "hive_config.yaml"),
        )

    @classmethod
    def load(cls, path: Optional[str] = None) -> "HiveConfig":
        """Load configuration from file."""
        config_path = Path(
            path
            or os.environ.get(
                "HIVE_CONFIG_PATH",
                os.path.join(os.path.dirname(__file__), "hive_config.yaml"),
            )
        )

        if config_path.exists():
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)
                if data:
                    return cls(**data)

        return cls()


GLOBAL_CONFIG = HiveConfig.load()


def get_config() -> HiveConfig:
    """Get the global configuration."""
    return GLOBAL_CONFIG


def save_config():
    """Save the global configuration."""
    GLOBAL_CONFIG.save()


def reload_config():
    """Reload configuration from file."""
    global GLOBAL_CONFIG
    GLOBAL_CONFIG = HiveConfig.load()


class ConfigProfile(Enum):
    """Predefined configuration profiles."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    MINIMAL = "minimal"
    CODING = "coding"


def apply_profile(profile: ConfigProfile):
    """Apply a predefined configuration profile."""
    profiles = {
        ConfigProfile.DEVELOPMENT: {
            "backend": "local",
            "ui.theme": "honey",
            "ui.syntax_highlighting": True,
            "ui.ansi_art_support": True,
        },
        ConfigProfile.PRODUCTION: {
            "backend": "cloud",
            "ui.theme": "dark",
            "ui.syntax_highlighting": True,
            "ui.ansi_art_support": False,
        },
        ConfigProfile.MINIMAL: {
            "backend": "local",
            "ui.theme": "dark",
            "ui.show_timestamps": False,
            "ui.show_typing_indicator": False,
            "ui.context_panel": False,
        },
        ConfigProfile.CODING: {
            "backend": "local",
            "ui.theme": "matrix",
            "ui.syntax_highlighting": True,
            "ui.ansi_art_support": True,
            "agents.coding_model": "qwen2.5-coder:32b",
        },
    }

    settings = profiles.get(profile, {})
    for path, value in settings.items():
        GLOBAL_CONFIG._set_nested(path, value)

    save_config()
    return f"Applied {profile.value} profile"


if __name__ == "__main__":
    import sys

    config = get_config()

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "show":
            print(json.dumps(config.to_dict(), indent=2))

        elif cmd == "save":
            config.save()
            print("Configuration saved.")

        elif cmd == "reload":
            reload_config()
            print("Configuration reloaded.")

        elif cmd == "profile":
            if len(sys.argv) > 2:
                profile_name = sys.argv[2].upper()
                try:
                    profile = ConfigProfile[profile_name]
                    print(apply_profile(profile))
                except KeyError:
                    print(f"Unknown profile: {profile_name}")
                    print(f"Available: {[p.name for p in ConfigProfile]}")
            else:
                print("Usage: python hive_config.py profile <name>")

        elif cmd == "check":
            print("Configuration Check:")
            print(f"  Backend: {config.backend}")
            print(f"  Cloud Available: {config.is_cloud_available()}")
            print(f"  Theme: {config.ui.theme}")
            print(f"  Coding Model: {config.agents.coding_model}")
            print(f"  Ollama Host: {config.ollama.host}")

    else:
        print("BeeAI Hive 999 Configuration")
        print("=" * 40)
        print(f"Backend: {config.backend}")
        print(f"Environment: {config.environment}")
        print(f"Theme: {config.ui.theme}")
        print(f"Coding Model: {config.agents.coding_model}")
        print(f"Ollama Host: {config.ollama.host}")
        print(f"Cloud Available: {config.is_cloud_available()}")
        print("\nCommands:")
        print("  python hive_config.py show      - Show full config")
        print("  python hive_config.py save      - Save config")
        print("  python hive_config.py reload    - Reload from file")
        print("  python hive_config.py profile <name> - Apply profile")
