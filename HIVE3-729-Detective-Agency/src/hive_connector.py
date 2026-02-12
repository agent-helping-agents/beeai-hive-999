#!/usr/bin/env python3
"""
🐝 Hive 999 ⟷ Terminal 221b Connector

This module allows BeeAI Hive 999 to communicate with Terminal 221b
without merging the codebases. They remain independent services.

Communication Methods:
1. HTTP REST API - For synchronous requests
2. WebSocket - For real-time streaming
3. Shared Events - Via Redis or file system

Usage:
    from hive_connector import Terminal221bClient
    
    # Connect to Terminal 221b
    client = Terminal221bClient(base_url="http://localhost:22181")
    
    # Start investigation
    result = await client.investigate(
        query="Analyze address 9x...",
        personality="holmes"
    )
    
    # Or use WebSocket for streaming
    async for message in client.stream_investigation("Analyze transaction..."):
        print(message)
"""

import asyncio
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, AsyncIterator, Dict, Optional, Callable
from uuid import uuid4

# HTTP client
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False
    print("⚠️  aiohttp not installed. Run: pip install aiohttp")

# WebSocket client
try:
    import websockets
    HAS_WEBSOCKETS = True
except ImportError:
    HAS_WEBSOCKETS = False


# ═══════════════════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class InvestigationResult:
    """Result from Terminal 221b investigation"""
    investigation_id: str
    status: str
    personality: str
    query: str
    result: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class DetectiveStatus:
    """Status of a detective agent"""
    agent_id: str
    personality: str
    status: str
    investigations_completed: int = 0


# ═══════════════════════════════════════════════════════════════════════════
# Terminal 221b Client
# ═══════════════════════════════════════════════════════════════════════════

class Terminal221bClient:
    """
    Client for communicating with Terminal 221b API
    
    This allows Hive 999 to use Terminal 221b's detective capabilities
    without directly importing or merging code.
    """
    
    def __init__(self, base_url: str = "http://localhost:22181", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session: Optional[Any] = None
        self.websocket: Optional[Any] = None
        self._event_handlers: Dict[str, List[Callable]] = {}
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def connect(self):
        """Establish HTTP session"""
        if HAS_AIOHTTP:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        else:
            raise ImportError("aiohttp required. Run: pip install aiohttp")
    
    async def close(self):
        """Close connections"""
        if self.session:
            await self.session.close()
            self.session = None
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
    
    # ═══════════════════════════════════════════════════════════════════════
    # REST API Methods
    # ═══════════════════════════════════════════════════════════════════════
    
    async def health_check(self) -> Dict[str, Any]:
        """Check if Terminal 221b is healthy"""
        async with self.session.get(f"{self.base_url}/health") as resp:
            return await resp.json()
    
    async def get_detectives(self) -> list:
        """List available detectives"""
        async with self.session.get(f"{self.base_url}/detectives") as resp:
            return await resp.json()
    
    async def investigate(
        self, 
        query: str, 
        personality: str = "holmes",
        context: Optional[Dict] = None
    ) -> InvestigationResult:
        """
        Start an investigation and wait for result
        
        Args:
            query: What to investigate
            personality: Which detective (holmes/watson/mycroft/irene)
            context: Additional context
        
        Returns:
            InvestigationResult with findings
        """
        # Start investigation
        payload = {
            "query": query,
            "personality": personality,
            "context": context or {}
        }
        
        async with self.session.post(
            f"{self.base_url}/investigate",
            json=payload
        ) as resp:
            data = await resp.json()
            investigation_id = data["investigation_id"]
        
        # Poll for completion
        max_attempts = 60  # 60 seconds max
        for _ in range(max_attempts):
            await asyncio.sleep(1)
            
            async with self.session.get(
                f"{self.base_url}/investigate/{investigation_id}"
            ) as resp:
                result = await resp.json()
                
                if result["status"] in ("completed", "error"):
                    return InvestigationResult(**result)
        
        raise TimeoutError(f"Investigation {investigation_id} timed out")
    
    async def investigate_async(
        self,
        query: str,
        personality: str = "holmes",
        context: Optional[Dict] = None
    ) -> str:
        """
        Start investigation and return ID immediately (don't wait)
        
        Returns:
            investigation_id - Use get_investigation_result() to check later
        """
        payload = {
            "query": query,
            "personality": personality,
            "context": context or {}
        }
        
        async with self.session.post(
            f"{self.base_url}/investigate",
            json=payload
        ) as resp:
            data = await resp.json()
            return data["investigation_id"]
    
    async def get_investigation_result(self, investigation_id: str) -> InvestigationResult:
        """Get result of an investigation by ID"""
        async with self.session.get(
            f"{self.base_url}/investigate/{investigation_id}"
        ) as resp:
            data = await resp.json()
            return InvestigationResult(**data)
    
    async def simulate_transaction(self, transaction_base64: str) -> Dict[str, Any]:
        """Simulate a transaction via Terminal 221b's SimServer"""
        payload = {"transaction_base64": transaction_base64}
        
        async with self.session.post(
            f"{self.base_url}/simulate",
            json=payload
        ) as resp:
            return await resp.json()
    
    async def send_hive_message(self, message_type: str, payload: Dict) -> Dict:
        """Send a message from Hive to Terminal 221b"""
        message = {
            "message_type": message_type,
            "payload": payload,
            "source": "hive_999",
            "timestamp": datetime.now().isoformat()
        }
        
        async with self.session.post(
            f"{self.base_url}/hive/message",
            json=message
        ) as resp:
            return await resp.json()
    
    async def quick_query(self, query_type: str, query: str) -> Dict:
        """Quick query endpoint for Hive integration"""
        async with self.session.get(
            f"{self.base_url}/hive/query/{query_type}",
            params={"q": query}
        ) as resp:
            return await resp.json()
    
    # ═══════════════════════════════════════════════════════════════════════
    # WebSocket Methods (Real-time)
    # ═══════════════════════════════════════════════════════════════════════
    
    async def connect_websocket(self) -> bool:
        """Connect to WebSocket for real-time updates"""
        if not HAS_WEBSOCKETS:
            raise ImportError("websockets required. Run: pip install websockets")
        
        ws_url = self.base_url.replace("http://", "ws://").replace("https://", "wss://")
        self.websocket = await websockets.connect(f"{ws_url}/ws")
        
        # Wait for connection confirmation
        response = await self.websocket.recv()
        data = json.loads(response)
        
        return data.get("type") == "connected"
    
    async def stream_investigation(
        self,
        query: str,
        personality: str = "holmes"
    ) -> AsyncIterator[Dict]:
        """
        Stream investigation progress in real-time
        
        Yields:
            Dict with type and message/result
        
        Example:
            async for msg in client.stream_investigation("Analyze address..."):
                if msg["type"] == "thinking":
                    print(f"Thinking: {msg['message']}")
                elif msg["type"] == "result":
                    print(f"Result: {msg['result']}")
        """
        if not self.websocket:
            await self.connect_websocket()
        
        # Send investigation request
        await self.websocket.send(json.dumps({
            "type": "investigate",
            "personality": personality,
            "query": query
        }))
        
        # Stream responses
        while True:
            try:
                response = await asyncio.wait_for(
                    self.websocket.recv(),
                    timeout=self.timeout
                )
                data = json.loads(response)
                yield data
                
                # Stop if we get result or error
                if data.get("type") in ("result", "error"):
                    break
                    
            except asyncio.TimeoutError:
                yield {"type": "error", "message": "Timeout"}
                break
    
    async def subscribe_to_events(self, callback: Callable[[Dict], None]):
        """
        Subscribe to all Terminal 221b events
        
        This runs indefinitely, calling callback for each event.
        Run in a background task.
        """
        if not self.websocket:
            await self.connect_websocket()
        
        try:
            while True:
                response = await self.websocket.recv()
                data = json.loads(response)
                callback(data)
        except websockets.exceptions.ConnectionClosed:
            print("🔌 WebSocket connection closed")
    
    # ═══════════════════════════════════════════════════════════════════════
    # Event System
    # ═══════════════════════════════════════════════════════════════════════
    
    def on(self, event_type: str, handler: Callable):
        """Register event handler"""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)
    
    def emit(self, event_type: str, data: Dict):
        """Emit event to handlers"""
        for handler in self._event_handlers.get(event_type, []):
            try:
                handler(data)
            except Exception as e:
                print(f"Event handler error: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# High-Level Bridge (for TUI integration)
# ═══════════════════════════════════════════════════════════════════════════

class HiveTerminalBridge:
    """
    High-level bridge for TUI integration
    
    This provides a simple interface for the Hive TUI to use
    Terminal 221b capabilities.
    """
    
    def __init__(self, client: Optional[Terminal221bClient] = None):
        self.client = client or Terminal221bClient()
        self._connected = False
    
    async def connect(self):
        """Connect to Terminal 221b"""
        await self.client.connect()
        
        # Check health
        health = await self.client.health_check()
        self._connected = health.get("status") == "healthy"
        
        return self._connected
    
    async def ask_detective(self, query: str, personality: str = "holmes") -> str:
        """
        Simple interface: ask a detective, get answer
        
        This is designed to be called from TUI commands like:
            :investigate What is the balance of address X?
        """
        if not self._connected:
            await self.connect()
        
        try:
            result = await self.client.investigate(query, personality)
            
            if result.status == "completed":
                return f"🕵️ **{personality.title()}**: {result.result}"
            else:
                return f"❌ Investigation failed: {result.result}"
                
        except Exception as e:
            return f"❌ Error: {e}"
    
    async def switch_detective(self, personality: str) -> str:
        """Switch to a different detective personality"""
        detectives = await self.client.get_detectives()
        
        if personality.lower() in [d.lower() for d in detectives]:
            return f"🕵️ Switched to {personality.title()}"
        else:
            available = ", ".join(detectives)
            return f"❌ Unknown detective. Available: {available}"
    
    async def get_status(self) -> str:
        """Get Terminal 221b status for display"""
        try:
            health = await self.client.health_check()
            agents = health.get("agents_ready", 0)
            return f"🕵️ Terminal 221b: {health.get('status', 'unknown')} | {agents} detectives ready"
        except Exception as e:
            return f"🕵️ Terminal 221b: ❌ Offline ({e})"


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

async def demo():
    """Demonstrate Hive ⟷ Terminal 221b communication"""
    print("=" * 70)
    print("🐝 Hive 999 ⟷ 🕵️ Terminal 221b Communication Demo")
    print("=" * 70)
    
    # Create client
    client = Terminal221bClient()
    
    try:
        print("\n1️⃣  Connecting to Terminal 221b...")
        await client.connect()
        
        print("\n2️⃣  Health check...")
        health = await client.health_check()
        print(f"   Status: {health.get('status')}")
        print(f"   Agents ready: {health.get('agents_ready')}")
        
        print("\n3️⃣  Getting available detectives...")
        detectives = await client.get_detectives()
        print(f"   Available: {', '.join(detectives)}")
        
        print("\n4️⃣  Starting investigation...")
        result = await client.investigate(
            query="Analyze transaction patterns for address DemoAddress123",
            personality="holmes"
        )
        print(f"   Status: {result.status}")
        print(f"   Result preview: {result.result[:100]}..." if result.result else "   No result")
        
        print("\n5️⃣  Sending Hive message...")
        response = await client.send_hive_message(
            message_type="status_query",
            payload={}
        )
        print(f"   Response: {response}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure Terminal 221b API is running:")
        print("   python -m terminal_221b.api.server")
    
    finally:
        await client.close()
    
    print("\n" + "=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demo())
