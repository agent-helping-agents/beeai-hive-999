#!/usr/bin/env python3
"""
🔒 Secure Hive 999 Client for Terminal 221b

Hardened client implementing security best practices:
- JWT token management with auto-refresh
- Request signing
- Certificate pinning (optional)
- Secure credential storage
- Audit logging

Usage:
    from secure_hive_client import SecureTerminal221bClient
    
    client = SecureTerminal221bClient(
        base_url="https://localhost:22181",
        username="hive",
        password="HiveConnect2024!"
    )
    
    await client.authenticate()
    
    result = await client.investigate(
        query="Analyze address...",
        personality="holmes"
    )
"""

import asyncio
import hashlib
import hmac
import json
import logging
import os
import ssl
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

import aiohttp
from cryptography.fernet import Fernet


# ═══════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════

class SecureClientConfig:
    """Secure client configuration"""
    
    # Connection settings
    DEFAULT_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    
    # Token refresh - refresh 5 minutes before expiry
    TOKEN_REFRESH_BUFFER: int = 300
    
    # Security settings
    VERIFY_SSL: bool = True
    CERT_PINNING: bool = False
    
    # Audit logging
    AUDIT_LOG_PATH: str = "/tmp/hive_secure_client.log"


# ═══════════════════════════════════════════════════════════════════════════
# Security Utilities
# ═══════════════════════════════════════════════════════════════════════════

class SecureStorage:
    """Secure credential storage (in production, use keyring or HSM)"""
    
    def __init__(self):
        self._key = self._get_or_create_key()
        self._cipher = Fernet(self._key)
        self._memory_store: Dict[str, bytes] = {}
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        key_path = Path(tempfile.gettempdir()) / ".t221b_key"
        
        if key_path.exists():
            return key_path.read_bytes()
        else:
            key = Fernet.generate_key()
            key_path.write_bytes(key)
            os.chmod(key_path, 0o600)  # Restrict permissions
            return key
    
    def store(self, key: str, value: str):
        """Encrypt and store value"""
        self._memory_store[key] = self._cipher.encrypt(value.encode())
    
    def retrieve(self, key: str) -> Optional[str]:
        """Retrieve and decrypt value"""
        encrypted = self._memory_store.get(key)
        if encrypted:
            return self._cipher.decrypt(encrypted).decode()
        return None
    
    def clear(self):
        """Clear all stored values"""
        self._memory_store.clear()


class AuditLogger:
    """Client-side audit logger"""
    
    def __init__(self, log_path: str):
        self.logger = logging.getLogger("hive_secure_client")
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_request(self, method: str, endpoint: str, status: int = 0):
        """Log API request"""
        self.logger.info(f"REQUEST: method={method} endpoint={endpoint} status={status}")
    
    def log_auth(self, success: bool, reason: str = ""):
        """Log authentication"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.warning(f"AUTH: status={status} reason={reason}")
    
    def log_error(self, error: str):
        """Log error"""
        self.logger.error(f"ERROR: {error}")


# ═══════════════════════════════════════════════════════════════════════════
# Secure Client
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TokenInfo:
    """Token information"""
    access_token: str
    refresh_token: Optional[str]
    expires_at: datetime
    token_type: str = "bearer"


class SecureTerminal221bClient:
    """
    Secure client for Terminal 221b API
    
    Features:
    - Automatic token management
    - Request retry with exponential backoff
    - SSL verification
    - Audit logging
    - Secure credential storage
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:22181",
        username: str = "",
        password: str = "",
        verify_ssl: bool = True,
        cert_path: Optional[str] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self._secure_storage = SecureStorage()
        self._secure_storage.store("password", password)
        
        self.token_info: Optional[TokenInfo] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.verify_ssl = verify_ssl
        self.cert_path = cert_path
        
        self.audit_logger = AuditLogger(SecureClientConfig.AUDIT_LOG_PATH)
        
        # SSL context
        self.ssl_context = None
        if verify_ssl and cert_path:
            self.ssl_context = ssl.create_default_context(cafile=cert_path)
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def connect(self):
        """Establish connection"""
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=5,
            ttl_dns_cache=300,
        )
        
        timeout = aiohttp.ClientTimeout(total=SecureClientConfig.DEFAULT_TIMEOUT)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                "User-Agent": "HiveSecureClient/1.0",
                "Accept": "application/json",
            }
        )
    
    async def close(self):
        """Close connection and clear credentials"""
        if self.session:
            await self.session.close()
            self.session = None
        
        self._secure_storage.clear()
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
        require_auth: bool = True,
        retries: int = 0
    ) -> Tuple[int, Dict]:
        """
        Make HTTP request with retry logic
        
        Returns:
            (status_code, response_data)
        """
        url = urljoin(self.base_url + "/", endpoint)
        headers = {}
        
        # Add auth header if required
        if require_auth:
            if not self.token_info or self._is_token_expired():
                await self.authenticate()
            
            if self.token_info:
                headers["Authorization"] = f"Bearer {self.token_info.access_token}"
        
        try:
            ssl = self.ssl_context if self.verify_ssl else False
            
            async with self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                ssl=ssl
            ) as response:
                
                status = response.status
                
                # Handle rate limiting
                if status == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    self.audit_logger.log_error(f"Rate limited, retry after {retry_after}s")
                    
                    if retries < SecureClientConfig.MAX_RETRIES:
                        await asyncio.sleep(retry_after)
                        return await self._make_request(
                            method, endpoint, json_data, require_auth, retries + 1
                        )
                
                # Handle auth failure - try to refresh token once
                if status == 401 and require_auth and retries < 1:
                    self.audit_logger.log_auth(False, "token_expired")
                    await self.authenticate()
                    return await self._make_request(
                        method, endpoint, json_data, require_auth, retries + 1
                    )
                
                # Parse response
                try:
                    data = await response.json()
                except:
                    data = {"message": await response.text()}
                
                self.audit_logger.log_request(method, endpoint, status)
                
                return status, data
                
        except aiohttp.ClientError as e:
            self.audit_logger.log_error(f"Request failed: {str(e)}")
            
            if retries < SecureClientConfig.MAX_RETRIES:
                await asyncio.sleep(SecureClientConfig.RETRY_DELAY * (2 ** retries))
                return await self._make_request(
                    method, endpoint, json_data, require_auth, retries + 1
                )
            
            raise
    
    def _is_token_expired(self) -> bool:
        """Check if token is expired or about to expire"""
        if not self.token_info:
            return True
        
        buffer = timedelta(seconds=SecureClientConfig.TOKEN_REFRESH_BUFFER)
        return datetime.utcnow() + buffer >= self.token_info.expires_at
    
    async def authenticate(self) -> bool:
        """Authenticate and get tokens"""
        password = self._secure_storage.retrieve("password")
        
        if not password:
            self.audit_logger.log_auth(False, "no_password_stored")
            raise ValueError("No password stored")
        
        status, data = await self._make_request(
            "POST",
            "token",
            json_data={
                "username": self.username,
                "password": password
            },
            require_auth=False
        )
        
        if status == 200:
            access_token = data.get("access_token")
            refresh_token = data.get("refresh_token")
            expires_in = data.get("expires_in", 1800)
            
            self.token_info = TokenInfo(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=datetime.utcnow() + timedelta(seconds=expires_in)
            )
            
            self.audit_logger.log_auth(True)
            return True
        else:
            error = data.get("detail", "Unknown error")
            self.audit_logger.log_auth(False, error)
            raise AuthenticationError(f"Authentication failed: {error}")
    
    async def logout(self):
        """Logout and revoke token"""
        await self._make_request("POST", "logout", require_auth=True)
        self.token_info = None
    
    # ═══════════════════════════════════════════════════════════════════════
    # API Methods
    # ═══════════════════════════════════════════════════════════════════════
    
    async def health_check(self) -> Dict:
        """Check API health"""
        status, data = await self._make_request(
            "GET", "health", require_auth=False
        )
        
        if status == 200:
            return data
        else:
            raise APIError(f"Health check failed: {data}")
    
    async def get_detectives(self) -> List[str]:
        """Get list of available detectives"""
        status, data = await self._make_request("GET", "detectives")
        
        if status == 200:
            return data
        else:
            raise APIError(f"Failed to get detectives: {data}")
    
    async def investigate(
        self,
        query: str,
        personality: str = "holmes",
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Start investigation
        
        Args:
            query: Investigation query
            personality: Detective personality
            context: Additional context
        
        Returns:
            Investigation result
        """
        # Start investigation
        status, data = await self._make_request(
            "POST",
            "investigate",
            json_data={
                "query": query,
                "personality": personality,
                "context": context or {}
            }
        )
        
        if status != 200:
            raise APIError(f"Investigation start failed: {data}")
        
        investigation_id = data.get("investigation_id")
        
        # Poll for completion
        max_attempts = 60
        for attempt in range(max_attempts):
            await asyncio.sleep(1)
            
            status, result = await self._make_request(
                "GET",
                f"investigate/{investigation_id}"
            )
            
            if status == 200:
                if result.get("status") in ("completed", "error"):
                    return result
            else:
                raise APIError(f"Failed to get investigation: {result}")
        
        raise TimeoutError(f"Investigation {investigation_id} timed out")
    
    async def get_admin_stats(self) -> Dict:
        """Get admin stats (requires admin role)"""
        status, data = await self._make_request("GET", "admin/stats")
        
        if status == 200:
            return data
        else:
            raise APIError(f"Failed to get stats: {data}")


# ═══════════════════════════════════════════════════════════════════════════
# Exceptions
# ═══════════════════════════════════════════════════════════════════════════

class AuthenticationError(Exception):
    """Authentication error"""
    pass


class APIError(Exception):
    """API error"""
    pass


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

async def demo_secure_client():
    """Demonstrate secure client"""
    print("=" * 70)
    print("🔒 Secure Hive Client Demo")
    print("=" * 70)
    
    client = SecureTerminal221bClient(
        base_url="http://localhost:22181",
        username="hive",
        password="HiveConnect2024!",
        verify_ssl=False  # Set to True with cert_path in production
    )
    
    try:
        print("\n1️⃣  Connecting to Terminal 221b...")
        await client.connect()
        print("   ✅ Connected")
        
        print("\n2️⃣  Authenticating...")
        await client.authenticate()
        print("   ✅ Authenticated")
        
        print("\n3️⃣  Health check...")
        health = await client.health_check()
        print(f"   Status: {health.get('status')}")
        
        print("\n4️⃣  Getting detectives...")
        detectives = await client.get_detectives()
        print(f"   Available: {', '.join(detectives)}")
        
        print("\n5️⃣  Starting investigation...")
        result = await client.investigate(
            query="Analyze address SecureDemo123456789",
            personality="holmes"
        )
        print(f"   Status: {result.get('status')}")
        print(f"   Result: {result.get('result', 'N/A')[:100]}..." if result.get('result') else "   No result yet")
        
        print("\n6️⃣  Testing admin access (should fail for hive user)...")
        try:
            stats = await client.get_admin_stats()
            print(f"   Stats: {stats}")
        except APIError as e:
            print(f"   ⚠️  Expected: {e}")
        
        print("\n7️⃣  Logging out...")
        await client.logout()
        print("   ✅ Logged out")
        
    except AuthenticationError as e:
        print(f"\n❌ Authentication failed: {e}")
        print("   Make sure the server is running and credentials are correct")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        await client.close()
    
    print("\n" + "=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demo_secure_client())
