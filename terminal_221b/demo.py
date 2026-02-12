#!/usr/bin/env python3
"""
Terminal 221b - Demo Script

Demonstrates the Sherlock Holmes-inspired Solana AI agent system.
Run this to see Terminal 221b in action without affecting the main TUI.

Usage:
    python terminal_221b/demo.py

"""

import asyncio
import os
import sys

# Project root setup
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from terminal_221b.agents.advisor_deps import AdvisorDeps, get_simulation_config
from terminal_221b.agents.detective_agent import (
    create_holmes,
    create_watson,
    create_mycroft,
    create_irene,
)
from terminal_221b.agents.worker_pool import parallel_investigations


async def demo_personalities():
    """Demo all four detective personalities."""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     🕵️  TERMINAL 221b - PERSONALITY DEMONSTRATION         ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    deps = get_simulation_config()
    
    # Create all detectives
    print("🔧 Initializing detective agents...\n")
    holmes = await create_holmes(deps)
    watson = await create_watson(deps)
    mycroft = await create_mycroft(deps)
    irene = await create_irene(deps)
    
    # Test query
    query = "Analyze the transaction patterns of address 221bDetectiveDemo"
    
    print("=" * 60)
    print("Query:", query)
    print("=" * 60)
    
    # Holmes
    print("\n🎩 SHERLOCK HOLMES:")
    print("-" * 40)
    response = await holmes.investigate(query)
    print(response)
    
    # Watson
    print("\n🩺 DR. WATSON:")
    print("-" * 40)
    response = await watson.investigate(query)
    print(response)
    
    # Mycroft
    print("\n🌐 MYCROFT HOLMES:")
    print("-" * 40)
    response = await mycroft.investigate(query)
    print(response)
    
    # Irene
    print("\n💋 IRENE ADLER:")
    print("-" * 40)
    response = await irene.investigate(query)
    print(response)
    
    # Cleanup
    if holmes.sim_server:
        await holmes.sim_server.stop()


async def demo_simulation():
    """Demo the simulation server."""
    print("\n\n╔══════════════════════════════════════════════════════════╗")
    print("║     🔬 SIMULATION SERVER DEMONSTRATION                  ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    from terminal_221b.simulation.sim_server import SimServer
    
    print("🚀 Starting simulation server...")
    sim = SimServer(port=8899, verbose=False)
    await sim.start()
    
    print(f"✅ Server running at {sim.rpc_url}\n")
    
    # Get current slot
    slot = await sim.get_slot()
    print(f"📦 Current slot: {slot}")
    
    # Request airdrop to test address
    test_address = "DetectiveDemoAddress111111111111111111111111111"
    print(f"\n💧 Requesting airdrop for {test_address[:20]}...")
    sig = await sim.request_airdrop(test_address, 10.0)
    print(f"✅ Airdrop signature: {sig}")
    
    # Check balance
    balance = await sim.get_account_balance(test_address)
    print(f"💰 Balance: {balance:.4f} SOL")
    
    # Simulate a transaction
    print("\n🔬 Simulating transaction...")
    # In production, this would be a real transaction
    sim_result = await sim.simulate_transaction(
        "AQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRobHB0eHyAhIiMkJSYnKCkqKywtLi8wMTIzNDU2Nzg5Ojs8PT4/"
    )
    print(f"Simulation result: {sim_result.to_dict()}")
    
    print("\n🛑 Stopping simulation server...")
    await sim.stop()
    print("✅ Demo complete!")


async def demo_parallel_investigation():
    """Demo parallel investigations with worker pool."""
    print("\n\n╔══════════════════════════════════════════════════════════╗")
    print("║     ⚡ PARALLEL INVESTIGATION DEMONSTRATION             ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    queries = [
        "What is the balance of address A111?",
        "Analyze transactions for address B222",
        "Check token holdings of address C333",
        "Investigate NFT collection for address D444",
    ]
    
    print(f"Submitting {len(queries)} parallel investigations...\n")
    
    results = await parallel_investigations(
        queries=queries,
        max_workers=3,
        personality="holmes"
    )
    
    for i, (query, result) in enumerate(zip(queries, results)):
        print(f"\n--- Investigation {i+1} ---")
        print(f"Query: {query}")
        print(f"Result: {result[:100]}..." if len(str(result)) > 100 else f"Result: {result}")


async def demo_transfer_with_safety():
    """Demo safe transfer with simulation and approval."""
    print("\n\n╔══════════════════════════════════════════════════════════╗")
    print("║     🛡️  SAFE TRANSFER DEMONSTRATION                     ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    deps = get_simulation_config()
    agent = await create_holmes(deps)
    
    print("Scenario: Transfer 1.5 SOL to recipient")
    print("Safety: Simulation mode (no real funds moved)\n")
    
    # First, simulate
    print("Step 1: Simulating transaction...")
    result = await agent.execute_transfer(
        recipient="RecipientAddress11111111111111111111111111",
        amount=1.5,
        simulate_first=True
    )
    
    print(f"Simulation result: {result}")
    
    # Show stats
    print("\n📊 Agent Statistics:")
    stats = agent.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    if agent.sim_server:
        await agent.sim_server.stop()


async def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("  🕵️  TERMINAL 221b - SOLANA AI DETECTIVE SYSTEM")
    print("  " + "-" * 66)
    print("  A Sherlock Holmes-inspired AI for blockchain investigation")
    print("=" * 70 + "\n")
    
    try:
        await demo_personalities()
    except Exception as e:
        print(f"\n❌ Personality demo failed: {e}")
    
    try:
        await demo_simulation()
    except Exception as e:
        print(f"\n❌ Simulation demo failed: {e}")
        print("   (Make sure solana-test-validator is installed)")
    
    try:
        await demo_parallel_investigation()
    except Exception as e:
        print(f"\n❌ Parallel investigation demo failed: {e}")
    
    try:
        await demo_transfer_with_safety()
    except Exception as e:
        print(f"\n❌ Transfer demo failed: {e}")
    
    print("\n" + "=" * 70)
    print("  ✨ Demo complete! Start the full TUI with: ./run.sh")
    print("  Then try: :221b help")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
