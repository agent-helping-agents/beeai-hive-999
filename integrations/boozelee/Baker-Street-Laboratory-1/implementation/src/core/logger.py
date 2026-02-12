"""
Baker Street Laboratory - Logging Configuration
Provides centralized logging setup for the research pipeline.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for Baker Street Laboratory.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        format_string: Optional custom format string
    
    Returns:
        Configured logger instance
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Default format string
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Get root logger
    logger = logging.getLogger("baker_street")
    logger.setLevel(numeric_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(f"baker_street.{name}")


def create_session_logger(session_id: str, output_dir: str) -> logging.Logger:
    """
    Create a session-specific logger.
    
    Args:
        session_id: Unique session identifier
        output_dir: Directory to store session logs
    
    Returns:
        Session logger instance
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(output_dir) / "logs" / f"session_{session_id}_{timestamp}.log"
    
    logger_name = f"baker_street.session.{session_id}"
    logger = logging.getLogger(logger_name)
    
    # Don't add handlers if they already exist
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        
        # Create file handler
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Set level
        logger.setLevel(logging.INFO)
    
    return logger
