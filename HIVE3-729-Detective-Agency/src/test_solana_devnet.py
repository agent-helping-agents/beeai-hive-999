#!/usr/bin/env python3
"""Test script for Solana devnet integration.

Verifies that we can:
1. Connect to Solana devnet
2. Get block hash
3. Check lamports (SOL) balance of a public key
4. Check cluster version
"""

import sys
import os
from typing import Optional
from solana.rpc.api import Client
from solders.pubkey import Pubkey

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Test configuration
TEST_PUBLIC_KEY = Pubkey.from_string(
    "11111111111111111111111111111111"
)  # Solana system program (always exists)
DEVNET_RPC_URL = "https://api.devnet.solana.com"


def test_solana_connection() -> bool:
    """Test basic Solana devnet connection."""
    print("🔗 Testing Solana devnet connection...")

    try:
        client = Client(DEVNET_RPC_URL)

        print("📦 Checking cluster connection...")
        response = client.is_connected()
        if not response:
            print("❌ Cluster connection failed")
            return False

        print("✅ Cluster connected successfully")

        print("\n📦 Getting recent blockhash...")
        blockhash_response = client.get_latest_blockhash()
        if blockhash_response.value:
            blockhash = str(blockhash_response.value.blockhash)
            print(f"✅ Blockhash: {blockhash[:8]}...")
        else:
            print("❌ Failed to get blockhash")
            return False

        print("\n📦 Checking cluster version...")
        version_response = client.get_version()
        if version_response.value:
            version = version_response.value.solana_core
            print(f"✅ Solana version: {version}")
        else:
            print("❌ Failed to get cluster version")
            return False

        print("\n📦 Checking system program balance...")
        balance_response = client.get_balance(TEST_PUBLIC_KEY)
        if balance_response.value is not None:
            balance_sol = balance_response.value / 1e9  # Convert lamports to SOL
            print(f"✅ System program balance: {balance_sol:.2f} SOL")
        else:
            print("❌ Failed to get system program balance")
            return False

        print("\n🎉 Solana devnet integration test PASSED!")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        print(traceback.format_exc())
        return False


def main():
    """Main function to run the test."""
    print("Solana Devnet Integration Test")
    print("=" * 50)

    if test_solana_connection():
        print("\n✅ The Hive is ready for Solana devnet deployment!")
    else:
        print("\n❌ Solana devnet integration test FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()
