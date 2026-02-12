"""
Supabase Vault Python Interface

Provides programmatic access to Supabase Vault for secrets management.
"""

import os
import json
import subprocess
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Secret:
    """Represents a secret in Supabase Vault."""
    name: str
    value: str
    description: str = ""
    created_at: Optional[str] = None


class SupabaseVault:
    """
    Interface to Supabase Vault for secrets management.
    
    Usage:
        vault = SupabaseVault()
        
        # Add secret
        vault.add_secret("OPENAI_API_KEY", "sk-...", "OpenAI API key")
        
        # Get secret
        secret = vault.get_secret("OPENAI_API_KEY")
        
        # List secrets
        secrets = vault.list_secrets()
    """
    
    def __init__(self, project_dir: str = None):
        self.project_dir = project_dir or os.path.expanduser("~/beeai-hive-999")
        self._vault_available = None
        self._env_file = os.path.expanduser("~/.env")
    
    def _run_sql(self, sql: str) -> Tuple[bool, str]:
        """Execute SQL via Supabase CLI."""
        try:
            result = subprocess.run(
                ["supabase", "db", "execute", sql],
                capture_output=True,
                text=True,
                cwd=self.project_dir
            )
            return result.returncode == 0, result.stdout
        except FileNotFoundError:
            return False, "Supabase CLI not found"
    
    def is_vault_available(self) -> bool:
        """Check if Supabase Vault is available."""
        if self._vault_available is not None:
            return self._vault_available
        
        # Check if supabase is initialized
        config_path = Path(self.project_dir) / "supabase" / "config.toml"
        if not config_path.exists():
            self._vault_available = False
            return False
        
        # Try to query vault
        success, _ = self._run_sql("SELECT 1 FROM vault.secrets LIMIT 1;")
        self._vault_available = success
        return success
    
    def init_vault(self) -> bool:
        """Initialize Vault extension."""
        sql = "CREATE EXTENSION IF NOT EXISTS vault WITH SCHEMA vault;"
        success, _ = self._run_sql(sql)
        if success:
            self._vault_available = True
        return success
    
    def add_secret(self, name: str, value: str, description: str = "") -> bool:
        """
        Add a secret to Vault (and .env as backup).
        
        Args:
            name: Secret name
            value: Secret value
            description: Optional description
        
        Returns:
            True if successful
        """
        # Try Vault first
        if self.is_vault_available():
            # Escape single quotes
            escaped_value = value.replace("'", "''")
            sql = f"""
            DELETE FROM vault.secrets WHERE name = '{name}';
            INSERT INTO vault.secrets (name, secret, description)
            VALUES ('{name}', '{escaped_value}', '{description}');
            """
            success, _ = self._run_sql(sql)
            if success:
                # Also update .env
                self._add_to_env(name, value)
                return True
        
        # Fall back to .env only
        return self._add_to_env(name, value)
    
    def _add_to_env(self, name: str, value: str) -> bool:
        """Add secret to .env file."""
        env_path = Path(self._env_file)
        
        # Read existing content
        lines = []
        if env_path.exists():
            with open(env_path) as f:
                lines = f.readlines()
        
        # Remove existing entry
        lines = [l for l in lines if not l.startswith(f"export {name}=")]
        
        # Add new entry
        lines.append(f"export {name}={value}\n")
        
        # Write back
        with open(env_path, "w") as f:
            f.writelines(lines)
        
        return True
    
    def get_secret(self, name: str) -> Optional[str]:
        """
        Get a secret value.
        
        Tries Vault first, then .env file.
        """
        # Try Vault first
        if self.is_vault_available():
            sql = f"SELECT secret FROM vault.secrets WHERE name = '{name}';"
            success, output = self._run_sql(sql)
            if success and output.strip():
                # Parse output (usually contains the value)
                lines = output.strip().split('\n')
                for line in lines:
                    if line and not line.startswith('-') and not line.startswith('('):
                        return line.strip()
        
        # Fall back to .env
        return self._get_from_env(name)
    
    def _get_from_env(self, name: str) -> Optional[str]:
        """Get secret from .env file."""
        env_path = Path(self._env_file)
        if not env_path.exists():
            return None
        
        with open(env_path) as f:
            for line in f:
                if line.startswith(f"export {name}="):
                    return line.split('=', 1)[1].strip()
        
        return None
    
    def list_secrets(self) -> List[Dict[str, str]]:
        """List all secrets (names only for security)."""
        secrets = []
        
        # Try Vault
        if self.is_vault_available():
            sql = "SELECT name, description, created_at FROM vault.secrets;"
            success, output = self._run_sql(sql)
            if success:
                # Parse output (this is simplified)
                lines = output.strip().split('\n')
                for line in lines[2:]:  # Skip header lines
                    if line and not line.startswith('-'):
                        parts = line.split('|')
                        if len(parts) >= 3:
                            secrets.append({
                                "name": parts[0].strip(),
                                "description": parts[1].strip(),
                                "created_at": parts[2].strip(),
                                "source": "Vault"
                            })
        
        # Also check .env
        env_path = Path(self._env_file)
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if line.startswith("export "):
                        name = line[7:].split('=', 1)[0]
                        # Skip if already in Vault list
                        if not any(s["name"] == name for s in secrets):
                            secrets.append({
                                "name": name,
                                "description": "From .env",
                                "source": ".env"
                            })
        
        return secrets
    
    def delete_secret(self, name: str) -> bool:
        """Delete a secret from Vault and .env."""
        success = True
        
        # Delete from Vault
        if self.is_vault_available():
            sql = f"DELETE FROM vault.secrets WHERE name = '{name}';"
            vault_success, _ = self._run_sql(sql)
            success = success and vault_success
        
        # Delete from .env
        env_path = Path(self._env_file)
        if env_path.exists():
            with open(env_path) as f:
                lines = f.readlines()
            
            lines = [l for l in lines if not l.startswith(f"export {name}=")]
            
            with open(env_path, "w") as f:
                f.writelines(lines)
        
        return success
    
    def load_to_env(self) -> Dict[str, str]:
        """Load all secrets to environment variables."""
        secrets = {}
        
        # Load from .env
        env_path = Path(self._env_file)
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if line.startswith("export "):
                        parts = line[7:].strip().split('=', 1)
                        if len(parts) == 2:
                            name, value = parts
                            os.environ[name] = value
                            secrets[name] = value
        
        return secrets


# Convenience functions
def get_vault() -> SupabaseVault:
    """Get default vault instance."""
    return SupabaseVault()


def add_secret(name: str, value: str, description: str = "") -> bool:
    """Quick function to add a secret."""
    return get_vault().add_secret(name, value, description)


def get_secret(name: str) -> Optional[str]:
    """Quick function to get a secret."""
    return get_vault().get_secret(name)


def list_secrets() -> List[Dict[str, str]]:
    """Quick function to list secrets."""
    return get_vault().list_secrets()


if __name__ == "__main__":
    # Test the vault
    vault = SupabaseVault()
    
    print("Supabase Vault Interface Test")
    print("=" * 50)
    print(f"Project dir: {vault.project_dir}")
    print(f"Vault available: {vault.is_vault_available()}")
    print(f".env file: {vault._env_file}")
    print("")
    
    print("Secrets:")
    for secret in vault.list_secrets():
        print(f"  - {secret['name']} ({secret.get('source', 'unknown')})")
