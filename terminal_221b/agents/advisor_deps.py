"""
AdvisorDeps - Configuration and Dependency Injection for Terminal 221b

Implements the configuration nucleus for Solana AI agents with:
- Secure credential management
- Multi-environment support (simulation/devnet/testnet/mainnet)
- Human-in-the-loop safety controls
- Fallback endpoint management

The "Advisor" pattern ensures AI recommendations require explicit approval
before high-value transaction execution - critical for financial safety.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from enum import Enum


class NetworkEnvironment(Enum):
    """Solana network environments."""
    SIMULATION = "simulation"  # Local validator via SimServer
    DEVNET = "devnet"          # https://api.devnet.solana.com
    TESTNET = "testnet"        # https://api.testnet.solana.com
    MAINNET = "mainnet"        # https://api.mainnet-beta.solana.com


class SafetyLevel(Enum):
    """Human-in-the-loop safety levels."""
    FULLY_AUTONOMOUS = "autonomous"      # No human approval required
    NOTIFY_ONLY = "notify"               # Inform but proceed
    APPROVE_MODERATE = "moderate"        # Approve transactions > threshold
    APPROVE_ALL = "strict"               # Approve all transactions


@dataclass
class AdvisorDeps:
    """
    Dependency injection container for Terminal 221b agents.
    
    Centralizes configuration to ensure consistency across agent instances
    and enables test-time mocking for SimServer operation.
    
    Attributes:
        solana_rpc_url: Primary Solana RPC endpoint
        solana_fallback_urls: Backup RPC endpoints for failover
        ethereum_provider_url: Ethereum RPC endpoint for ethers integration
        openai_api_key: OpenAI API key for LLM operations
        anthropic_api_key: Anthropic API key (optional)
        langsmith_api_key: LangSmith tracing key (optional)
        wallet_private_key: Solana wallet private key (encrypted storage recommended)
        wallet_public_key: Solana wallet public key
        environment: Target network environment
        safety_level: Human approval requirements
        auto_approve_threshold_lamports: Auto-approve transactions below this value
        simulation_mode: Route all calls through SimServer when True
        jito_enabled: Enable Jito MEV bundle submission
        priority_fee_micro_lamports: Default priority fee for transactions
    """
    
    # Solana Configuration
    solana_rpc_url: str = "https://api.devnet.solana.com"
    solana_fallback_urls: List[str] = field(default_factory=list)
    
    # Ethereum Configuration (for multi-chain support)
    ethereum_provider_url: Optional[str] = None
    ethereum_wallet_key: Optional[str] = None
    
    # LLM Provider Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    langsmith_api_key: Optional[str] = None
    
    # Wallet Configuration
    wallet_private_key: Optional[str] = None  # Use keyring/HSM in production!
    wallet_public_key: Optional[str] = None
    
    # Environment & Safety
    environment: NetworkEnvironment = NetworkEnvironment.DEVNET
    safety_level: SafetyLevel = SafetyLevel.APPROVE_MODERATE
    auto_approve_threshold_lamports: int = 100_000_000  # 0.1 SOL default
    
    # Operational Mode
    simulation_mode: bool = True  # Default to safe simulation
    sim_server_port: int = 8899
    
    # MEV & Transaction Optimization
    jito_enabled: bool = False
    jito_block_engine_url: str = "https://mainnet.block-engine.jito.wtf"
    priority_fee_micro_lamports: int = 10_000  # 0.00001 SOL
    
    # Agent Personality
    detective_personality: str = "holmes"  # holmes, watson, mycroft, irene
    enable_reasoning_traces: bool = True
    
    # Caching & Performance
    redis_url: Optional[str] = None
    enable_caching: bool = True
    
    def __post_init__(self):
        """Validate configuration and set defaults."""
        # Load from environment if not provided
        self.openai_api_key = self.openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = self.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.langsmith_api_key = self.langsmith_api_key or os.getenv("LANGSMITH_API_KEY")
        self.wallet_private_key = self.wallet_private_key or os.getenv("SOLANA_PRIVATE_KEY")
        self.wallet_public_key = self.wallet_public_key or os.getenv("SOLANA_PUBLIC_KEY")
        
        # Set environment-specific defaults
        if self.environment == NetworkEnvironment.SIMULATION:
            self.solana_rpc_url = f"http://localhost:{self.sim_server_port}"
            self.simulation_mode = True
        elif self.environment == NetworkEnvironment.DEVNET:
            self.solana_rpc_url = "https://api.devnet.solana.com"
            self.solana_fallback_urls = [
                "https://devnet.helius-rpc.com/?api-key=...",
                "https://rpc.ankr.com/solana_devnet",
            ]
        elif self.environment == NetworkEnvironment.MAINNET:
            self.solana_rpc_url = "https://api.mainnet-beta.solana.com"
            self.simulation_mode = False  # Force explicit override
            
        # Validate safety constraints
        if self.environment == NetworkEnvironment.MAINNET:
            assert not self.simulation_mode, "Cannot use simulation mode on mainnet"
            if self.safety_level == SafetyLevel.FULLY_AUTONOMOUS:
                print("⚠️  WARNING: Fully autonomous mode on mainnet. Ensure this is intentional.")
    
    def requires_approval(self, amount_lamports: int) -> bool:
        """
        Determine if a transaction requires human approval.
        
        Args:
            amount_lamports: Transaction amount in lamports
            
        Returns:
            True if approval is required
        """
        if self.safety_level == SafetyLevel.FULLY_AUTONOMOUS:
            return False
        elif self.safety_level == SafetyLevel.APPROVE_ALL:
            return True
        elif self.safety_level == SafetyLevel.APPROVE_MODERATE:
            return amount_lamports > self.auto_approve_threshold_lamports
        return False
    
    def get_effective_rpc_url(self) -> str:
        """Get the appropriate RPC URL for current environment."""
        if self.simulation_mode:
            return f"http://localhost:{self.sim_server_port}"
        return self.solana_rpc_url
    
    def to_safe_dict(self) -> Dict[str, Any]:
        """
        Export configuration with secrets masked.
        Useful for logging and debugging.
        """
        return {
            "environment": self.environment.value,
            "rpc_url": self.solana_rpc_url,
            "simulation_mode": self.simulation_mode,
            "safety_level": self.safety_level.value,
            "auto_approve_threshold_sol": self.auto_approve_threshold_lamports / 1e9,
            "wallet_public_key": self.wallet_public_key[:10] + "..." if self.wallet_public_key else None,
            "jito_enabled": self.jito_enabled,
            "priority_fee_sol": self.priority_fee_micro_lamports / 1e6,
            "has_openai": bool(self.openai_api_key),
            "has_anthropic": bool(self.anthropic_api_key),
        }
    
    @classmethod
    def from_env(cls) -> "AdvisorDeps":
        """Create configuration from environment variables."""
        env_map = {
            "simulation": NetworkEnvironment.SIMULATION,
            "devnet": NetworkEnvironment.DEVNET,
            "testnet": NetworkEnvironment.TESTNET,
            "mainnet": NetworkEnvironment.MAINNET,
        }
        
        safety_map = {
            "autonomous": SafetyLevel.FULLY_AUTONOMOUS,
            "notify": SafetyLevel.NOTIFY_ONLY,
            "moderate": SafetyLevel.APPROVE_MODERATE,
            "strict": SafetyLevel.APPROVE_ALL,
        }
        
        return cls(
            environment=env_map.get(
                os.getenv("TERMINAL_221B_ENV", "devnet").lower(),
                NetworkEnvironment.DEVNET
            ),
            safety_level=safety_map.get(
                os.getenv("TERMINAL_221B_SAFETY", "moderate").lower(),
                SafetyLevel.APPROVE_MODERATE
            ),
            simulation_mode=os.getenv("TERMINAL_221B_SIMULATION", "false").lower() == "true",
            detective_personality=os.getenv("TERMINAL_221B_PERSONALITY", "holmes"),
        )


# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

def get_simulation_config() -> AdvisorDeps:
    """Get safe simulation configuration for development."""
    return AdvisorDeps(
        environment=NetworkEnvironment.SIMULATION,
        simulation_mode=True,
        safety_level=SafetyLevel.FULLY_AUTONOMOUS,  # Safe in simulation
        enable_reasoning_traces=True,
    )


def get_devnet_config() -> AdvisorDeps:
    """Get devnet configuration for testing."""
    return AdvisorDeps(
        environment=NetworkEnvironment.DEVNET,
        simulation_mode=False,
        safety_level=SafetyLevel.APPROVE_MODERATE,
        auto_approve_threshold_lamports=100_000_000,  # 0.1 SOL
    )


def get_mainnet_config(
    wallet_key: str,
    safety_level: SafetyLevel = SafetyLevel.APPROVE_ALL
) -> AdvisorDeps:
    """
    Get mainnet configuration with strict safety defaults.
    
    Args:
        wallet_key: Solana wallet private key (handle securely!)
        safety_level: Override default strict safety
    """
    return AdvisorDeps(
        environment=NetworkEnvironment.MAINNET,
        simulation_mode=False,
        safety_level=safety_level,
        wallet_private_key=wallet_key,
        jito_enabled=True,  # Enable MEV protection on mainnet
        priority_fee_micro_lamports=50_000,  # Higher priority for mainnet
    )
