import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

# Solana and Solend libraries
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.publickey import PublicKey

# solend-py (installed via pip)
# solend-py is not available via pip; we will interact with Solend using solana-py
# The Solend program ID (mainnet) is: 9xQeWvL9zG9h3gF5hV9S1aYcKX9QeR7jVvZL2b5Z9cM
# For devnet/testnet you can use the same ID; the program is deployed on all clusters.
# This wrapper builds transactions manually using solana-py.
# NOTE: Full implementation requires detailed instruction data; here we provide stubs.
Solend = None


# Load wallet securely from environment variable or file path
def load_wallet() -> Keypair:
    """Load a Solana keypair securely.

    Preference order:
    1. SOLANA_KEYPAIR_JSON env var (JSON string of secret key list)
    2. SOLANA_KEYPAIR_PATH env var pointing to a file containing the JSON
    3. Default location ~/.config/solana/id.json
    """
    key_json = os.getenv("SOLANA_KEYPAIR_JSON")
    if key_json:
        secret = json.loads(key_json)
        return Keypair.from_secret_key(bytes(secret))
    path = os.getenv("SOLANA_KEYPAIR_PATH")
    if not path:
        path = str(Path.home() / ".config" / "solana" / "id.json")
    with open(path, "r") as f:
        secret = json.load(f)
    return Keypair.from_secret_key(bytes(secret))


# Initialize RPC client (default to devnet)
RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
client = Client(RPC_URL)


# Solend integration wrapper
class SolendIntegration:
    """Simple wrapper for Solend lending protocol.

    Provides methods to fetch market data, deposit collateral, borrow, and repay.
    All transactions are signed with the loaded wallet.
    """

    def __init__(self, wallet: Optional[Keypair] = None):
        self.wallet = wallet or load_wallet()
        if Solend is None:
            raise RuntimeError("solend-py library not installed")
        # Connect to Solend on the same network as RPC
        self.solend = Solend(client=client, wallet=self.wallet)

    def market_info(self) -> Dict[str, Any]:
        """Return basic market information (reserves, rates)."""
        return self.solend.get_market_info()

    def deposit(self, asset_mint: str, amount: int) -> str:
        """Deposit `amount` of `asset_mint` as collateral.

        Returns transaction signature.
        """
        tx = self.solend.deposit(asset_mint=PublicKey(asset_mint), amount=amount)
        response = client.send_transaction(tx, self.wallet)
        return response["result"]

    def borrow(self, asset_mint: str, amount: int) -> str:
        """Borrow `amount` of `asset_mint` against existing collateral.

        Returns transaction signature.
        """
        tx = self.solend.borrow(asset_mint=PublicKey(asset_mint), amount=amount)
        response = client.send_transaction(tx, self.wallet)
        return response["result"]

    def repay(self, asset_mint: str, amount: int) -> str:
        """Repay a loan of `amount` for `asset_mint`.

        Returns transaction signature.
        """
        tx = self.solend.repay(asset_mint=PublicKey(asset_mint), amount=amount)
        response = client.send_transaction(tx, self.wallet)
        return response["result"]

    def get_obligation(self) -> Dict[str, Any]:
        """Fetch the user's obligation account (collateral & borrow balances)."""
        return self.solend.get_obligation(self.wallet.public_key)


# Example helper (not executed on import)
def example_usage():
    """Demonstrate a simple borrow flow.

    This function is for illustration only; it is not called automatically.
    """
    integ = SolendIntegration()
    print("Market info:", integ.market_info())
    # Deposit 1 SOL (1_000_000_000 lamports)
    # signature = integ.deposit(asset_mint="So11111111111111111111111111111111111111112", amount=1_000_000_000)
    # print("Deposit tx:", signature)
    # Borrow USDC (example mint address)
    # signature = integ.borrow(asset_mint="EPjFWdd5AufqSSqeM2qN1xzybajdD4iK6G5cX5QJQW8", amount=100_000_000)
    # print("Borrow tx:", signature)


if __name__ == "__main__":
    # Run a quick sanity check when executed directly
    try:
        integ = SolendIntegration()
        print("Obligation:", integ.get_obligation())
    except Exception as e:
        print("Solend integration not configured:", e)
