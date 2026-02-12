#!/usr/bin/env python3
"""
Baker Street Laboratory - Configuration Management System
Robust configuration management with validation and security

ASSIGNED TO: Qodo Configuration Management Agent
PRIORITY: 5.1 - Configuration Management System
TIMELINE: 2-3 days
DEPENDENCIES: None (can start immediately)
"""

import yaml
import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass, asdict
import logging
from cryptography.fernet import Fernet
import hashlib
import time

@dataclass
class ConfigurationSchema:
    """Schema definition for Baker Street Laboratory configuration"""
    breakthrough_capabilities: Dict[str, Any]
    polymorphic_framework: Dict[str, Any]
    collaborative_intelligence: Dict[str, Any]
    creative_scientific_synthesis: Dict[str, Any]
    performance_targets: Dict[str, Any]
    ai_models: Dict[str, Any]
    hardware_allocation: Dict[str, Any]
    security_settings: Dict[str, Any]

class ConfigurationValidator:
    """
    Robust configuration management with validation
    
    FEATURES:
    - YAML configuration validation with schema checking
    - Environment variable management with encryption
    - Hot-reload configuration without system restart
    - Configuration versioning and rollback
    - Security audit and validation
    """
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.logger = logging.getLogger(__name__)
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.config_cache = {}
        self.config_watchers = []
    
    def _get_or_create_encryption_key(self) -> bytes:
        """
        Get or create encryption key for sensitive configuration data
        
        TODO for Qodo Agent: Implement secure key management
        - Generate encryption key if not exists
        - Store key securely (not in code)
        - Implement key rotation mechanism
        - Add key backup and recovery
        """
        key_file = Path(".config_key")
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            # TODO: Implement secure key storage
            # For now, storing in file (NOT SECURE for production)
            key_file.write_bytes(key)
            return key
    
    def validate_yaml_configs(self, config_path: Optional[str] = None) -> Dict[str, bool]:
        """
        Validate all YAML configuration files
        
        Args:
            config_path: Specific config file to validate, or None for all configs
            
        Returns:
            Dictionary mapping config files to validation status
            
        TODO for Qodo Agent: Implement comprehensive YAML validation
        - Schema validation against ConfigurationSchema
        - Cross-reference validation between configs
        - Dependency validation
        - Performance impact analysis
        """
        validation_results = {}
        
        if config_path:
            config_files = [Path(config_path)]
        else:
            config_files = list(self.config_dir.glob("**/*.yaml")) + list(self.config_dir.glob("**/*.yml"))
        
        for config_file in config_files:
            try:
                validation_results[str(config_file)] = self._validate_single_config(config_file)
            except Exception as e:
                self.logger.error(f"Error validating {config_file}: {e}")
                validation_results[str(config_file)] = False
        
        return validation_results
    
    def _validate_single_config(self, config_file: Path) -> bool:
        """
        Validate a single configuration file
        
        TODO for Qodo Agent: Implement detailed validation logic
        - YAML syntax validation
        - Schema compliance checking
        - Value range validation
        - Required field verification
        """
        try:
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            
            # TODO: Implement schema validation
            # if config_file.name == "breakthrough_config.yaml":
            #     return self._validate_breakthrough_config(config_data)
            # elif config_file.name == "ollama-models.yaml":
            #     return self._validate_models_config(config_data)
            
            # Basic validation for now
            return isinstance(config_data, dict) and len(config_data) > 0
            
        except yaml.YAMLError as e:
            self.logger.error(f"YAML syntax error in {config_file}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Validation error in {config_file}: {e}")
            return False
    
    def manage_environment_variables(self) -> Dict[str, str]:
        """
        Secure environment variable management
        
        Returns:
            Dictionary of managed environment variables (non-sensitive values only)
            
        TODO for Qodo Agent: Implement secure environment management
        - Encrypt sensitive environment variables
        - Validate environment variable formats
        - Implement environment variable templates
        - Add environment variable auditing
        """
        managed_vars = {}
        
        # Define required environment variables
        required_vars = [
            "BAKER_STREET_API_KEY",
            "OLLAMA_HOST",
            "OPENAI_API_KEY",
            "PERPLEXITY_API_KEY"
        ]
        
        # Define optional environment variables with defaults
        optional_vars = {
            "BAKER_STREET_LOG_LEVEL": "INFO",
            "BAKER_STREET_MAX_WORKERS": "4",
            "BAKER_STREET_CACHE_SIZE": "1000"
        }
        
        # TODO: Implement secure variable management
        for var in required_vars:
            value = os.getenv(var)
            if value:
                # Store encrypted version for sensitive data
                if "API_KEY" in var:
                    managed_vars[var] = "[ENCRYPTED]"
                else:
                    managed_vars[var] = value
            else:
                self.logger.warning(f"Required environment variable {var} not set")
        
        for var, default in optional_vars.items():
            managed_vars[var] = os.getenv(var, default)
        
        return managed_vars
    
    def dynamic_config_updates(self, new_config: Dict[str, Any], 
                             config_file: str = "breakthrough_config.yaml") -> bool:
        """
        Hot-reload configuration without system restart
        
        Args:
            new_config: New configuration data
            config_file: Configuration file to update
            
        Returns:
            True if update successful, False otherwise
            
        TODO for Qodo Agent: Implement hot-reload mechanism
        - Validate new configuration before applying
        - Create configuration backup before update
        - Implement rollback mechanism on failure
        - Notify configuration watchers of changes
        - Test configuration compatibility
        """
        try:
            config_path = self.config_dir / config_file
            
            # TODO: Implement comprehensive update logic
            # 1. Validate new configuration
            # 2. Create backup of current configuration
            # 3. Apply new configuration
            # 4. Test system with new configuration
            # 5. Rollback if issues detected
            # 6. Notify watchers of successful update
            
            # Basic implementation for now
            with open(config_path, 'w') as f:
                yaml.dump(new_config, f, default_flow_style=False)
            
            # Update cache
            self.config_cache[config_file] = new_config
            
            # Notify watchers
            self._notify_config_watchers(config_file, new_config)
            
            self.logger.info(f"Successfully updated configuration: {config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update configuration {config_file}: {e}")
            return False
    
    def _notify_config_watchers(self, config_file: str, new_config: Dict[str, Any]):
        """
        Notify registered watchers of configuration changes
        
        TODO for Qodo Agent: Implement watcher notification system
        """
        for watcher in self.config_watchers:
            try:
                watcher(config_file, new_config)
            except Exception as e:
                self.logger.error(f"Error notifying config watcher: {e}")
    
    def register_config_watcher(self, callback):
        """Register a callback for configuration changes"""
        self.config_watchers.append(callback)
    
    def get_config(self, config_file: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration with caching
        
        TODO for Qodo Agent: Implement intelligent caching
        - Cache frequently accessed configurations
        - Implement cache invalidation
        - Add cache statistics and monitoring
        """
        if config_file in self.config_cache:
            return self.config_cache[config_file]
        
        config_path = self.config_dir / config_file
        if not config_path.exists():
            return None
        
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            
            self.config_cache[config_file] = config_data
            return config_data
            
        except Exception as e:
            self.logger.error(f"Error loading configuration {config_file}: {e}")
            return None
    
    def create_config_backup(self, config_file: str) -> str:
        """
        Create backup of configuration file
        
        Returns:
            Path to backup file
            
        TODO for Qodo Agent: Implement comprehensive backup system
        - Versioned backups with timestamps
        - Compressed backup storage
        - Automatic cleanup of old backups
        - Backup integrity verification
        """
        config_path = self.config_dir / config_file
        timestamp = int(time.time())
        backup_path = self.config_dir / "backups" / f"{config_file}.{timestamp}.backup"
        
        # Create backups directory if not exists
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            import shutil
            shutil.copy2(config_path, backup_path)
            self.logger.info(f"Created backup: {backup_path}")
            return str(backup_path)
        except Exception as e:
            self.logger.error(f"Failed to create backup for {config_file}: {e}")
            raise
    
    def restore_config_backup(self, backup_path: str, config_file: str) -> bool:
        """
        Restore configuration from backup
        
        TODO for Qodo Agent: Implement backup restoration
        - Validate backup integrity
        - Test restored configuration
        - Create rollback point before restoration
        """
        try:
            import shutil
            config_path = self.config_dir / config_file
            shutil.copy2(backup_path, config_path)
            
            # Clear cache
            if config_file in self.config_cache:
                del self.config_cache[config_file]
            
            self.logger.info(f"Restored configuration from backup: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore backup {backup_path}: {e}")
            return False
    
    def audit_configuration_security(self) -> Dict[str, Any]:
        """
        Audit configuration for security issues
        
        Returns:
            Dictionary containing security audit results
            
        TODO for Qodo Agent: Implement comprehensive security audit
        - Check for hardcoded secrets
        - Validate file permissions
        - Check for insecure configurations
        - Audit encryption usage
        - Generate security recommendations
        """
        audit_results = {
            "timestamp": time.time(),
            "security_issues": [],
            "recommendations": [],
            "overall_score": 0.0
        }
        
        # TODO: Implement comprehensive security audit
        # Check for common security issues:
        # - Hardcoded API keys or passwords
        # - Insecure file permissions
        # - Unencrypted sensitive data
        # - Weak encryption settings
        # - Missing security headers
        
        # Placeholder implementation
        audit_results["overall_score"] = 85.0  # Example score
        audit_results["recommendations"] = [
            "Implement proper key rotation mechanism",
            "Add configuration file integrity checking",
            "Enable audit logging for configuration changes"
        ]
        
        return audit_results

# Example usage and testing
def main():
    """
    Example usage of configuration management system
    
    TODO for Qodo Agent: Implement comprehensive testing examples
    """
    config_manager = ConfigurationValidator()
    
    # Test configuration validation
    print("🔧 Baker Street Laboratory - Configuration Management System")
    print("=" * 60)
    
    validation_results = config_manager.validate_yaml_configs()
    print(f"Configuration validation results: {validation_results}")
    
    # Test environment variable management
    env_vars = config_manager.manage_environment_variables()
    print(f"Managed environment variables: {len(env_vars)}")
    
    # Test security audit
    security_audit = config_manager.audit_configuration_security()
    print(f"Security audit score: {security_audit['overall_score']}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
