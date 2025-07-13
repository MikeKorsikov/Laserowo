# controllers/treatment_area_controller.py
from sqlalchemy.orm import Session
from models.treatment_area import TreatmentArea # Make sure this import is correct
from typing import Optional, List, Dict, Any

class TreatmentAreaController:
    def __init__(self, db: Session):
        self.db = db

    def get_area_by_name(self, name: str) -> Optional[TreatmentArea]:
        """Retrieves a treatment area by its name (case-insensitive)."""
        if not name: return None
        return self.db.query(TreatmentArea).filter(TreatmentArea.name.ilike(name)).first()

    def create_area(self, name: str, description: Optional[str] = None) -> Optional[TreatmentArea]:
        """Creates a new treatment area."""
        if not name:
            print("Error: Treatment area name cannot be empty.")
            return None
        existing_area = self.get_area_by_name(name)
        if existing_area:
            print(f"Warning: Treatment area '{name}' already exists (ID: {existing_area.id}). Skipping creation.")
            return existing_area

        new_area = TreatmentArea(name=name, description=description)
        try:
            self.db.add(new_area)
            self.db.commit()
            self.db.refresh(new_area)
            print(f"Treatment Area created: {new_area.name} (ID: {new_area.id})")
            return new_area
        except Exception as e:
            self.db.rollback()
            print(f"Error creating treatment area '{name}': {e}")
            return None

    def get_or_create_area(self, name: str, description: Optional[str] = None) -> Optional[TreatmentArea]:
        """Gets a treatment area by name, or creates it if it doesn't exist."""
        area = self.get_area_by_name(name)
        if area:
            return area
        return self.create_area(name, description)
    
    def get_all_areas(self) -> List[Dict[str, Any]]:
        """Retrieves all treatment areas as a list of dictionaries."""
        areas = self.db.query(TreatmentArea).order_by(TreatmentArea.name).all()
        return [area.to_dict() for area in areas]

# updated