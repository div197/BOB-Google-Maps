"""bob_core.config

Configuration management for BOB Google Maps.
"""
from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

__all__ = ["Config", "load_config", "save_config", "get_default_config"]


@dataclass
class Config:
    """BOB configuration settings."""
    
    # Scraping settings
    default_backend: str = "auto"  # selenium, playwright, auto
    default_headless: bool = True
    default_timeout: int = 30
    
    # Batch processing
    default_workers: int = 4
    max_workers: int = 20
    
    # Output settings
    output_dir: str = "output"
    default_format: str = "json"
    
    # Analytics settings
    enable_sentiment: bool = True
    enable_keywords: bool = True
    
    # Rate limiting
    request_delay: float = 1.0
    max_retries: int = 3
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create from dictionary."""
        return cls(**data)


def get_config_path() -> Path:
    """Get configuration file path."""
    # Check environment variable first
    if config_path := os.getenv("BOB_CONFIG_PATH"):
        return Path(config_path)
    
    # Check current directory
    local_config = Path("bob_config.json")
    if local_config.exists():
        return local_config
    
    # Use user config directory
    if os.name == "nt":  # Windows
        config_dir = Path(os.getenv("APPDATA", "")) / "BOB"
    else:  # Unix-like
        config_dir = Path.home() / ".config" / "bob"
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def get_default_config() -> Config:
    """Get default configuration."""
    return Config()


def load_config(config_path: Optional[Path] = None) -> Config:
    """
    Load configuration from file.
    
    Parameters
    ----------
    config_path : Optional[Path]
        Path to config file. If None, uses default location.
        
    Returns
    -------
    Config
        Loaded configuration
    """
    if config_path is None:
        config_path = get_config_path()
    
    if not config_path.exists():
        return get_default_config()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Config.from_dict(data)
    except (json.JSONDecodeError, TypeError, ValueError):
        # Return default config if file is corrupted
        return get_default_config()


def save_config(config: Config, config_path: Optional[Path] = None) -> Path:
    """
    Save configuration to file.
    
    Parameters
    ----------
    config : Config
        Configuration to save
    config_path : Optional[Path]
        Path to save config. If None, uses default location.
        
    Returns
    -------
    Path
        Path where config was saved
    """
    if config_path is None:
        config_path = get_config_path()
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config.to_dict(), f, indent=2)
    
    return config_path


def update_config(**kwargs) -> Config:
    """
    Update configuration with new values.
    
    Parameters
    ----------
    **kwargs
        Configuration values to update
        
    Returns
    -------
    Config
        Updated configuration
    """
    config = load_config()
    
    # Update values
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    save_config(config)
    return config 