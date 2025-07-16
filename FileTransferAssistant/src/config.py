import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class Config:
    """Configuration manager for the application."""
    
    def __init__(self, filename: str):
        """Initialize the configuration manager.
        
        Args:
            filename: Path to the configuration file.
        """
        self.filename = filename
        self.data: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.set_defaults()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            self.set_defaults()
    
    def set_defaults(self) -> None:
        """Set default configuration values."""
        self.data = {
            'window': {
                'geometry': None,
                'maximized': False
            },
            'source_folders': [],
            'file_types': [],
            'min_file_size_mb': 0,
            'max_file_size_mb': 0,  # 0 means no limit
            'date_filter_days': 0,  # 0 means no filter
            'default_destination': '',
            'auto_select_destination': True,
            'notifications': {
                'popup': True,
                'tray': True,
                'sound': True
            },
            'transfer': {
                'preserve_structure': True,
                'verify_checksum': True,
                'conflict_resolution': 'ask',  # 'ask', 'overwrite', 'skip', 'rename'
                'overwrite_policy': 'ask',
                'verify': False,
                'preserve_structure': True
            },
            'appearance': {
                'theme': 'system',  # 'system', 'light', 'dark'
                'font_size': 9,
                'icon_theme': 'default'
            },
            'recent_destinations': [],
            'recent_sources': []
        }
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Key in dot notation (e.g., 'window.width').
            default: Default value if key is not found.
            
        Returns:
            The configuration value or default.
        """
        keys = key.split('/')
        value = self.data
        
        try:
            for k in keys:
                if k.isdigit() and isinstance(value, list):
                    value = value[int(k)]
                else:
                    value = value[k]
            return value
        except (KeyError, TypeError, IndexError, AttributeError):
            # Try to get the default if available
            if default is not None:
                return default
            
            # Otherwise, create a temporary dictionary with default values
            try:
                temp_data = {}
                # Create a copy of the default configuration
                self.set_defaults()
                temp_data = self.data.copy()
                # Restore the original data
                self.load()
                
                # Get the value from the default data
                value = temp_data
                for k in keys:
                    value = value[k]
                return value
            except (KeyError, TypeError, IndexError, AttributeError):
                return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Key in dot notation (e.g., 'window.width').
            value: Value to set.
        """
        keys = key.split('/')
        current = self.data
        
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        self.save()
    
    def add_recent_destination(self, path: str) -> None:
        """Add a path to recent destinations.
        
        Args:
            path: Path to add to recent destinations.
        """
        recent = self.get('recent_destinations', [])
        if path in recent:
            recent.remove(path)
        recent.insert(0, path)
        self.set('recent_destinations', recent[:10])  # Keep only 10 most recent
    
    def add_recent_source(self, path: str) -> None:
        """Add a path to recent sources.
        
        Args:
            path: Path to add to recent sources.
        """
        recent = self.get('recent_sources', [])
        if path in recent:
            recent.remove(path)
        recent.insert(0, path)
        self.set('recent_sources', recent[:10])  # Keep only 10 most recent
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a boolean configuration value.
        
        Args:
            key: Key in dot notation (e.g., 'window.width').
            default: Default value if key is not found.
            
        Returns:
            bool: The boolean value of the configuration.
        """
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        return str(value).lower() in ('true', '1', 'yes', 'y')
    
    def get_int(self, key, default=0):
        """Get an integer configuration value.
        
        Args:
            key (str): The configuration key in 'section/name' format.
            default: Default value if key is not found or conversion fails.
            
        Returns:
            int: The integer value of the configuration.
        """
        try:
            return int(self.get(key, default))
        except (ValueError, TypeError):
            return default


class ConfigManager(Config):
    """Configuration manager that extends the base Config class."""
    def __init__(self, filename=None):
        if filename is None:
            # Use the user's home directory for the config file
            from pathlib import Path
            config_dir = Path.home() / '.filetransferassistant'
            config_dir.mkdir(exist_ok=True, parents=True)
            filename = str(config_dir / 'config.json')
        super().__init__(filename)
