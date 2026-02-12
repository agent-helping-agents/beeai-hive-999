#!/usr/bin/env python3
"""Secure server without SimServer dependency for testing"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager

# Import the secure server but mock the SimServer
sys.path.insert(0, '/home/boozelee/beeai-hive-999')

# Mock SimServer for testing
class MockSimServer:
    def __init__(self, *args, **kwargs):
        self.rpc_url = "http://localhost:8899"
        self.is_running = True
    
    async def start(self):
        print("   ✅ Mock SimServer (testing mode)")
    
    async def stop(self):
        self.is_running = False
    
    async def get_slot(self):
        return 12345
    
    async def request_airdrop(self, *args, **kwargs):
        return "mock_signature"
    
    async def get_account_balance(self, *args, **kwargs):
        return 10.0
    
    async def simulate_transaction(self, *args, **kwargs):
        class MockResult:
            success = True
            logs = ["mock log"]
            units_consumed = 1000
            error = None
            def to_dict(self):
                return {"success": True, "logs": self.logs, "units_consumed": self.units_consumed}
        return MockResult()

# Patch SimServer before importing
import terminal_221b.simulation.sim_server as sim_module
sim_module.SimServer = MockSimServer

# Now import and run the secure server
from terminal_221b.api.secure_server import *

# Override lifespan to use mock SimServer
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔒 Starting Secure Terminal 221b API Server (TESTING MODE)...")
    
    # Use mock SimServer
    app.state.sim_server = MockSimServer()
    await app.state.sim_server.start()
    
    # Initialize agents with mock
    from terminal_221b.agents.advisor_deps import get_simulation_config
    
    deps = get_simulation_config()
    
    # Create mock agents
    class MockAgent:
        def __init__(self, personality):
            self.personality = personality
            self.id = f"mock-{personality}"
            self.sim_server = app.state.sim_server
        
        async def investigate(self, query):
            await asyncio.sleep(0.5)  # Simulate work
            return f"[{self.personality.upper()}] Investigation of '{query[:30]}...': Suspicious pattern detected. Recommendation: Further analysis required."
    
    app.state.agents = {
        "holmes": MockAgent("holmes"),
        "watson": MockAgent("watson"),
        "mycroft": MockAgent("mycroft"),
        "irene": MockAgent("irene"),
    }
    print(f"   ✅ 4 mock detectives ready")
    
    app.state.investigations = {}
    app.state.websocket_connections = set()
    
    print(f"\n🔒 Secure Terminal 221b API Server ready!")
    print(f"   ⚠️  Using MOCK SimServer - for testing only!")
    print(f"   ⚠️  Change default passwords before production use!")
    print(f"   Docs: http://localhost:22181/docs")
    
    yield
    
    print("\n🛑 Shutting down...")
    if app.state.sim_server:
        await app.state.sim_server.stop()

# Update app lifespan
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    print("Starting secure server in TESTING MODE (no Solana required)")
    uvicorn.run(app, host="0.0.0.0", port=22181)
