# D:\PYTHON\Laserowo\P1_desktop_app\controllers\hardware_controller.py

from models.hardware import Hardware
from sqlalchemy.orm import Session
from typing import Optional

class HardwareController: # <--- THIS CLASS NAME MUST MATCH EXACTLY
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_hardware_by_name(self, name: str) -> Optional[Hardware]:
        """
        Retrieves hardware by its name.
        """
        return self.db_session.query(Hardware).filter_by(name=name).first()

    def create_hardware(self, name: str, description: Optional[str] = None) -> Optional[Hardware]:
        """
        Creates new hardware.
        """
        try:
            new_hardware = Hardware(name=name, description=description)
            self.db_session.add(new_hardware)
            self.db_session.commit()
            self.db_session.refresh(new_hardware)
            return new_hardware
        except Exception as e:
            self.db_session.rollback()
            print(f"Error creating hardware '{name}': {e}")
            return None

    def get_or_create_hardware(self, name: str, **kwargs) -> Optional[Hardware]:
        """
        Gets hardware by name, or creates it if it doesn't exist.
        """
        hardware = self.get_hardware_by_name(name)
        if hardware:
            return hardware
        else:
            print(f"Creating new hardware: '{name}'")
            return self.create_hardware(name=name, **kwargs)

    # Add other CRUD methods (update, delete, get_all, etc.) as needed