# AI Jobs Automation - Utility Functions

import os
import json
from datetime import datetime

def create_backup(file_path):
    """
    Create backup of a file with timestamp
    
    Args:
        file_path: Path to file to backup
        
    Returns:
        Path to backup file
    """
    if not os.path.exists(file_path):
        return None
        
    # Create backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.bak_{timestamp}"
    
    # Copy file
    with open(file_path, 'r') as source:
        with open(backup_path, 'w') as backup:
            backup.write(source.read())
    
    print(f"✅ Created backup: {backup_path}")
    return backup_path

def load_json_config(file_path):
    """
    Load JSON configuration file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary with configuration or None if error
    """
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
        print(f"✅ Loaded config: {file_path}")
        return config
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None

def save_json_config(file_path, config):
    """
    Save configuration to JSON file
    
    Args:
        file_path: Path to save JSON file
        config: Dictionary with configuration
        
    Returns:
        True if successful, False if error
    """
    try:
        # Create backup first
        create_backup(file_path)
        
        # Save new config
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Saved config: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return False

def validate_email(email):
    """
    Basic email validation
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False if invalid
    """
    if not email or '@' not in email or '.' not in email:
        return False
    
    # Simple validation - for more robust validation use a library
    return True

def get_timestamp():
    """
    Get current timestamp in ISO format
    
    Returns:
        ISO format timestamp string
    """
    return datetime.now().isoformat()

def log_activity(activity, details=""):
    """
    Log automation activity
    
    Args:
        activity: Activity description
        details: Additional details
    """
    timestamp = get_timestamp()
    log_entry = f"[{timestamp}] {activity}"
    
    if details:
        log_entry += f": {details}"
    
    print(log_entry)
    
    # Also write to log file
    with open('automation.log', 'a') as f:
        f.write(log_entry + '\n')

def ensure_directory_exists(directory):
    """
    Ensure directory exists, create if not
    
    Args:
        directory: Directory path
        
    Returns:
        True if exists or created, False if error
    """
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory ensured: {directory}")
        return True
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return False

def read_file_content(file_path):
    """
    Read file content safely
    
    Args:
        file_path: Path to file
        
    Returns:
        File content or None if error
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def write_file_content(file_path, content, backup=True):
    """
    Write content to file safely
    
    Args:
        file_path: Path to file
        content: Content to write
        backup: Whether to create backup
        
    Returns:
        True if successful, False if error
    """
    try:
        if backup and os.path.exists(file_path):
            create_backup(file_path)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Written to file: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

# WATERMARK: PRIMAX-AI-BSP-2025
© 2025 Bakery Street Project