import yaml
from pathlib import Path
import logging
from typing import Dict, Optional

class Config:
    """Manages configuration settings for the application."""
    
    def __init__(self, config_path: str, secrets_path: str):
        """Initialize with paths to config and secrets files."""
        self.config_path = Path(config_path)
        self.secrets_path = Path(secrets_path)
        self.logger = logging.getLogger(__name__)
        self.config_data = self._load_config()
        self.secrets_data = self._load_secrets()
    
    def _load_config(self) -> Dict:
        """Load application configuration from app_config.yaml."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
            self.logger.info(f"Loaded configuration from {self.config_path}")
            return config
        except FileNotFoundError:
            self.logger.error(f"Config file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing config file {self.config_path}: {e}")
            raise
    
    def _load_secrets(self) -> Dict:
        """Load sensitive data from secrets.yaml."""
        try:
            with open(self.secrets_path, 'r') as f:
                secrets = yaml.safe_load(f) or {}
            self.logger.info(f"Loaded secrets from {self.secrets_path}")
            return secrets
        except FileNotFoundError:
            self.logger.error(f"Secrets file not found: {self.secrets_path}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing secrets file {self.secrets_path}: {e}")
            raise
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieve a configuration value, falling back to secrets or default."""
        value = self.config_data.get(key, self.secrets_data.get(key, default))
        if value is None:
            self.logger.warning(f"Configuration key {key} not found, using default {default}")
        return value
    
    def get_database_config(self) -> Dict:
        """Retrieve database configuration."""
        db_config = {
            'encryption_key': self.secrets_data.get('database', {}).get('encryption_key'),
            'db_path': self.config_data.get('database', {}).get('db_path', 'data/database.db')
        }
        if not db_config['encryption_key']:
            self.logger.error("Database encryption key not found in secrets")
            raise ValueError("Missing encryption key")
        return db_config
    
    def get_notification_config(self) -> Dict:
        """Retrieve notification configuration."""
        return {
            'smtp_server': self.secrets_data.get('notifications', {}).get('smtp_server'),
            'smtp_port': self.secrets_data.get('notifications', {}).get('smtp_port'),
            'sms_gateway': self.secrets_data.get('notifications', {}).get('sms_gateway'),
            'email_from': self.secrets_data.get('notifications', {}).get('email_from')
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = Config("config/app_config.yaml", "config/secrets.yaml")
    try:
        print(f"Database config: {config.get_database_config()}")
        print(f"Notification config: {config.get_notification_config()}")
        print(f"Custom key: {config.get('custom_key', 'default_value')}")
    except Exception as e:
        print(f"Error: {e}")