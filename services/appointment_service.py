"""
Appointment service for managing appointments
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from app.database.db_manager import db_manager

logger = logging.getLogger(__name__)

class AppointmentService:
    """Handles appointment management"""
    
    @staticmethod
    def add_appointment(client_id: int, service_id: int, area_id: int, 
                       appointment_date: str, start_time: str, end_time: str, 
                       notes: str = None) -> Optional[int]:
        """Add a new appointment and return appointment_id if successful"""
        try:
            cursor = db_manager.execute_query(
                """INSERT INTO appointments (client_id, service_id, area_id, 
                   appointment_date, start_time, end_time, notes) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (client_id, service_id, area_id, appointment_date, start_time, end_time, notes)
            )
            appointment_id = cursor.lastrowid
            logger.info(f"Appointment added with ID: {appointment_id}")
            return appointment_id
        except Exception as e:
            logger.error(f"Error adding appointment: {e}")
            return None
    
    @staticmethod
    def get_appointment_by_id(appointment_id: int) -> Optional[Dict[str, Any]]:
        """Get an appointment by ID with related data"""
        try:
            appointment = db_manager.fetch_one(
                """SELECT a.*, c.full_name as client_name, s.service_name, 
                   ta.area_name, s.base_price, s.estimated_duration_minutes
                   FROM appointments a
                   JOIN clients c ON a.client_id = c.client_id
                   JOIN services s ON a.service_id = s.service_id
                   JOIN treatment_areas ta ON a.area_id = ta.area_id
                   WHERE a.appointment_id = ?""",
                (appointment_id,)
            )
            if appointment:
                return dict(appointment)
            return None
        except Exception as e:
            logger.error(f"Error getting appointment {appointment_id}: {e}")
            return None
    
    @staticmethod
    def get_appointments_for_date(appointment_date: str) -> List[Dict[str, Any]]:
        """Get all appointments for a specific date"""
        try:
            appointments = db_manager.fetch_all(
                """SELECT a.*, c.full_name as client_name, s.service_name, 
                   ta.area_name, s.base_price, s.estimated_duration_minutes
                   FROM appointments a
                   JOIN clients c ON a.client_id = c.client_id
                   JOIN services s ON a.service_id = s.service_id
                   JOIN treatment_areas ta ON a.area_id = ta.area_id
                   WHERE a.appointment_date = ?
                   ORDER BY a.start_time""",
                (appointment_date,)
            )
            return [dict(appointment) for appointment in appointments]
        except Exception as e:
            logger.error(f"Error getting appointments for date {appointment_date}: {e}")
            return []
    
    @staticmethod
    def get_appointments_for_client(client_id: int) -> List[Dict[str, Any]]:
        """Get all appointments for a specific client"""
        try:
            appointments = db_manager.fetch_all(
                """SELECT a.*, c.full_name as client_name, s.service_name, 
                   ta.area_name, s.base_price, s.estimated_duration_minutes
                   FROM appointments a
                   JOIN clients c ON a.client_id = c.client_id
                   JOIN services s ON a.service_id = s.service_id
                   JOIN treatment_areas ta ON a.area_id = ta.area_id
                   WHERE a.client_id = ?
                   ORDER BY a.appointment_date DESC, a.start_time""",
                (client_id,)
            )
            return [dict(appointment) for appointment in appointments]
        except Exception as e:
            logger.error(f"Error getting appointments for client {client_id}: {e}")
            return []
    
    @staticmethod
    def get_all_appointments(limit: int = 100) -> List[Dict[str, Any]]:
        """Get all appointments with limit"""
        try:
            appointments = db_manager.fetch_all(
                """SELECT a.*, c.full_name as client_name, s.service_name, 
                   ta.area_name, s.base_price, s.estimated_duration_minutes
                   FROM appointments a
                   JOIN clients c ON a.client_id = c.client_id
                   JOIN services s ON a.service_id = s.service_id
                   JOIN treatment_areas ta ON a.area_id = ta.area_id
                   ORDER BY a.appointment_date DESC, a.start_time
                   LIMIT ?""",
                (limit,)
            )
            return [dict(appointment) for appointment in appointments]
        except Exception as e:
            logger.error(f"Error getting all appointments: {e}")
            return []
    
    @staticmethod
    def update_appointment_status(appointment_id: int, status: str) -> bool:
        """Update appointment status"""
        try:
            valid_statuses = ['scheduled', 'completed', 'cancelled']
            if status not in valid_statuses:
                logger.error(f"Invalid status: {status}")
                return False
            
            db_manager.execute_query(
                "UPDATE appointments SET status = ?, updated_at = ? WHERE appointment_id = ?",
                (status, datetime.now().isoformat(), appointment_id)
            )
            logger.info(f"Appointment {appointment_id} status updated to: {status}")
            return True
        except Exception as e:
            logger.error(f"Error updating appointment status {appointment_id}: {e}")
            return False
    
    @staticmethod
    def update_appointment(appointment_id: int, **kwargs) -> bool:
        """Update appointment details"""
        try:
            # Build dynamic update query
            update_fields = []
            values = []
            
            allowed_fields = ['client_id', 'service_id', 'area_id', 'appointment_date', 
                            'start_time', 'end_time', 'status', 'notes']
            
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
            
            # Add appointment_id for WHERE clause
            values.append(appointment_id)
            
            query = f"UPDATE appointments SET {', '.join(update_fields)} WHERE appointment_id = ?"
            
            db_manager.execute_query(query, tuple(values))
            logger.info(f"Appointment updated: {appointment_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating appointment {appointment_id}: {e}")
            return False
    
    @staticmethod
    def delete_appointment(appointment_id: int) -> bool:
        """Delete an appointment"""
        try:
            db_manager.execute_query(
                "DELETE FROM appointments WHERE appointment_id = ?",
                (appointment_id,)
            )
            logger.info(f"Appointment deleted: {appointment_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting appointment {appointment_id}: {e}")
            return False
    
    @staticmethod
    def get_services() -> List[Dict[str, Any]]:
        """Get all active services"""
        try:
            services = db_manager.fetch_all(
                "SELECT * FROM services WHERE is_active = 1 ORDER BY service_name"
            )
            return [dict(service) for service in services]
        except Exception as e:
            logger.error(f"Error getting services: {e}")
            return []
    
    @staticmethod
    def get_treatment_areas() -> List[Dict[str, Any]]:
        """Get all active treatment areas"""
        try:
            areas = db_manager.fetch_all(
                "SELECT * FROM treatment_areas WHERE is_active = 1 ORDER BY area_name"
            )
            return [dict(area) for area in areas]
        except Exception as e:
            logger.error(f"Error getting treatment areas: {e}")
            return []