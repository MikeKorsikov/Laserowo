import yaml
import os
import logging
from src.utils.logger import Logger

class Config:
    """Loads and manages configuration settings from YAML files."""
    
    REQUIRED_SECRETS = {
        'database': ['encryption_key'],
        'notifications': {
            'smtp': ['host', 'port', 'username', 'password'],
            'twilio': ['account_sid', 'auth_token', 'from_number'],
            'calendar': {
                'google': ['client_id', 'client_secret', 'refresh_token'],
                'apple': ['client_id', 'team_id', 'key_id', 'private_key']
            }
        }
    }
    
    DEFAULTS = {
        'logging': {'level': 'INFO'}
    }

    def __init__(self, config_path: str, secrets_path: str):
        """Initialize with paths to config and secrets YAML files."""
        self.config_path = config_path
        self.secrets_path = secrets_path
        self.logger = Logger().get_logger(__name__)
        self.config_data = {}
        self.secrets_data = {}
        self._load_configs()

    def _load_configs(self):
        """Load configuration and secrets from YAML files."""
        try:
            # Load app_config.yaml
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config_data = yaml.safe_load(f) or {}
                self.logger.info("Loaded configuration from %s", self.config_path)
            else:
                self.logger.warning("Configuration file %s not found, using empty config", self.config_path)

            # Load secrets.yaml
            if os.path.exists(self.secrets_path):
                with open(self.secrets_path, 'r') as f:
                    self.secrets_data = yaml.safe_load(f) or {}
                self._validate_secrets()
                self.logger.info("Loaded secrets from %s", self.secrets_path)
            else:
                self.logger.error("Secrets file %s not found, application may fail", self.secrets_path)
                raise FileNotFoundError(f"Secrets file {self.secrets_path} is required")
        except yaml.YAMLError as e:
            self.logger.error("Error parsing YAML files: %s", str(e))
            raise

    def _validate_secrets(self):
        """Validate that required secrets are present."""
        for section, required_fields in self.REQUIRED_SECRETS.items():
            if isinstance(required_fields, dict):  # Nested sections like notifications
                for sub_section, sub_fields in required_fields.items():
                    if sub_section not in self.secrets_data.get(section, {}):
                        self.logger.warning("Missing %s section in secrets", sub_section)
                    else:
                        for field in sub_fields:
                            if field not in self.secrets_data[section][sub_section]:
                                self.logger.error("Missing required field %s in %s.%s", field, section, sub_section)
                                raise KeyError(f"Missing required field {field} in {section}.{sub_section}")
            else:  # Flat sections like database
                for field in required_fields:
                    if field not in self.secrets_data.get(section, {}):
                        self.logger.error("Missing required field %s in %s", field, section)
                        raise KeyError(f"Missing required field {field} in {section}")

    def get(self, key: str, default=None):
        """Retrieve a configuration value, checking both config and secrets."""
        keys = key.split('.')
        value = self.config_data
        for k in keys[:-1]:
            value = value.get(k, {})
        value = value.get(keys[-1], default)

        # Fallback to secrets if not in config
        if value is None and keys[0] in self.secrets_data:
            secrets_value = self.secrets_data
            for k in keys:
                secrets_value = secrets_value.get(k, {})
            value = secrets_value if secrets_value != {} else default

        # Apply defaults for optional settings
        if value is None and keys[0] in self.DEFAULTS:
            defaults = self.DEFAULTS
            for k in keys:
                defaults = defaults.get(k, {})
            value = defaults if defaults != {} else default

        if value is None:
            self.logger.warning("Key %s not found, returning default %s", key, default)
        return value

    def get_logging_level(self) -> str:
        """Retrieve logging level with fallback."""
        level = self.get('logging.level')
        return level if level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] else 'INFO'

if __name__ == "__main__":
    config = Config("config/app_config.yaml", "config/secrets.yaml")
    print(config.get('database.encryption_key'))
    print(config.get('notifications.smtp.host'))
    print(config.get_logging_level())