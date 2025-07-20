import smtplib
from email.mime.text import MIMEText
from src.utils.config import Config
import logging
from typing import Optional

class EmailSender:
    """Handles sending email notifications for the application."""
    
    def __init__(self, config_path: str, secrets_path: str):
        """Initialize with configuration and secrets paths."""
        self.config = Config(config_path, secrets_path)
        self.logger = logging.getLogger(__name__)
        self.notification_config = self.config.get_notification_config()
    
    def send_email(self, to_email: str, subject: str, message: str) -> bool:
        """Send an email to the specified recipient."""
        try:
            if not to_email or not isinstance(to_email, str):
                raise ValueError("Invalid recipient email address")
            
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.notification_config.get('email_from', 'no-reply@laserapp.com')
            msg['To'] = to_email
            
            with smtplib.SMTP(self.notification_config.get('smtp_server', 'localhost'),
                            int(self.notification_config.get('smtp_port', 587))) as server:
                server.starttls()
                server.login(self.config.get('smtp_username'), self.config.get('smtp_password'))
                server.send_message(msg)
            
            self.logger.info(f"Email sent to {to_email} with subject '{subject}'")
            return True
        except ValueError as e:
            self.logger.error(f"Validation error sending email to {to_email}: {e}")
            raise
        except smtplib.SMTPAuthenticationError:
            self.logger.error(f"Authentication failed sending email to {to_email}")
            raise
        except Exception as e:
            self.logger.error(f"Error sending email to {to_email}: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sender = EmailSender("config/app_config.yaml", "config/secrets.yaml")
    try:
        success = sender.send_email(
            "client@example.com",
            "Appointment Reminder",
            "Your appointment is scheduled for tomorrow at 10:00 AM."
        )
        print(f"Email sent: {success}")
    except Exception as e:
        print(f"Error: {e}")