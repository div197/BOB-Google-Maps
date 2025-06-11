"""bob_core.logging_config

Centralized logging configuration for BOB Google Maps.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

__all__ = ["setup_logging", "get_logger"]


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None,
    include_timestamp: bool = True
) -> logging.Logger:
    """
    Setup centralized logging configuration.
    
    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log_file : Optional[str]
        Path to log file. If None, logs only to console.
    format_string : Optional[str]
        Custom format string. If None, uses default.
    include_timestamp : bool
        Whether to include timestamp in logs
        
    Returns
    -------
    logging.Logger
        Configured logger instance
    """
    # Clear any existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)
    
    # Create formatter
    if format_string is None:
        if include_timestamp:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        else:
            format_string = "%(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Parameters
    ----------
    name : str
        Logger name (typically __name__)
        
    Returns
    -------
    logging.Logger
        Logger instance
    """
    return logging.getLogger(name)


def setup_scraper_logging(
    output_dir: str = "output",
    session_id: Optional[str] = None
) -> logging.Logger:
    """
    Setup logging specifically for scraping sessions.
    
    Parameters
    ----------
    output_dir : str
        Output directory for logs
    session_id : Optional[str]
        Unique session identifier. If None, uses timestamp.
        
    Returns
    -------
    logging.Logger
        Configured logger for scraping
    """
    if session_id is None:
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    log_file = Path(output_dir) / "logs" / f"scrape_{session_id}.log"
    
    return setup_logging(
        level="INFO",
        log_file=str(log_file),
        format_string="%(asctime)s - %(levelname)s - %(message)s"
    ) 