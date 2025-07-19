from src.database.db_operations import DatabaseOperations
from src.models.inventory import Inventory
import logging
from typing import List, Optional

class InventoryManager:
    """Manages inventory-related operations for the laser hair removal application."""
    
    def __init__(self, config_path: str, db_path: str):
        """Initialize with database configuration and path."""
        self.db = DatabaseOperations(config_path, db_path)
        self.logger = logging.getLogger(__name__)
    
    def add_item(self, item_name: str, current_quantity: float, unit: str, 
                 low_stock_threshold: float = 10.0) -> int:
        """Add a new inventory item and return the item_id."""
        try:
            inventory = Inventory(0, item_name, current_quantity, unit, low_stock_threshold)
            query = """
                INSERT INTO inventory (item_name, current_quantity, unit, low_stock_threshold)
                VALUES (?, ?, ?, ?)
            """
            params = (inventory.item_name, inventory.current_quantity, inventory.unit, inventory.low_stock_threshold)
            self.db.execute_query(query, params)
            item_id = self.db.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            self.logger.info(f"Added inventory item {item_name} with ID {item_id}")
            return item_id
        except ValueError as e:
            self.logger.error(f"Validation error adding item {item_name}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error adding item {item_name}: {e}")
            raise
    
    def update_quantity(self, item_id: int, new_quantity: float) -> bool:
        """Update the current quantity of an inventory item."""
        try:
            current_item = self.get_item(item_id)
            if not current_item:
                self.logger.warning(f"Inventory item {item_id} not found for update")
                return False
            inventory = Inventory(item_id, current_item.item_name, new_quantity, current_item.unit, current_item.low_stock_threshold)
            query = "UPDATE inventory SET current_quantity = ? WHERE item_id = ?"
            self.db.execute_query(query, (inventory.current_quantity, item_id))
            self.logger.info(f"Updated quantity for item {item_id} to {new_quantity}")
            return True
        except ValueError as e:
            self.logger.error(f"Validation error updating item {item_id}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error updating item {item_id}: {e}")
            raise
    
    def get_item(self, item_id: int) -> Optional[Inventory]:
        """Retrieve an inventory item by item_id."""
        try:
            query = "SELECT * FROM inventory WHERE item_id = ?"
            results = self.db.execute_query(query, (item_id,))
            return Inventory.from_dict(results[0]) if results else None
        except Exception as e:
            self.logger.error(f"Error retrieving item {item_id}: {e}")
            raise
    
    def get_low_stock_items(self) -> List[Inventory]:
        """Retrieve all inventory items below their low stock threshold."""
        try:
            query = "SELECT * FROM inventory WHERE current_quantity < low_stock_threshold"
            results = self.db.execute_query(query)
            return [Inventory.from_dict(result) for result in results]
        except Exception as e:
            self.logger.error(f"Error retrieving low stock items: {e}")
            raise
    
    def adjust_threshold(self, item_id: int, new_threshold: float) -> bool:
        """Adjust the low stock threshold for an inventory item."""
        try:
            current_item = self.get_item(item_id)
            if not current_item:
                self.logger.warning(f"Inventory item {item_id} not found for threshold adjustment")
                return False
            inventory = Inventory(item_id, current_item.item_name, current_item.current_quantity, current_item.unit, new_threshold)
            query = "UPDATE inventory SET low_stock_threshold = ? WHERE item_id = ?"
            self.db.execute_query(query, (inventory.low_stock_threshold, item_id))
            self.logger.info(f"Adjusted threshold for item {item_id} to {new_threshold}")
            return True
        except ValueError as e:
            self.logger.error(f"Validation error adjusting threshold for item {item_id}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error adjusting threshold for item {item_id}: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = InventoryManager("config/secrets.yaml", "data/database.db")
    try:
        # Add an item
        item_id = manager.add_item("Laser Gel", 15.0, "ml")
        print(f"Added item ID: {item_id}")
        
        # Update quantity
        success = manager.update_quantity(item_id, 8.0)
        print(f"Quantity updated: {success}")
        
        # Check low stock
        low_stock_items = manager.get_low_stock_items()
        print(f"Low stock items: {[str(item) for item in low_stock_items]}")
    except Exception as e:
        print(f"Error: {e}")