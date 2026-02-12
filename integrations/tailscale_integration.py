"""
Tailscale Integration for BeeAI Hive 999

Provides secure networking for the Hive using Tailscale.
- Auto-connect to Tailscale network on startup
- Secure communication between Hive agents
- Access control list (ACL) configuration
- Network policy management

"Secure communication for distributed bee colonies"
"""

import subprocess
import os
import sys
import time
from typing import Optional

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TAILSCALE_CONFIG = os.path.join(PROJECT_ROOT, "config", "tailscale.conf")


class TailscaleManager:
    """Manage Tailscale integration for the Hive."""

    def __init__(self):
        self.connected = False
        self.ip_address = None
        self.status = "disconnected"

    def is_available(self) -> bool:
        """Check if Tailscale is available."""
        try:
            result = subprocess.run(
                ["which", "tailscale"], capture_output=True, text=True
            )
            return result.returncode == 0
        except:
            return False

    def connect(self, auth_key: str = None, hostname: str = "beeai-hive") -> bool:
        """
        Connect to Tailscale network.

        Args:
            auth_key: Tailscale auth key (from https://login.tailscale.com/admin/settings/keys)
            hostname: Custom hostname for the Hive

        Returns:
            True if connection successful, False otherwise
        """
        if not self.is_available():
            self.status = "tailscale_unavailable"
            return False

        try:
            # Check if already connected
            result = subprocess.run(
                ["tailscale", "status"], capture_output=True, text=True
            )

            if "Stopped" in result.stdout or result.returncode != 0:
                # Start Tailscale daemon
                subprocess.run(["sudo", "systemctl", "start", "tailscaled"], check=True)
                time.sleep(1)

            if "Connected" not in result.stdout:
                connect_cmd = ["tailscale", "up", "--hostname", hostname]
                if auth_key:
                    connect_cmd.extend(["--authkey", auth_key])

                subprocess.run(connect_cmd, check=True)
                time.sleep(2)

            # Verify connection
            result = subprocess.run(
                ["tailscale", "status"], capture_output=True, text=True
            )

            if "Connected" in result.stdout:
                self.connected = True
                # Get IP address
                ip_result = subprocess.run(
                    ["tailscale", "ip"], capture_output=True, text=True
                )
                self.ip_address = ip_result.stdout.strip()
                self.status = "connected"
                return True
            else:
                self.status = "connection_failed"
                return False

        except Exception as e:
            self.status = f"error: {str(e)}"
            return False

    def disconnect(self) -> bool:
        """Disconnect from Tailscale network."""
        if not self.is_available():
            return False

        try:
            subprocess.run(["tailscale", "down"], check=True)
            self.connected = False
            self.ip_address = None
            self.status = "disconnected"
            return True
        except Exception as e:
            self.status = f"error: {str(e)}"
            return False

    def get_status(self) -> dict:
        """Get detailed Tailscale status."""
        if not self.is_available():
            return {
                "available": False,
                "connected": False,
                "status": "tailscale_unavailable",
            }

        try:
            result = subprocess.run(
                ["tailscale", "status"], capture_output=True, text=True
            )

            return {
                "available": True,
                "connected": self.connected,
                "status": self.status,
                "ip_address": self.ip_address,
                "raw_status": result.stdout if self.connected else "Not connected",
            }
        except Exception as e:
            return {"available": True, "connected": False, "status": f"error: {str(e)}"}

    def share_node(self, duration: int = 30) -> str:
        """
        Share this node for remote access.

        Args:
            duration: Duration in minutes

        Returns:
            Shareable URL or error message
        """
        if not self.connected:
            return "Not connected to Tailscale"

        try:
            result = subprocess.run(
                ["tailscale", "ssh", "--share", f"{duration}m"],
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error sharing node: {str(e)}"


def load_tailscale_config() -> dict:
    """Load Tailscale configuration from file."""
    config = {
        "enabled": False,
        "auth_key": None,
        "hostname": "beeai-hive",
        "acl": {
            "allow": [
                {"src": "autogroup:admin", "dst": "tag:hive:*:*"},
                {"src": "tag:hive:worker", "dst": "tag:hive:worker:*"},
                {"src": "tag:hive:queen", "dst": "tag:hive:*:*"},
            ]
        },
    }

    if os.path.exists(TAILSCALE_CONFIG):
        try:
            import yaml

            with open(TAILSCALE_CONFIG, "r") as f:
                config.update(yaml.safe_load(f))
        except Exception as e:
            print(f"Warning: Failed to load Tailscale config: {e}")

    return config


# Global Tailscale manager instance
_tailscale_manager = TailscaleManager()


def get_tailscale_manager() -> TailscaleManager:
    """Get the global Tailscale manager instance."""
    return _tailscale_manager


def initialize_tailscale() -> bool:
    """Initialize Tailscale connection from config file."""
    config = load_tailscale_config()

    if not config.get("enabled", False):
        return False

    print("🔒 Connecting to Tailscale network...")

    manager = get_tailscale_manager()
    auth_key = config.get("auth_key")
    hostname = config.get("hostname", "beeai-hive")

    if manager.connect(auth_key, hostname):
        status = manager.get_status()
        print(f"✅ Tailscale connected: {status['ip_address']}")
        return True
    else:
        print(f"❌ Tailscale connection failed: {manager.status}")
        return False


if __name__ == "__main__":
    # Quick test
    if len(sys.argv) > 1:
        if sys.argv[1] == "connect":
            auth_key = sys.argv[2] if len(sys.argv) > 2 else None
            hostname = sys.argv[3] if len(sys.argv) > 3 else "beeai-hive"
            success = _tailscale_manager.connect(auth_key, hostname)
            print("Connected successfully!" if success else "Connection failed")

        elif sys.argv[1] == "status":
            status = _tailscale_manager.get_status()
            print(f"Status: {status['status']}")
            if status["connected"]:
                print(f"IP: {status['ip_address']}")

        elif sys.argv[1] == "share":
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            print(_tailscale_manager.share_node(duration))

        elif sys.argv[1] == "disconnect":
            _tailscale_manager.disconnect()
            print("Disconnected")

        else:
            print(
                "Usage: python tailscale_integration.py [connect|status|share|disconnect]"
            )
    else:
        print("Tailscale Integration for BeeAI Hive 999")
        print("-" * 50)
        status = _tailscale_manager.get_status()
        print(f"Available: {status['available']}")
        print(f"Connected: {status['connected']}")
        if status["connected"]:
            print(f"IP Address: {status['ip_address']}")
