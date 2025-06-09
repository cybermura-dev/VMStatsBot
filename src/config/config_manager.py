import json
from pathlib import Path
from typing import Set, Dict, Any
from pydantic import BaseModel

class VMConnection(BaseModel):
    address: str
    password: str
    protocol: str
    rdp_settings: Dict[str, Any]

class VMConfig(BaseModel):
    name: str
    connection: VMConnection

class NotificationSettings(BaseModel):
    enable: bool
    check_interval: int
    settings: Dict[str, bool]
    messages: Dict[str, str]

class LoggingConfig(BaseModel):
    level: str
    format: str

class BotConfig(BaseModel):
    token: str
    admin_ids: Set[int]

class Config(BaseModel):
    bot: BotConfig
    vm: VMConfig
    notifications: NotificationSettings
    logging: LoggingConfig

class ConfigManager:
    _instance = None
    _config: Config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self.load_config()

    def load_config(self, config_path: str = "config.json") -> None:
        """Load configuration from file"""
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                self._config = Config(**config_data)
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")

    def save_config(self, config_path: str = "config.json") -> None:
        """Save configuration to file"""
        try:
            config_file = Path(config_path)
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config.model_dump(), f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error saving configuration: {str(e)}")

    @property
    def config(self) -> Config:
        """Get current configuration"""
        return self._config

    def update_config(self, new_config: dict) -> None:
        """Update configuration"""
        self._config = Config(**new_config)
        self.save_config() 