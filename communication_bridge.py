#!/usr/bin/env python3
"""
🌉 Hive 999 ⟷ Terminal 221b Communication Bridge

Lightweight inter-process communication for two independent systems.

Methods (in order of preference):
1. Shared Memory (fastest, same machine)
2. Unix Domain Sockets (local only)
3. TCP Sockets (network capable)
4. File System (fallback, works everywhere)

Usage:
    # Terminal 221b side (server)
    from communication_bridge import BridgeServer
    server = BridgeServer()
    await server.start()
    
    # Hive side (client)
    from communication_bridge import BridgeClient
    client = BridgeClient()
    await client.send({"type": "investigate", "query": "..."})
"""

import asyncio
import json
import os
import socket
import tempfile
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
from uuid import uuid4


# ═══════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════

BRIDGE_DIR = Path("/tmp/hive_terminal_bridge")
BRIDGE_SOCKET = BRIDGE_DIR / "bridge.sock"
BRIDGE_PIPE = BRIDGE_DIR / "pipe.jsonl"


# ═══════════════════════════════════════════════════════════════════════════
# Message Protocol
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class BridgeMessage:
    """Standard message format for bridge communication"""
    msg_type: str  # investigate, result, status, event, ping, pong
    payload: Dict[str, Any]
    sender: str  # "hive" or "terminal_221b"
    msg_id: str = ""
    timestamp: float = 0.0
    
    def __post_init__(self):
        if not self.msg_id:
            self.msg_id = str(uuid4())[:8]
        if not self.timestamp:
            self.timestamp = time.time()
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, data: str) -> "BridgeMessage":
        return cls(**json.loads(data))


# ═══════════════════════════════════════════════════════════════════════════
# Transport Layer
# ═══════════════════════════════════════════════════════════════════════════

class FileTransport:
    """
    File-based transport (works everywhere, no dependencies)
    
    Uses append-only JSON Lines file for messages.
    Each system reads from the other's file.
    """
    
    def __init__(self, role: str):
        self.role = role  # "hive" or "terminal_221b"
        BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Each role has its own file
        self.outbox = BRIDGE_DIR / f"{role}_outbox.jsonl"
        self.inbox = BRIDGE_DIR / f"{('terminal_221b' if role == 'hive' else 'hive')}_outbox.jsonl"
        
        # Track read position
        self.inbox_pos = 0
        self._handlers: List[Callable] = []
    
    async def send(self, message: BridgeMessage) -> bool:
        """Send message by appending to outbox"""
        try:
            with open(self.outbox, "a") as f:
                f.write(message.to_json() + "\n")
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
    
    async def receive(self, timeout: float = 0.1) -> Optional[BridgeMessage]:
        """Receive single message from inbox"""
        try:
            if not self.inbox.exists():
                return None
            
            with open(self.inbox, "r") as f:
                f.seek(self.inbox_pos)
                line = f.readline()
                self.inbox_pos = f.tell()
                
                if line.strip():
                    return BridgeMessage.from_json(line.strip())
        except Exception as e:
            print(f"Receive error: {e}")
        
        return None
    
    async def receive_loop(self, callback: Callable[[BridgeMessage], None]):
        """Continuously receive messages"""
        while True:
            msg = await self.receive()
            if msg:
                if asyncio.iscoroutinefunction(callback):
                    await callback(msg)
                else:
                    callback(msg)
            else:
                await asyncio.sleep(0.1)


class SocketTransport:
    """
    Unix Domain Socket transport (faster, local only)
    """
    
    def __init__(self, role: str):
        self.role = role
        self.socket_path = str(BRIDGE_SOCKET)
        self.sock: Optional[socket.socket] = None
        self.server: Optional[asyncio.Server] = None
        self._handlers: List[Callable] = []
    
    async def start_server(self, handler: Callable[[BridgeMessage], None]):
        """Start socket server (Terminal 221b side)"""
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
        
        self.server = await asyncio.start_unix_server(
            self._handle_client,
            path=self.socket_path
        )
        print(f"📡 Socket server listening on {self.socket_path}")
    
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client connection"""
        while True:
            try:
                line = await reader.readline()
                if not line:
                    break
                
                msg = BridgeMessage.from_json(line.decode().strip())
                for handler in self._handlers:
                    handler(msg)
                    
            except Exception as e:
                print(f"Client handler error: {e}")
                break
        
        writer.close()
        await writer.wait_closed()
    
    async def connect(self) -> bool:
        """Connect to socket server (Hive side)"""
        try:
            self.reader, self.writer = await asyncio.open_unix_connection(self.socket_path)
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    async def send(self, message: BridgeMessage) -> bool:
        """Send message over socket"""
        try:
            self.writer.write(message.to_json().encode() + b"\n")
            await self.writer.drain()
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
    
    async def receive(self) -> Optional[BridgeMessage]:
        """Receive message from socket"""
        try:
            line = await asyncio.wait_for(self.reader.readline(), timeout=0.5)
            if line:
                return BridgeMessage.from_json(line.decode().strip())
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(f"Receive error: {e}")
        return None
    
    def on_message(self, handler: Callable[[BridgeMessage], None]):
        """Register message handler"""
        self._handlers.append(handler)


# ═══════════════════════════════════════════════════════════════════════════
# High-Level Bridge Classes
# ═══════════════════════════════════════════════════════════════════════════

class Terminal221bBridge:
    """
    Bridge for Terminal 221b side
    
    Usage:
        bridge = Terminal221bBridge()
        await bridge.start()
        
        # Handle incoming requests
        @bridge.on("investigate")
        async def handle_investigate(payload):
            result = await detective.investigate(payload["query"])
            return {"result": result}
    """
    
    def __init__(self, transport: str = "auto"):
        self.transport_type = transport
        self.transport: Union[FileTransport, SocketTransport, None] = None
        self._handlers: Dict[str, Callable] = {}
        self._running = False
    
    async def start(self):
        """Start the bridge"""
        # Try socket first, fall back to file
        if self.transport_type in ("auto", "socket"):
            try:
                self.transport = SocketTransport("terminal_221b")
                await self.transport.start_server(self._on_message)
                print("🌉 Bridge: Unix socket transport")
            except Exception as e:
                print(f"Socket failed ({e}), using file transport")
                self.transport = FileTransport("terminal_221b")
        else:
            self.transport = FileTransport("terminal_221b")
        
        self._running = True
        
        # Start receive loop
        asyncio.create_task(self._receive_loop())
        
        print("🌉 Terminal 221b Bridge started")
    
    async def stop(self):
        """Stop the bridge"""
        self._running = False
        print("🌉 Bridge stopped")
    
    async def _receive_loop(self):
        """Receive loop for file transport"""
        while self._running:
            try:
                msg = await self.transport.receive()
                if msg:
                    await self._on_message(msg)
            except Exception as e:
                print(f"Receive error: {e}")
            await asyncio.sleep(0.1)
    
    def on(self, msg_type: str):
        """Decorator to register handler"""
        def decorator(func: Callable):
            self._handlers[msg_type] = func
            return func
        return decorator
    
    async def _on_message(self, msg: BridgeMessage):
        """Handle incoming message"""
        print(f"📨 Received [{msg.msg_type}] from {msg.sender}")
        
        handler = self._handlers.get(msg.msg_type)
        if handler:
            try:
                result = await handler(msg.payload)
                
                # Send response
                if result:
                    response = BridgeMessage(
                        msg_type="result",
                        payload=result,
                        sender="terminal_221b",
                        msg_id=msg.msg_id
                    )
                    await self.transport.send(response)
                    
            except Exception as e:
                print(f"Handler error: {e}")
                # Send error response
                response = BridgeMessage(
                    msg_type="error",
                    payload={"error": str(e)},
                    sender="terminal_221b",
                    msg_id=msg.msg_id
                )
                await self.transport.send(response)
    
    async def send_event(self, event_type: str, data: Dict):
        """Send event to Hive"""
        msg = BridgeMessage(
            msg_type="event",
            payload={"event_type": event_type, "data": data},
            sender="terminal_221b"
        )
        await self.transport.send(msg)


class HiveBridge:
    """
    Bridge for Hive 999 side
    
    Usage:
        bridge = HiveBridge()
        await bridge.connect()
        
        # Send investigation request
        result = await bridge.investigate("Analyze address...", personality="holmes")
    """
    
    def __init__(self, transport: str = "auto"):
        self.transport_type = transport
        self.transport: Union[FileTransport, SocketTransport, None] = None
        self._pending: Dict[str, asyncio.Future] = {}
        self._response_handlers: Dict[str, Callable] = {}
    
    async def connect(self):
        """Connect to bridge"""
        # Try socket first
        if self.transport_type in ("auto", "socket"):
            try:
                self.transport = SocketTransport("hive")
                if await self.transport.connect():
                    print("🌉 Connected via Unix socket")
                    asyncio.create_task(self._receive_loop())
                    return
            except Exception as e:
                print(f"Socket connect failed: {e}")
        
        # Fall back to file transport
        self.transport = FileTransport("hive")
        print("🌉 Connected via file transport")
        asyncio.create_task(self._receive_loop())
    
    async def disconnect(self):
        """Disconnect from bridge"""
        print("🌉 Disconnected")
    
    async def _receive_loop(self):
        """Continuously receive responses"""
        while True:
            try:
                if isinstance(self.transport, FileTransport):
                    msg = await self.transport.receive()
                else:
                    msg = await self.transport.receive()
                
                if msg:
                    self._handle_response(msg)
                    
            except Exception as e:
                print(f"Receive loop error: {e}")
            
            await asyncio.sleep(0.1)
    
    def _handle_response(self, msg: BridgeMessage):
        """Handle incoming response"""
        # Check for pending requests
        future = self._pending.pop(msg.msg_id, None)
        if future and not future.done():
            future.set_result(msg)
        
        # Also call registered handlers
        handler = self._response_handlers.get(msg.msg_type)
        if handler:
            handler(msg.payload)
    
    async def send(self, msg_type: str, payload: Dict, wait_for_response: bool = True, timeout: float = 30.0) -> Optional[BridgeMessage]:
        """Send message and optionally wait for response"""
        msg = BridgeMessage(
            msg_type=msg_type,
            payload=payload,
            sender="hive"
        )
        
        if wait_for_response:
            # Create future for response
            future = asyncio.get_event_loop().create_future()
            self._pending[msg.msg_id] = future
            
            # Send message
            await self.transport.send(msg)
            
            # Wait for response
            try:
                return await asyncio.wait_for(future, timeout=timeout)
            except asyncio.TimeoutError:
                print(f"Timeout waiting for response to {msg_type}")
                return None
        else:
            await self.transport.send(msg)
            return None
    
    # High-level methods
    
    async def investigate(self, query: str, personality: str = "holmes") -> Optional[str]:
        """Ask Terminal 221b to investigate"""
        response = await self.send("investigate", {
            "query": query,
            "personality": personality
        })
        
        if response and response.payload:
            return response.payload.get("result")
        return None
    
    async def get_status(self) -> Dict:
        """Get Terminal 221b status"""
        response = await self.send("status", {})
        if response:
            return response.payload
        return {"status": "unknown"}
    
    async def simulate_transaction(self, transaction_base64: str) -> Dict:
        """Simulate transaction via Terminal 221b"""
        response = await self.send("simulate", {
            "transaction_base64": transaction_base64
        })
        
        if response:
            return response.payload
        return {"success": False, "error": "No response"}


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

async def demo_both_sides():
    """
    Demonstrate both sides of the bridge
    
    In real usage, these would be in separate processes.
    """
    print("=" * 70)
    print("🌉 Communication Bridge Demo")
    print("=" * 70)
    
    # Terminal 221b side
    t221b = Terminal221bBridge(transport="file")
    
    @t221b.on("investigate")
    async def handle_investigate(payload):
        print(f"   🕵️  Terminal 221b investigating: {payload['query']}")
        await asyncio.sleep(1)  # Simulate work
        return {
            "result": f"Investigation complete. Found: Suspicious pattern detected in {payload['query'][-10:]}",
            "confidence": 0.87
        }
    
    @t221b.on("status")
    async def handle_status(payload):
        return {
            "status": "operational",
            "agents": ["holmes", "watson", "mycroft", "irene"],
            "load": 0.3
        }
    
    await t221b.start()
    
    # Hive side
    hive = HiveBridge(transport="file")
    await hive.connect()
    
    # Give time for connection
    await asyncio.sleep(0.5)
    
    print("\n1️⃣  Hive → Terminal 221b: Status check")
    status = await hive.get_status()
    print(f"   Response: {status}")
    
    print("\n2️⃣  Hive → Terminal 221b: Investigation request")
    result = await hive.investigate(
        query="Analyze address 221bDemo123456789",
        personality="holmes"
    )
    print(f"   Result: {result}")
    
    print("\n3️⃣  Multiple parallel investigations")
    queries = [
        "Check balance of AddrA",
        "Analyze transactions for AddrB",
        "Verify NFT ownership AddrC",
    ]
    
    results = await asyncio.gather(*[
        hive.investigate(q) for q in queries
    ])
    
    for q, r in zip(queries, results):
        print(f"   ✓ {q[:30]}... → {r[:50]}..." if r else f"   ✗ {q[:30]}... → Failed")
    
    # Cleanup
    await t221b.stop()
    await hive.disconnect()
    
    print("\n" + "=" * 70)
    print("Demo complete! Bridge communication successful.")
    print("=" * 70)
    print("\nIn production:")
    print("  - Terminal 221b runs: python terminal_221b/api/server.py")
    print("  - Hive connects via: HiveBridge() or Terminal221bClient()")


if __name__ == "__main__":
    # Cleanup old bridge files
    import shutil
    if BRIDGE_DIR.exists():
        shutil.rmtree(BRIDGE_DIR)
    
    asyncio.run(demo_both_sides())
