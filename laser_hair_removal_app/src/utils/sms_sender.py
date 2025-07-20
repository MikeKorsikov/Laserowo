import requests
from src.utils.config import Config
import logging
from typing import Optional

class SMSSender:
    """Handles sending SMS notifications for the application."""
    
    def __init__(self, config_path: str, secrets_path: str):
        """Initialize with configuration and secrets paths."""
        self.config = Config(config_path, secrets_path)
        self.logger = logging.getLogger(__name__)
        self.notification_config = self.config.get_notification_config()
    
    def send_sms(self, to_phone: str, message: str) -> bool:
        """Send an SMS to the specified phone number."""
        try:
            if not to_phone or not isinstance(to_phone, str):
                raise ValueError("Invalid phone number")
            
            sms_gateway = self.notification_config.get('sms_gateway')
            api_key = self.config.get('sms_api_key')
            if not sms_gateway or not api_key:
                raise ValueError("SMS gateway or API key not configured")
            
            # Assume a simple HTTP POST request to a gateway (e.g., Twilio-like API)
            url = f"{sms_gateway}/send"
            payload = {
                'to': to_phone,
                'message': message,
                'api_key': api_key,
                'from': self.notification_config.get('sms_from', 'LaserApp')
            }
            response = requests.post(url, data=payload, timeout=10)
            
            if response.status_code == 200 and response.json().get('success'):
                self.logger.info(f"SMS sent to {to_phone}")
                return True
            else:
                self.logger.warning(f"Failed to send SMS to {to_phone}: {response.text}")
                raise ValueError(f"Failed to send SMS: {response.text}")
        except ValueError as e:
            self.logger.error(f"Validation error sending SMS to {to_phone}: {e}")
            raise
        except requests.RequestException as e:
            self.logger.error(f"Network error sending SMS to {to_phone}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error sending SMS to {to_phone}: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sender = SMSSender("config/app_config.yaml", "config/secrets.yaml")
    try:
        success = sender.send_sms(
            "+48123456789",
            "Your appointment is scheduled for tomorrow at 10:00 AM."
        )
        print(f"SMS sent: {success}")
    except Exception as e:
        print(f"Error: {e}")