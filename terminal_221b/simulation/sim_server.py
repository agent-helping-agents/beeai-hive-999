"""
SimServer - Local Solana Validator Simulation for Safe Agent Testing

Provides isolated Solana ledger simulation enabling:
- Transaction preflight validation without mainnet exposure
- Program behavior testing with controlled initial state
- Agent policy verification in sandboxed environment
- Historical state replay for backtesting

Implementation Options:
1. Full local validator via solana-test-validator
2. Lightweight RPC simulation via simulateTransaction
3. Historical state replay for strategy backtesting

"The detective must verify his deductions before presenting them."
"""

import subprocess
import time
import json
import asyncio
from dataclasses import dataclass
from typing import Optional, Dict, List, Any, Tuple
from pathlib import Path
import aiohttp


@dataclass
class SimulationResult:
    """Result of a transaction simulation."""

    success: bool
    signature: Optional[str]  # Simulated signature
    slot: Optional[int]
    compute_units_consumed: int
    accounts_changed: List[Dict[str, Any]]
    logs: List[str]
    error: Optional[str] = None
    error_code: Optional[int] = None

    # Financial impact (simulated)
    balance_changes: Dict[str, float] = None  # account -> SOL change
    token_changes: Dict[str, Dict[str, float]] = None  # account -> {mint: amount}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "success": self.success,
            "signature": self.signature,
            "slot": self.slot,
            "compute_units_consumed": self.compute_units_consumed,
            "accounts_changed": len(self.accounts_changed),
            "logs": self.logs[-10:] if self.logs else [],  # Last 10 logs
            "error": self.error,
            "balance_changes": self.balance_changes,
        }


class SimServer:
    """
    Solana simulation server for safe agent development.

    Wraps solana-test-validator with additional tooling for:
    - Automatic faucet airdrops
    - Program deployment simulation
    - State snapshot/restore for reproducible tests
    - Parallel simulation of multiple transaction paths

    Usage:
        # Start simulation environment
        sim = SimServer()
        await sim.start()

        # Simulate a transaction
        result = await sim.simulate_transaction(transaction_bytes)

        # Check if safe to execute
        if result.success and result.compute_units_consumed < 200_000:
            await agent.execute_on_real_network(transaction)

        # Cleanup
        await sim.stop()
    """

    def __init__(
        self,
        port: int = 8899,
        rpc_port: int = 8899,
        faucet_port: int = 9900,
        ledger_dir: Optional[Path] = None,
        verbose: bool = False,
        reset_ledger: bool = True,
        airdrop_sol: float = 1000.0,  # Starting SOL for test wallet
    ):
        self.port = port
        self.rpc_port = rpc_port
        self.faucet_port = faucet_port
        self.ledger_dir = ledger_dir or Path("./.simulator_ledger")
        self.verbose = verbose
        self.reset_ledger = reset_ledger
        self.airdrop_sol = airdrop_sol

        self._process: Optional[subprocess.Popen] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self._is_running = False
        self._start_time: Optional[float] = None

    @property
    def rpc_url(self) -> str:
        """Get the RPC URL for this simulator."""
        return f"http://localhost:{self.rpc_port}"

    async def start(self, timeout: float = 60.0) -> bool:
        """
        Start the simulation server.

        Args:
            timeout: Maximum time to wait for startup

        Returns:
            True if started successfully
        """
        if self._is_running:
            return True

        # Prepare ledger directory
        if self.reset_ledger and self.ledger_dir.exists():
            import shutil

            shutil.rmtree(self.ledger_dir)
        self.ledger_dir.mkdir(parents=True, exist_ok=True)

        # Build command
        cmd = [
            "solana-test-validator",
            "--ledger",
            str(self.ledger_dir),
            "--rpc-port",
            str(self.rpc_port),
            "--faucet-port",
            str(self.faucet_port),
            "--reset",  # Start from genesis
            "--quiet" if not self.verbose else "--log",
        ]

        # Skip cloning programs to speed up startup
        # builtin_programs = [
        #     "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",  # SPL Token
        #     "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb",  # Token-2022
        #     "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s",  # Metaplex
        # ]
        # for program in builtin_programs:
        #     cmd.extend(["--clone", program])

        print(f"🚀 Starting SimServer on port {self.rpc_port}...")

        # Start process
        self._process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE if not self.verbose else None,
            stderr=subprocess.PIPE if not self.verbose else None,
        )

        # Wait for RPC to be available
        self._session = aiohttp.ClientSession()
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                async with self._session.post(
                    self.rpc_url,
                    json={"jsonrpc": "2.0", "id": 1, "method": "getHealth"},
                    timeout=aiohttp.ClientTimeout(total=2),
                ) as resp:
                    if resp.status == 200:
                        self._is_running = True
                        self._start_time = time.time()
                        print(f"✅ SimServer ready at {self.rpc_url}")

                        # Fund test wallet
                        await self._fund_test_wallet()

                        return True
            except Exception:
                pass
            await asyncio.sleep(0.5)

        # Timeout - cleanup
        await self.stop()
        raise TimeoutError(f"SimServer failed to start within {timeout}s")

    async def stop(self):
        """Stop the simulation server."""
        if self._process:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None

        if self._session:
            await self._session.close()
            self._session = None

        self._is_running = False
        print("🛑 SimServer stopped")

    async def _fund_test_wallet(self):
        """Airdrop SOL to the test wallet."""
        # This would use the solana CLI or RPC to airdrop
        # For now, placeholder
        pass

    async def simulate_transaction(
        self,
        transaction_base64: str,
        signer_pubkeys: Optional[List[str]] = None,
        commitment: str = "confirmed",
    ) -> SimulationResult:
        """
        Simulate a transaction without submitting it.

        Args:
            transaction_base64: Base64-encoded transaction
            signer_pubkeys: Optional list of signers (for sigVerify)
            commitment: Confirmation level

        Returns:
            SimulationResult with detailed outcome
        """
        if not self._is_running:
            raise RuntimeError("SimServer not running. Call start() first.")

        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "simulateTransaction",
            "params": [
                transaction_base64,
                {
                    "encoding": "base64",
                    "commitment": commitment,
                    "replaceRecentBlockhash": True,
                    "sigVerify": False,  # Don't verify signatures in sim
                },
            ],
        }

        async with self._session.post(self.rpc_url, json=request) as resp:
            data = await resp.json()

            if "error" in data:
                return SimulationResult(
                    success=False,
                    signature=None,
                    slot=None,
                    compute_units_consumed=0,
                    accounts_changed=[],
                    logs=[],
                    error=data["error"].get("message", "Unknown error"),
                    error_code=data["error"].get("code"),
                )

            result = data.get("result", {}).get("value", {})

            return SimulationResult(
                success=result.get("err") is None,
                signature=None,  # No real signature in simulation
                slot=data.get("result", {}).get("context", {}).get("slot"),
                compute_units_consumed=result.get("unitsConsumed", 0),
                accounts_changed=[],  # Would parse from simulation result
                logs=result.get("logs", []),
                error=str(result.get("err")) if result.get("err") else None,
            )

    async def get_account_balance(self, pubkey: str) -> float:
        """Get account balance in SOL."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [pubkey],
        }

        async with self._session.post(self.rpc_url, json=request) as resp:
            data = await resp.json()
            lamports = data.get("result", {}).get("value", 0)
            return lamports / 1e9

    async def request_airdrop(self, pubkey: str, amount_sol: float = 1.0) -> str:
        """
        Request an airdrop of SOL.

        Returns:
            Transaction signature
        """
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "requestAirdrop",
            "params": [pubkey, int(amount_sol * 1e9)],
        }

        async with self._session.post(self.rpc_url, json=request) as resp:
            data = await resp.json()
            return data.get("result")

    async def get_slot(self) -> int:
        """Get current slot."""
        request = {"jsonrpc": "2.0", "id": 1, "method": "getSlot"}

        async with self._session.post(self.rpc_url, json=request) as resp:
            data = await resp.json()
            return data.get("result", 0)

    async def snapshot_state(self, name: str = "default") -> Path:
        """
        Create a snapshot of current ledger state for later restoration.

        This enables reproducible test scenarios and "save points" for
        complex multi-step agent operations.
        """
        snapshot_dir = self.ledger_dir / "snapshots" / name
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        # In production, this would copy ledger files
        # For now, placeholder
        return snapshot_dir

    async def restore_state(self, name: str = "default"):
        """Restore ledger from snapshot."""
        # Requires restart
        await self.stop()
        # Copy snapshot to ledger dir
        await self.start()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._process:
            self._process.terminate()
        return False

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()
        return False


# ============================================================================
# SIMULATION HELPERS
# ============================================================================


async def with_simulation(func, *args, **kwargs):
    """
    Decorator pattern for running code in simulation environment.

    Usage:
        result = await with_simulation(
            agent.execute_transaction,
            transaction_data
        )
    """
    async with SimServer() as sim:
        # Inject sim into function context if needed
        if hasattr(func, "__self__"):
            func.__self__.sim_server = sim
        return await func(*args, **kwargs)


def estimate_transaction_risk(
    simulation: SimulationResult, account_value_sol: float = 0.0
) -> Dict[str, Any]:
    """
    Estimate risk level of a transaction based on simulation results.

    Returns risk assessment with recommendations.
    """
    risks = []
    risk_level = "low"

    # Check compute units
    if simulation.compute_units_consumed > 1_000_000:
        risks.append("High compute usage - may fail during congestion")
        risk_level = "high"
    elif simulation.compute_units_consumed > 200_000:
        risks.append("Moderate compute usage")
        risk_level = "medium"

    # Check for errors
    if simulation.error:
        risks.append(f"Simulation error: {simulation.error}")
        risk_level = "critical"

    # Check account modifications
    sensitive_programs = ["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"]
    # Would check if sensitive programs are invoked

    return {
        "level": risk_level,
        "risks": risks,
        "recommendation": "proceed_with_caution" if risk_level != "low" else "proceed",
        "compute_efficiency": simulation.compute_units_consumed / 1_400_000,  # % of max
    }
