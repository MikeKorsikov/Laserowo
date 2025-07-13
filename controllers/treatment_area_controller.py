# controllers/treatment_area_controller.py
from sqlalchemy.orm import Session
from models.treatment_area import TreatmentArea # Make sure your TreatmentArea model is defined
from typing import Optional, List, Dict, Any

class TreatmentAreaController:
    def __init__(self, db: Session):
        self.db = db

    def create_area(self, name: str) -> Optional[TreatmentArea]:
        """Creates a new treatment area."""
        if not name:
            print("Error: Treatment area name cannot be empty.")
            return None
        new_area = TreatmentArea(name=name)
        try:
            self.db.add(new_area)
            self.db.commit()
            self.db.refresh(new_area)
            print(f"Treatment Area created: {new_area.name}")
            return new_area
        except Exception as e:
            self.db.rollback()
            print(f"Error creating treatment area '{name}': {e}")
            return None

    def get_area_by_id(self, area_id: int) -> Optional[TreatmentArea]:
        """Retrieves a treatment area by ID."""
        return self.db.query(TreatmentArea).get(area_id)

    def get_area_by_name(self, name: str) -> Optional[TreatmentArea]:
        """Retrieves a treatment area by name."""
        return self.db.query(TreatmentArea).filter(TreatmentArea.name == name).first()

    def get_or_create_area(self, name: str) -> Optional[TreatmentArea]:
        """Retrieves a treatment area by name, or creates it if it doesn't exist."""
        area = self.get_area_by_name(name)
        if not area:
            area = self.create_area(name)
        return area

    def get_all_areas(self) -> List[Dict[str, Any]]:
        """Retrieves all treatment areas."""
        areas = self.db.query(TreatmentArea).order_by(TreatmentArea.name).all()
        return [area.to_dict() for area in areas]

# reviewed