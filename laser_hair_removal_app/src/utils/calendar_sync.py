from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.utils.config import Config
import logging
from datetime import datetime, timedelta
import os
from typing import Optional

class CalendarSync:
    """Handles synchronization of appointments with an external calendar."""
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self, config_path: str, secrets_path: str):
        """Initialize with configuration and secrets paths."""
        self.config = Config(config_path, secrets_path)
        self.logger = logging.getLogger(__name__)
        self.credentials = self._get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)
    
    def _get_credentials(self) -> Credentials:
        """Get or refresh Google Calendar API credentials."""
        creds = None
        token_path = 'data/token.json'
        credentials_path = self.config.get('google_credentials_path', 'config/credentials.json')
        
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
        
        return creds
    
    def add_event(self, appointment_id: int, appointment_date: str, client_name: str) -> Optional[str]:
        """Add an appointment as an event to the calendar."""
        try:
            # Parse date and set time (e.g., 10:00 AM to 11:00 AM)
            date = datetime.strptime(appointment_date, '%Y-%m-%d')
            start_time = date.replace(hour=10, minute=0, second=0).isoformat() + 'Z'
            end_time = date.replace(hour=11, minute=0, second=0).isoformat() + 'Z'
            
            event = {
                'summary': f"Appointment {appointment_id} - {client_name}",
                'start': {'dateTime': start_time, 'timeZone': 'Europe/Warsaw'},
                'end': {'dateTime': end_time, 'timeZone': 'Europe/Warsaw'},
                'description': f"Client: {client_name}, Appointment ID: {appointment_id}"
            }
            
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            self.logger.info(f"Added event {event.get('id')} for appointment {appointment_id}")
            return event.get('id')
        except Exception as e:
            self.logger.error(f"Error adding event for appointment {appointment_id}: {e}")
            raise
    
    def update_event(self, event_id: str, appointment_date: str, client_name: str) -> bool:
        """Update an existing calendar event for a rescheduled appointment."""
        try:
            date = datetime.strptime(appointment_date, '%Y-%m-%d')
            start_time = date.replace(hour=10, minute=0, second=0).isoformat() + 'Z'
            end_time = date.replace(hour=11, minute=0, second=0).isoformat() + 'Z'
            
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            event['start'] = {'dateTime': start_time, 'timeZone': 'Europe/Warsaw'}
            event['end'] = {'dateTime': end_time, 'timeZone': 'Europe/Warsaw'}
            event['summary'] = f"Appointment {event_id.split('_')[0]} - {client_name}"
            
            self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
            self.logger.info(f"Updated event {event_id} for appointment")
            return True
        except Exception as e:
            self.logger.error(f"Error updating event {event_id}: {e}")
            raise
    
    def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event for a cancelled appointment."""
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            self.logger.info(f"Deleted event {event_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting event {event_id}: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sync = CalendarSync("config/app_config.yaml", "config/secrets.yaml")
    try:
        # Add a sample event (today's date: July 20, 2025)
        event_id = sync.add_event(1, "2025-07-20", "Jan Kowalski")
        print(f"Added event ID: {event_id}")
        
        # Update the event (e.g., to tomorrow)
        sync.update_event(event_id, "2025-07-21", "Jan Kowalski")
        print(f"Updated event {event_id}")
        
        # Delete the event
        success = sync.delete_event(event_id)
        print(f"Deleted event: {success}")
    except Exception as e:
        print(f"Error: {e}")