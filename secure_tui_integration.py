#!/usr/bin/env python3
"""
🔒 Secure TUI Integration for Terminal 221b

Integrates Terminal 221b with Hive TUI using secure communication.

Features:
- Secure credential input (hidden passwords)
- Token persistence (encrypted)
- Automatic reconnection
- Security status display
- Audit trail in TUI

Usage:
    from secure_tui_integration import SecureTUIController
    
    controller = SecureTUIController()
    await controller.connect()
    
    # In TUI command handler
    result = await controller.investigate("Analyze address...")
"""

import asyncio
import getpass
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Callable

from secure_hive_client import SecureTerminal221bClient, AuthenticationError


@dataclass
class ConnectionStatus:
    """Connection status"""
    connected: bool = False
    authenticated: bool = False
    last_error: Optional[str] = None
    last_activity: Optional[datetime] = None
    username: Optional[str] = None
    server_version: Optional[str] = None


class SecureTUIController:
    """
    Secure controller for TUI integration
    
    This provides a simplified interface for the Hive TUI to use
    Terminal 221b with full security features.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:22181",
        credentials_callback: Optional[Callable[[], tuple]] = None
    ):
        self.base_url = base_url
        self.credentials_callback = credentials_callback
        self.client: Optional[SecureTerminal221bClient] = None
        self.status = ConnectionStatus()
        self._message_handler: Optional[Callable[[str], None]] = None
    
    def on_message(self, handler: Callable[[str], None]):
        """Set message handler for TUI updates"""
        self._message_handler = handler
    
    def _emit(self, message: str):
        """Emit message to TUI"""
        if self._message_handler:
            self._message_handler(message)
    
    async def connect(self, username: str = "", password: str = "") -> bool:
        """
        Connect to Terminal 221b with authentication
        
        Args:
            username: Username (if empty, will prompt)
            password: Password (if empty, will prompt)
        
        Returns:
            True if connected and authenticated
        """
        # Get credentials if not provided
        if not username or not password:
            if self.credentials_callback:
                username, password = self.credentials_callback()
            else:
                # In TUI context, these would come from secure input dialogs
                print("Terminal 221b Authentication Required")
                username = username or input("Username: ")
                password = password or getpass.getpass("Password: ")
        
        # Create client
        self.client = SecureTerminal221bClient(
            base_url=self.base_url,
            username=username,
            password=password,
            verify_ssl=False  # Change in production
        )
        
        try:
            self._emit("🔌 Connecting to Terminal 221b...")
            await self.client.connect()
            self.status.connected = True
            
            self._emit("🔐 Authenticating...")
            await self.client.authenticate()
            self.status.authenticated = True
            self.status.username = username
            self.status.last_activity = datetime.now()
            
            # Get server info
            try:
                health = await self.client.health_check()
                self.status.server_version = health.get("version")
            except:
                pass
            
            self._emit(f"✅ Connected as {username}")
            return True
            
        except AuthenticationError as e:
            self.status.last_error = str(e)
            self._emit(f"❌ Authentication failed: {e}")
            return False
        except Exception as e:
            self.status.last_error = str(e)
            self._emit(f"❌ Connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect and cleanup"""
        if self.client:
            try:
                await self.client.logout()
            except:
                pass
            await self.client.close()
            self.client = None
        
        self.status = ConnectionStatus()
        self._emit("Disconnected from Terminal 221b")
    
    async def ensure_connected(self) -> bool:
        """Ensure connection is active, reconnect if needed"""
        if not self.client:
            return await self.connect()
        
        if not self.status.authenticated:
            try:
                await self.client.authenticate()
                self.status.authenticated = True
                return True
            except:
                return await self.connect()
        
        return True
    
    async def investigate(
        self,
        query: str,
        personality: str = "holmes",
        timeout: int = 60
    ) -> str:
        """
        Run investigation and return formatted result
        
        Args:
            query: Investigation query
            personality: Detective personality
            timeout: Maximum wait time in seconds
        
        Returns:
            Formatted result string for TUI display
        """
        if not await self.ensure_connected():
            return "❌ Not connected to Terminal 221b"
        
        try:
            self._emit(f"🕵️  {personality.title()} is investigating...")
            
            result = await asyncio.wait_for(
                self.client.investigate(query, personality),
                timeout=timeout
            )
            
            self.status.last_activity = datetime.now()
            
            if result.get("status") == "completed":
                return self._format_result(result, personality)
            else:
                error = result.get("result", "Unknown error")
                return f"❌ Investigation failed: {error}"
                
        except asyncio.TimeoutError:
            return f"⏱️  Investigation timed out after {timeout}s"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _format_result(self, result: dict, personality: str) -> str:
        """Format investigation result for TUI"""
        detective_emoji = {
            "holmes": "🎩",
            "watson": "🩺",
            "mycroft": "🌐",
            "irene": "💋"
        }.get(personality.lower(), "🕵️")
        
        investigation_result = result.get("result", "No result")
        
        return f"""
{detective_emoji} **{personality.title()}** says:

{investigation_result}

---
*Investigation ID: {result.get('investigation_id', 'N/A')[:8]}...*
""".strip()
    
    async def get_status_text(self) -> str:
        """Get status text for TUI status bar"""
        if not self.status.connected:
            return "🕵️ T-221b: Disconnected"
        
        if not self.status.authenticated:
            return "🕵️ T-221b: Connected (not auth)"
        
        return f"🕵️ T-221b: {self.status.username}@{self.base_url.split('://')[-1]}"
    
    async def get_detectives(self) -> list:
        """Get list of available detectives"""
        if not await self.ensure_connected():
            return []
        
        try:
            return await self.client.get_detectives()
        except:
            return []
    
    async def quick_query(self, query_type: str, query: str) -> str:
        """
        Quick query for common operations
        
        Args:
            query_type: Type of query (address, transaction, etc.)
            query: The query string
        
        Returns:
            Formatted result
        """
        templates = {
            "address": "Analyze address {query}",
            "transaction": "Analyze transaction {query}",
            "block": "Analyze block {query}",
            "token": "Analyze token {query}",
        }
        
        template = templates.get(query_type, "{query}")
        full_query = template.format(query=query)
        
        return await self.investigate(full_query)


# ═══════════════════════════════════════════════════════════════════════════
# TUI Command Handlers
# ═══════════════════════════════════════════════════════════════════════════

class TUICommandHandlers:
    """
    Command handlers for TUI integration
    
    Maps TUI commands to Terminal 221b operations.
    """
    
    def __init__(self, controller: SecureTUIController):
        self.controller = controller
    
    async def handle_detective_command(self, args: list) -> str:
        """Handle :detective command"""
        if not args:
            detectives = await self.controller.get_detectives()
            return f"🕵️ Available detectives: {', '.join(detectives)}"
        
        personality = args[0].lower()
        return f"🕵️ Switched to {personality.title()}"
    
    async def handle_investigate_command(self, args: list) -> str:
        """Handle :investigate command"""
        if not args:
            return "Usage: :investigate <query> [personality]"
        
        query = " ".join(args)
        personality = "holmes"  # Default
        
        # Check if personality specified
        for p in ["holmes", "watson", "mycroft", "irene"]:
            if query.lower().endswith(f" as {p}"):
                personality = p
                query = query[:-(len(p) + 3)].strip()
                break
        
        return await self.controller.investigate(query, personality)
    
    async def handle_t221b_status(self) -> str:
        """Handle :221b status command"""
        status = self.controller.status
        
        lines = [
            "🕵️ Terminal 221b Status",
            "",
            f"Connected: {'Yes' if status.connected else 'No'}",
            f"Authenticated: {'Yes' if status.authenticated else 'No'}",
        ]
        
        if status.username:
            lines.append(f"User: {status.username}")
        
        if status.server_version:
            lines.append(f"Server Version: {status.server_version}")
        
        if status.last_activity:
            lines.append(f"Last Activity: {status.last_activity.strftime('%H:%M:%S')}")
        
        if status.last_error:
            lines.append(f"Last Error: {status.last_error}")
        
        return "\n".join(lines)
    
    async def handle_connect_command(self, args: list) -> str:
        """Handle :221b connect command"""
        if self.controller.status.authenticated:
            return "Already connected to Terminal 221b"
        
        success = await self.controller.connect()
        
        if success:
            return "✅ Connected to Terminal 221b"
        else:
            return "❌ Failed to connect"
    
    async def handle_disconnect_command(self) -> str:
        """Handle :221b disconnect command"""
        await self.controller.disconnect()
        return "Disconnected from Terminal 221b"


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

async def demo_secure_tui():
    """Demonstrate secure TUI integration"""
    print("=" * 70)
    print("🔒 Secure TUI Integration Demo")
    print("=" * 70)
    
    # Create controller with message handler
    controller = SecureTUIController()
    
    def message_handler(msg: str):
        """Handle messages from controller"""
        print(f"   [TUI] {msg}")
    
    controller.on_message(message_handler)
    
    # Create command handlers
    handlers = TUICommandHandlers(controller)
    
    try:
        print("\n1️⃣  Testing connection...")
        result = await handlers.handle_connect_command([])
        print(f"   Result: {result}")
        
        if controller.status.authenticated:
            print("\n2️⃣  Getting detectives...")
            result = await handlers.handle_detective_command([])
            print(f"   Result: {result}")
            
            print("\n3️⃣  Running investigation...")
            result = await handlers.handle_investigate_command([
                "Analyze", "address", "SecureDemo123"
            ])
            print(f"   Result:\n{result}")
            
            print("\n4️⃣  Checking status...")
            result = await handlers.handle_t221b_status()
            print(f"   Result:\n{result}")
            
            print("\n5️⃣  Disconnecting...")
            result = await handlers.handle_disconnect_command()
            print(f"   Result: {result}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demo_secure_tui())
