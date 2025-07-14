"""
Client service for managing client data
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.database.db_manager import db_manager

logger = logging.getLogger(__name__)

class ClientService:
    """Handles client data management"""
    
    @staticmethod
    def add_client(full_name: str, phone_number: str = None, email: str = None, 
                  date_of_birth: str = None, is_blacklisted: bool = False, 
                  is_active: bool = True) -> Optional[int]:
        """Add a new client and return client_id if successful"""
        try:
            cursor = db_manager.execute_query(
                """INSERT INTO clients (full_name, phone_number, email, date_of_birth, 
                   is_blacklisted, is_active) VALUES (?, ?, ?, ?, ?, ?)""",
                (full_name, phone_number, email, date_of_birth, is_blacklisted, is_active)
            )
            client_id = cursor.lastrowid
            logger.info(f"Client added: {full_name} with ID: {client_id}")
            return client_id
        except Exception as e:
            logger.error(f"Error adding client {full_name}: {e}")
            return None
    
    @staticmethod
    def get_client_by_id(client_id: int) -> Optional[Dict[str, Any]]:
        """Get a client by ID"""
        try:
            client = db_manager.fetch_one(
                "SELECT * FROM clients WHERE client_id = ?",
                (client_id,)
            )
            if client:
                return dict(client)
            return None
        except Exception as e:
            logger.error(f"Error getting client {client_id}: {e}")
            return None
    
    @staticmethod
    def get_all_clients(active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all clients"""
        try:
            if active_only:
                query = "SELECT * FROM clients WHERE is_active = 1 ORDER BY full_name"
            else:
                query = "SELECT * FROM clients ORDER BY full_name"
            
            clients = db_manager.fetch_all(query)
            return [dict(client) for client in clients]
        except Exception as e:
            logger.error(f"Error getting all clients: {e}")
            return []
    
    @staticmethod
    def update_client(client_id: int, **kwargs) -> bool:
        """Update client details"""
        try:
            # Build dynamic update query
            update_fields = []
            values = []
            
            allowed_fields = ['full_name', 'phone_number', 'email', 'date_of_birth', 
                            'is_blacklisted', 'is_active']
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    update_fields.append(f"{field} = ?")
                    values.append(value)
            
            if not update_fields:
                logger.warning("No valid fields to update")
                return False
            
            # Add updated_at timestamp
            update_fields.append("updated_at = ?")
            values.append(datetime.now().isoformat())
            
            # Add client_id for WHERE clause
            values.append(client_id)
            
            query = f"UPDATE clients SET {', '.join(update_fields)} WHERE client_id = ?"
            
            db_manager.execute_query(query, tuple(values))
            logger.info(f"Client updated: {client_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating client {client_id}: {e}")
            return False
    
    @staticmethod
    def delete_client(client_id: int) -> bool:
        """Soft delete a client (set is_active to False)"""
        try:
            return ClientService.update_client(client_id, is_active=False)
        except Exception as e:
            logger.error(f"Error deleting client {client_id}: {e}")
            return False
    
    @staticmethod
    def search_clients(search_term: str) -> List[Dict[str, Any]]:
        """Search clients by name, phone, or email"""
        try:
            search_pattern = f"%{search_term}%"
            clients = db_manager.fetch_all(
                """SELECT * FROM clients 
                   WHERE (full_name LIKE ? OR phone_number LIKE ? OR email LIKE ?) 
                   AND is_active = 1 
                   ORDER BY full_name""",
                (search_pattern, search_pattern, search_pattern)
            )
            return [dict(client) for client in clients]
        except Exception as e:
            logger.error(f"Error searching clients: {e}")
            return []
    
    @staticmethod
    def get_client_count() -> int:
        """Get the total number of active clients"""
        try:
            result = db_manager.fetch_one(
                "SELECT COUNT(*) as count FROM clients WHERE is_active = 1"
            )
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error getting client count: {e}")
            return 0
    
    @staticmethod
    def blacklist_client(client_id: int, blacklist: bool = True) -> bool:
        """Blacklist or unblacklist a client"""
        try:
            return ClientService.update_client(client_id, is_blacklisted=blacklist)
        except Exception as e:
            logger.error(f"Error blacklisting client {client_id}: {e}")
            return False