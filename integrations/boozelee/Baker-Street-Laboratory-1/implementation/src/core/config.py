"""
Baker Street Laboratory - Configuration Management
Handles loading and managing configuration from YAML files and environment variables.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class AgentConfig:
    """Configuration for a single agent."""
    name: str
    type: str
    model: str
    temperature: float = 0.3
    max_tokens: int = 2000
    role: str = ""
    capabilities: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)


@dataclass
class APISettings:
    """API configuration settings."""
    openai_api_base: str = "https://api.openai.com/v1"
    rate_limit: int = 60
    timeout: int = 30


@dataclass
class PipelineSettings:
    """Pipeline configuration settings."""
    max_iterations: int = 5
    convergence_threshold: float = 0.95
    output_format: str = "markdown"
    save_intermediate: bool = True


@dataclass
class PrivacySettings:
    """Privacy and security settings."""
    anonymize_data: bool = True
    encrypt_sensitive: bool = True
    audit_trail: bool = True


@dataclass
class OutputSettings:
    """Output configuration settings."""
    research_dir: str = "research"
    implementation_dir: str = "implementation"
    optimization_dir: str = "optimization"
    log_level: str = "INFO"


@dataclass
class GlobalConfig:
    """Global configuration settings."""
    api_settings: APISettings = field(default_factory=APISettings)
    pipeline_settings: PipelineSettings = field(default_factory=PipelineSettings)
    privacy: PrivacySettings = field(default_factory=PrivacySettings)
    output: OutputSettings = field(default_factory=OutputSettings)


@dataclass
class ToolConfig:
    """Configuration for external tools and APIs."""
    name: str
    type: str = ""
    api_key_env: str = ""
    base_url: str = ""
    config: Dict[str, Any] = field(default_factory=dict)


class Config:
    """Main configuration class for Baker Street Laboratory."""
    
    def __init__(self):
        self.agents: Dict[str, AgentConfig] = {}
        self.global_config: GlobalConfig = GlobalConfig()
        self.tools: Dict[str, ToolConfig] = {}
        self._env_loaded = False
        
    @classmethod
    def from_file(cls, config_path: str) -> 'Config':
        """Load configuration from a YAML file."""
        config = cls()
        config.load_from_file(config_path)
        return config
    
    def load_from_file(self, config_path: str) -> None:
        """Load configuration from a YAML file."""
        # Load environment variables first
        if not self._env_loaded:
            load_dotenv()
            self._env_loaded = True
        
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
        
        # Load agents
        if 'agents' in data:
            for agent_name, agent_data in data['agents'].items():
                self.agents[agent_name] = AgentConfig(
                    name=agent_name,
                    type=agent_data.get('type', ''),
                    model=agent_data.get('model', 'gpt-3.5-turbo'),
                    temperature=agent_data.get('temperature', 0.3),
                    max_tokens=agent_data.get('max_tokens', 2000),
                    role=agent_data.get('role', ''),
                    capabilities=agent_data.get('capabilities', []),
                    tools=agent_data.get('tools', [])
                )
        
        # Load global configuration
        if 'global_config' in data:
            global_data = data['global_config']
            
            # API settings
            if 'api_settings' in global_data:
                api_data = global_data['api_settings']
                self.global_config.api_settings = APISettings(
                    openai_api_base=api_data.get('openai_api_base', 'https://api.openai.com/v1'),
                    rate_limit=api_data.get('rate_limit', 60),
                    timeout=api_data.get('timeout', 30)
                )
            
            # Pipeline settings
            if 'pipeline_settings' in global_data:
                pipeline_data = global_data['pipeline_settings']
                self.global_config.pipeline_settings = PipelineSettings(
                    max_iterations=pipeline_data.get('max_iterations', 5),
                    convergence_threshold=pipeline_data.get('convergence_threshold', 0.95),
                    output_format=pipeline_data.get('output_format', 'markdown'),
                    save_intermediate=pipeline_data.get('save_intermediate', True)
                )
            
            # Privacy settings
            if 'privacy' in global_data:
                privacy_data = global_data['privacy']
                self.global_config.privacy = PrivacySettings(
                    anonymize_data=privacy_data.get('anonymize_data', True),
                    encrypt_sensitive=privacy_data.get('encrypt_sensitive', True),
                    audit_trail=privacy_data.get('audit_trail', True)
                )
            
            # Output settings
            if 'output' in global_data:
                output_data = global_data['output']
                self.global_config.output = OutputSettings(
                    research_dir=output_data.get('research_dir', 'research'),
                    implementation_dir=output_data.get('implementation_dir', 'implementation'),
                    optimization_dir=output_data.get('optimization_dir', 'optimization'),
                    log_level=output_data.get('log_level', 'INFO')
                )
        
        # Load tools
        if 'tools' in data:
            for tool_category, tools_list in data['tools'].items():
                if isinstance(tools_list, list):
                    for tool_data in tools_list:
                        tool_name = tool_data.get('name', '')
                        if tool_name:
                            self.tools[tool_name] = ToolConfig(
                                name=tool_name,
                                type=tool_category,
                                api_key_env=tool_data.get('api_key_env', ''),
                                base_url=tool_data.get('base_url', ''),
                                config=tool_data
                            )
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent."""
        return self.agents.get(agent_name)
    
    def get_tool_config(self, tool_name: str) -> Optional[ToolConfig]:
        """Get configuration for a specific tool."""
        return self.tools.get(tool_name)
    
    def get_api_key(self, env_var_name: str) -> Optional[str]:
        """Get API key from environment variables."""
        return os.getenv(env_var_name)
    
    def list_agents(self) -> List[str]:
        """Get list of configured agent names."""
        return list(self.agents.keys())
    
    def list_tools(self) -> List[str]:
        """Get list of configured tool names."""
        return list(self.tools.keys())
    
    def validate(self) -> Dict[str, Any]:
        """Validate the configuration and return status."""
        issues = []
        warnings = []
        
        # Check if we have at least one agent
        if not self.agents:
            issues.append("No agents configured")
        
        # Check for required API keys
        required_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
        missing_keys = []
        
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
        
        if len(missing_keys) == len(required_keys):
            issues.append("No AI API keys found in environment")
        elif missing_keys:
            warnings.append(f"Missing API keys: {', '.join(missing_keys)}")
        
        # Check tool configurations
        for tool_name, tool_config in self.tools.items():
            if tool_config.api_key_env and not os.getenv(tool_config.api_key_env):
                warnings.append(f"API key not found for tool '{tool_name}': {tool_config.api_key_env}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'agents': {name: {
                'type': agent.type,
                'model': agent.model,
                'temperature': agent.temperature,
                'max_tokens': agent.max_tokens,
                'role': agent.role,
                'capabilities': agent.capabilities,
                'tools': agent.tools
            } for name, agent in self.agents.items()},
            'global_config': {
                'api_settings': {
                    'openai_api_base': self.global_config.api_settings.openai_api_base,
                    'rate_limit': self.global_config.api_settings.rate_limit,
                    'timeout': self.global_config.api_settings.timeout
                },
                'pipeline_settings': {
                    'max_iterations': self.global_config.pipeline_settings.max_iterations,
                    'convergence_threshold': self.global_config.pipeline_settings.convergence_threshold,
                    'output_format': self.global_config.pipeline_settings.output_format,
                    'save_intermediate': self.global_config.pipeline_settings.save_intermediate
                }
            },
            'tools': {name: tool.config for name, tool in self.tools.items()}
        }
