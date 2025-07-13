# controllers/service_controller.py
from sqlalchemy.orm import Session
from models.service import Service # Make sure this import is correct
from typing import Optional, List, Dict, Any

class ServiceController:
    def __init__(self, db: Session):
        self.db = db

    def get_service_by_name(self, name: str) -> Optional[Service]:
        """Retrieves a service by its name (case-insensitive)."""
        if not name: return None
        return self.db.query(Service).filter(Service.name.ilike(name)).first()

    def create_service(self, name: str, description: Optional[str] = None) -> Optional[Service]:
        """Creates a new service."""
        if not name:
            print("Error: Service name cannot be empty.")
            return None
        existing_service = self.get_service_by_name(name)
        if existing_service:
            print(f"Warning: Service '{name}' already exists (ID: {existing_service.id}). Skipping creation.")
            return existing_service

        new_service = Service(name=name, description=description)
        try:
            self.db.add(new_service)
            self.db.commit()
            self.db.refresh(new_service)
            print(f"Service created: {new_service.name} (ID: {new_service.id})")
            return new_service
        except Exception as e:
            self.db.rollback()
            print(f"Error creating service '{name}': {e}")
            return None

    def get_or_create_service(self, name: str, description: Optional[str] = None) -> Optional[Service]:
        """Gets a service by name, or creates it if it doesn't exist."""
        service = self.get_service_by_name(name)
        if service:
            return service
        return self.create_service(name, description)
    
    def get_all_services(self) -> List[Dict[str, Any]]:
        """Retrieves all services as a list of dictionaries."""
        services = self.db.query(Service).order_by(Service.name).all()
        return [service.to_dict() for service in services]

# updated