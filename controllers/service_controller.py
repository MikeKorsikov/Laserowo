# controllers/service_controller.py
from sqlalchemy.orm import Session
from models.service import Service # Assuming you have a Service model
from typing import Optional, List, Dict, Any

class ServiceController:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_service(self, name: str, description: Optional[str] = None) -> Optional[Service]:
        """
        Retrieves a service by name, or creates a new one if it doesn't exist.
        """
        service = self.db.query(Service).filter_by(name=name).first()
        if not service:
            try:
                service = Service(name=name, description=description or f"Service imported: {name}")
                self.db.add(service)
                self.db.commit()
                self.db.refresh(service)
                print(f"Created new service: '{name}' (ID: {service.id})")
            except Exception as e:
                self.db.rollback()
                print(f"Error creating service '{name}': {e}")
                return None
        return service
    
    def get_service_by_name(self, name: str) -> Optional[Service]:
        """Retrieves a service by its exact name."""
        return self.db.query(Service).filter_by(name=name).first()

    def get_service_by_id(self, service_id: int) -> Optional[Service]:
        """Retrieves a service by its ID."""
        return self.db.query(Service).get(service_id)

    def get_all_services(self) -> List[Service]:
        """Retrieves all services."""
        return self.db.query(Service).all()

    # Add update_service, delete_service if needed