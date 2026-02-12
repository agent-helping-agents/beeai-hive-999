"""
Baker Street Laboratory - Environment Utilities
Environment validation and system checks.
"""

import os
import sqlite3
from pathlib import Path
from typing import Dict, Any


def check_environment() -> Dict[str, Any]:
    """
    Check the Baker Street Laboratory environment for completeness.
    
    Returns:
        Dict containing validation results
    """
    results = {
        'valid': True,
        'message': '',
        'checks': {}
    }
    
    # Check Python version
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    results['checks']['python_version'] = python_version
    
    # Check virtual environment
    venv_active = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    results['checks']['virtual_env'] = venv_active
    
    # Check .env file
    env_file_exists = os.path.exists('.env')
    results['checks']['env_file'] = env_file_exists
    
    # Check configuration file
    config_file_exists = os.path.exists('config/agents.yaml')
    results['checks']['config_file'] = config_file_exists
    
    # Check database
    db_path = 'data/metadata.db'
    db_exists = os.path.exists(db_path)
    db_valid = False
    
    if db_exists:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM system_config")
            cursor.fetchone()
            conn.close()
            db_valid = True
        except Exception:
            db_valid = False
    
    results['checks']['database_exists'] = db_exists
    results['checks']['database_valid'] = db_valid
    
    # Check required directories
    required_dirs = [
        'research', 'implementation', 'optimization', 'config', 'data'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    results['checks']['directories'] = len(missing_dirs) == 0
    results['checks']['missing_directories'] = missing_dirs
    
    # Check API keys (basic check)
    api_keys_configured = False
    if env_file_exists:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            # Check for at least one AI API key
            openai_key = os.getenv('OPENAI_API_KEY')
            anthropic_key = os.getenv('ANTHROPIC_API_KEY')
            
            api_keys_configured = bool(openai_key or anthropic_key)
        except Exception:
            pass
    
    results['checks']['api_keys'] = api_keys_configured
    
    # Determine overall validity
    critical_checks = [
        venv_active,
        config_file_exists,
        results['checks']['directories']
    ]
    
    if not all(critical_checks):
        results['valid'] = False
        results['message'] = "Critical environment checks failed"
    elif not env_file_exists:
        results['message'] = "Environment file missing - some features may not work"
    elif not api_keys_configured:
        results['message'] = "API keys not configured - AI features will not work"
    elif not (db_exists and db_valid):
        results['message'] = "Database not initialized - run database setup"
    else:
        results['message'] = "Environment is properly configured"
    
    return results


def get_database_status() -> Dict[str, Any]:
    """
    Get detailed database status information.
    
    Returns:
        Dict containing database status
    """
    db_path = 'data/metadata.db'
    status = {
        'exists': False,
        'valid': False,
        'tables': [],
        'version': None,
        'size': 0
    }
    
    if os.path.exists(db_path):
        status['exists'] = True
        status['size'] = os.path.getsize(db_path)
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get table list
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            status['tables'] = [row[0] for row in cursor.fetchall()]
            
            # Get database version
            try:
                cursor.execute("SELECT config_value FROM system_config WHERE config_key = 'db_version'")
                version_row = cursor.fetchone()
                if version_row:
                    status['version'] = version_row[0]
            except Exception:
                pass
            
            conn.close()
            status['valid'] = True
            
        except Exception as e:
            status['error'] = str(e)
    
    return status


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"
