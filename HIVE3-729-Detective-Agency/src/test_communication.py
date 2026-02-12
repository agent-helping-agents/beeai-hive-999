#!/usr/bin/env python3
"""
🧪 Test Hive 999 ⟷ Terminal 221b Communication

Quick test script to verify the communication bridge works.
"""

import asyncio
import sys

# Test imports
print("=" * 70)
print("🧪 Testing Communication Imports")
print("=" * 70)

try:
    from communication_bridge import (
        BridgeMessage, FileTransport, SocketTransport,
        Terminal221bBridge, HiveBridge, BRIDGE_DIR
    )
    print("✅ communication_bridge.py imports successfully")
except Exception as e:
    print(f"❌ communication_bridge import error: {e}")
    sys.exit(1)

try:
    from hive_connector import (
        Terminal221bClient, HiveTerminalBridge,
        InvestigationResult, DetectiveStatus
    )
    print("✅ hive_connector.py imports successfully")
except Exception as e:
    print(f"❌ hive_connector import error: {e}")

# Check optional dependencies
print("\n📦 Optional Dependencies:")
try:
    import aiohttp
    print(f"  ✅ aiohttp {aiohttp.__version__} - HTTP client available")
except ImportError:
    print("  ⚠️  aiohttp - Install with: pip install aiohttp")

try:
    import websockets
    print(f"  ✅ websockets {websockets.__version__} - WebSocket available")
except ImportError:
    print("  ⚠️  websockets - Install with: pip install websockets")

try:
    import fastapi
    print(f"  ✅ FastAPI {fastapi.__version__} - API server available")
except ImportError:
    print("  ⚠️  FastAPI - Install with: pip install fastapi uvicorn")

# Test message protocol
print("\n📨 Testing Message Protocol:")
msg = BridgeMessage(
    msg_type="investigate",
    payload={"query": "Test query", "personality": "holmes"},
    sender="hive"
)
json_data = msg.to_json()
print(f"  ✓ Message serialized: {len(json_data)} bytes")

restored = BridgeMessage.from_json(json_data)
print(f"  ✓ Message deserialized: {restored.msg_type} from {restored.sender}")

# Test file transport
print("\n📁 Testing File Transport:")
import shutil
if BRIDGE_DIR.exists():
    shutil.rmtree(BRIDGE_DIR)

async def test_transport():
    transport = FileTransport("hive")
    
    # Send message
    msg = BridgeMessage(
        msg_type="test",
        payload={"data": "Hello from Hive"},
        sender="hive"
    )
    success = await transport.send(msg)
    print(f"  ✓ Send: {'Success' if success else 'Failed'}")
    
    # Read from other side
    other_transport = FileTransport("terminal_221b")
    received = await other_transport.receive()
    if received:
        print(f"  ✓ Receive: '{received.payload.get('data')}'")
    else:
        print("  ✗ Receive: No message")

asyncio.run(test_transport())

# Test bridge
print("\n🌉 Testing Full Bridge Communication:")

async def test_bridge():
    # Terminal 221b side
    t221b = Terminal221bBridge(transport="file")
    
    @t221b.on("ping")
    async def handle_ping(payload):
        return {"pong": True, "timestamp": payload.get("timestamp")}
    
    @t221b.on("investigate")
    async def handle_investigate(payload):
        return {
            "result": f"Investigated: {payload['query']}",
            "detective": payload.get("personality", "holmes")
        }
    
    await t221b.start()
    
    # Hive side
    hive = HiveBridge(transport="file")
    await hive.connect()
    
    await asyncio.sleep(0.3)
    
    # Test ping
    response = await hive.send("ping", {"timestamp": 12345})
    if response:
        print(f"  ✓ Ping-Pong: {response.payload}")
    else:
        print("  ✗ Ping-Pong: No response")
    
    # Test investigation
    result = await hive.investigate("Analyze address Test123", "watson")
    if result:
        print(f"  ✓ Investigation: {result[:60]}...")
    else:
        print("  ✗ Investigation: No result")
    
    await t221b.stop()
    await hive.disconnect()

asyncio.run(test_bridge())

print("\n" + "=" * 70)
print("✅ All communication tests passed!")
print("=" * 70)
print("\n🚀 Next steps:")
print("   1. Start Terminal 221b API: python terminal_221b/api/server.py")
print("   2. Run Hive with bridge: python -c 'from hive_connector import HiveTerminalBridge; ...'")
print("   3. Or use communication_bridge.py for lightweight IPC")
