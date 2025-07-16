import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """Manages application configuration with JSON file persistence."""
    
    def __init__(self, config_file: str = None):
        """Initialize the configuration manager.
        
        Args:
            config_file: Path to the configuration file. If None, uses default location.
        """
        # Default configuration
        self._default_config = {
            'ui': {
                'theme': 'light',  # 'light' or 'dark'
                'window_geometry': None,
                'window_state': None,
                'recent_destinations': [],
                'recent_sources': [],
            },
            'transfer': {
                'preserve_structure': True,
                'overwrite_policy': 'prompt',  # 'prompt', 'overwrite', 'skip', 'rename'
                'verify_checksum': False,
                'default_source_folders': [
                    str(Path.home() / 'Desktop'),
                    str(Path.home() / 'Downloads'),
                    str(Path.home() / 'Documents'),
                ]
            },
            'notifications': {
                'enabled': True,
                'sound': True,
                'popup': True
            },
            'logging': {
                'enabled': True,
                'max_log_size_mb': 10,
                'max_log_files': 5
            }
        }
        
        # Determine config file path
        if config_file is None:
            self.config_dir = Path.home() / '.filetransferassistant'
            self.config_file = self.config_dir / 'config.json'
        else:
            self.config_file = Path(config_file)
            self.config_dir = self.config_file.parent
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize config
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default if it doesn't exist."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return self._merge_configs(self._default_config, config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using default configuration.")
                return self._default_config.copy()
        else:
            self._save_config(self._default_config)
            return self._default_config.copy()
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, sort_keys=True)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def _merge_configs(self, default: Dict[str, Any], custom: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge default and custom configurations."""
        result = default.copy()
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by dot notation key."""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value by dot notation key."""
        keys = key.split('.')
        config = self._config
        
        # Navigate to the parent of the last key
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save the updated configuration
        self._save_config(self._config)
    
    def add_recent_destination(self, path: str) -> None:
        """Add a path to the recent destinations list."""
        self._update_recent_list('ui.recent_destinations', path)
    
    def add_recent_source(self, path: str) -> None:
        """Add a path to the recent sources list."""
        self._update_recent_list('ui.recent_sources', path)
    
    def _update_recent_list(self, config_key: str, path: str, max_items: int = 10) -> None:
        """Update a recent items list in the config."""
        recent = self.get(config_key, [])
        
        # Remove if already exists
        if path in recent:
            recent.remove(path)
        
        # Add to the beginning
        recent.insert(0, path)
        
        # Limit the number of items
        if len(recent) > max_items:
            recent = recent[:max_items]
        
        self.set(config_key, recent)
    
    def get_recent_destinations(self) -> list:
        """Get the list of recent destinations."""
        return self.get('ui.recent_destinations', [])
    
    def get_recent_sources(self) -> list:
        """Get the list of recent sources."""
        return self.get('ui.recent_sources', [])
    
    @property
    def theme(self) -> str:
        """Get the current theme."""
        return self.get('ui.theme', 'light')
    
    @theme.setter
    def theme(self, value: str) -> None:
        """Set the current theme."""
        if value in ('light', 'dark'):
            self.set('ui.theme', value)
