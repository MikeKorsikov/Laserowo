from src.database.db_operations import DatabaseOperations
from src.models.hardware import Hardware
from src.utils.reminder_manager import ReminderManager
import logging
from datetime import datetime
from typing import List, Optional

class HardwareManager:
    """Manages hardware-related operations for the laser hair removal application."""
    
    def __init__(self, config_path: str, db_path: str):
        """Initialize with database configuration and path."""
        self.db = DatabaseOperations(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.reminder_manager = ReminderManager(config_path, db_path)
    
    def add_hardware(self, equipment_name: str, purchase_date: str = None, 
                     maximum_impulses_on_purchase: int = 0) -> int:
        """Add a new hardware item and return the hardware_id."""
        try:
            hardware = Hardware(0, equipment_name, purchase_date, maximum_impulses_on_purchase=maximum_impulses_on_purchase)
            query = """
                INSERT INTO hardware (equipment_name, purchase_date, maximum_impulses_on_purchase)
                VALUES (?, ?, ?)
            """
            params = (hardware.equipment_name, hardware.purchase_date, hardware.maximum_impulses_on_purchase)
            self.db.execute_query(query, params)
            hardware_id = self.db.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            self._schedule_initial_reminders(hardware_id)
            self.logger.info(f"Added hardware {equipment_name} with ID {hardware_id}")
            return hardware_id
        except ValueError as e:
            self.logger.error(f"Validation error adding hardware {equipment_name}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error adding hardware {equipment_name}: {e}")
            raise
    
    def record_impulse(self, hardware_id: int, impulses: int) -> bool:
        """Record impulses used and update total_impulses_recorded."""
        try:
            current_hardware = self.get_hardware(hardware_id)
            if not current_hardware:
                self.logger.warning(f"Hardware {hardware_id} not found for impulse recording")
                return False
            new_total = current_hardware.total_impulses_recorded + impulses
            hardware = Hardware(hardware_id, current_hardware.equipment_name, current_hardware.purchase_date,
                              current_hardware.last_maintenance_date, current_hardware.next_maintenance_due_date,
                              current_hardware.last_insurance_date, current_hardware.next_insurance_date,
                              current_hardware.maximum_impulses_on_purchase, new_total)
            query = "UPDATE hardware SET total_impulses_recorded = ? WHERE hardware_id = ?"
            self.db.execute_query(query, (hardware.total_impulses_recorded, hardware_id))
            self.logger.info(f"Recorded {impulses} impulses for hardware {hardware_id}")
            return True
        except ValueError as e:
            self.logger.error(f"Validation error recording impulses for hardware {hardware_id}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error recording impulses for hardware {hardware_id}: {e}")
            raise
    
    def update_maintenance(self, hardware_id: int, last_maintenance_date: str, 
                          next_maintenance_due_date: str) -> bool:
        """Update maintenance dates for hardware."""
        try:
            current_hardware = self.get_hardware(hardware_id)
            if not current_hardware:
                self.logger.warning(f"Hardware {hardware_id} not found for maintenance update")
                return False
            hardware = Hardware(hardware_id, current_hardware.equipment_name, current_hardware.purchase_date,
                              last_maintenance_date, next_maintenance_due_date, current_hardware.last_insurance_date,
                              current_hardware.next_insurance_date, current_hardware.maximum_impulses_on_purchase,
                              current_hardware.total_impulses_recorded)
            query = """
                UPDATE hardware SET last_maintenance_date = ?, next_maintenance_due_date = ? 
                WHERE hardware_id = ?
            """
            self.db.execute_query(query, (hardware.last_maintenance_date, hardware.next_maintenance_due_date, hardware_id))
            self.logger.info(f"Updated maintenance for hardware {hardware_id}")
            return True
        except ValueError as e:
            self.logger.error(f"Validation error updating maintenance for hardware {hardware_id}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error updating maintenance for hardware {hardware_id}: {e}")
            raise
    
    def update_insurance(self, hardware_id: int, last_insurance_date: str, 
                        next_insurance_due_date: str) -> bool:
        """Update insurance dates for hardware."""
        try:
            current_hardware = self.get_hardware(hardware_id)
            if not current_hardware:
                self.logger.warning(f"Hardware {hardware_id} not found for insurance update")
                return False
            hardware = Hardware(hardware_id, current_hardware.equipment_name, current_hardware.purchase_date,
                              current_hardware.last_maintenance_date, current_hardware.next_maintenance_due_date,
                              last_insurance_date, next_insurance_due_date, current_hardware.maximum_impulses_on_purchase,
                              current_hardware.total_impulses_recorded)
            query = """
                UPDATE hardware SET last_insurance_date = ?, next_insurance_due_date = ? 
                WHERE hardware_id = ?
            """
            self.db.execute_query(query, (hardware.last_insurance_date, hardware.next_insurance_date, hardware_id))
            self.logger.info(f"Updated insurance for hardware {hardware_id}")
            return True
        except ValueError as e:
            self.logger.error(f"Validation error updating insurance for hardware {hardware_id}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error updating insurance for hardware {hardware_id}: {e}")
            raise
    
    def get_hardware(self, hardware_id: int) -> Optional[Hardware]:
        """Retrieve a hardware item by hardware_id."""
        try:
            query = "SELECT * FROM hardware WHERE hardware_id = ?"
            results = self.db.execute_query(query, (hardware_id,))
            return Hardware.from_dict(results[0]) if results else None
        except Exception as e:
            self.logger.error(f"Error retrieving hardware {hardware_id}: {e}")
            raise
    
    def get_all_hardware(self) -> List[Hardware]:
        """Retrieve all hardware items."""
        try:
            query = "SELECT * FROM hardware"
            results = self.db.execute_query(query)
            return [Hardware.from_dict(result) for result in results]
        except Exception as e:
            self.logger.error(f"Error retrieving all hardware: {e}")
            raise
    
    def _schedule_initial_reminders(self, hardware_id: int) -> None:
        """Schedule initial maintenance and insurance reminders."""
        try:
            hardware = self.get_hardware(hardware_id)
            if hardware.next_maintenance_due_date:
                self.reminder_manager.schedule_reminder(
                    "Maintenance", hardware_id, hardware.next_maintenance_due_date, 
                    "Maintenance due for laser machine", "Popup"
                )
            if hardware.next_insurance_date:
                self.reminder_manager.schedule_reminder(
                    "Insurance", hardware_id, hardware.next_insurance_due_date, 
                    "Insurance renewal due for laser machine", "Popup"
                )
        except Exception as e:
            self.logger.error(f"Error scheduling reminders for hardware {hardware_id}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = HardwareManager("config/secrets.yaml", "data/database.db")
    try:
        # Add hardware
        hardware_id = manager.add_hardware("Laser Machine", "2024-01-15", 1000000)
        print(f"Added hardware ID: {hardware_id}")
        
        # Record impulses
        success = manager.record_impulse(hardware_id, 500)
        print(f"Impulses recorded: {success}")
        
        # Update maintenance
        maintenance_success = manager.update_maintenance(hardware_id, "2025-07-01", "2025-12-31")
        print(f"Maintenance updated: {maintenance_success}")
    except Exception as e:
        print(f"Error: {e}")