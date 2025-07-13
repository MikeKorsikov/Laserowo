# P1_desktop_app/controllers/promotion_controller.py

from models.promotion import Promotion  # Assuming you have a Promotion model
from datetime import datetime, date

class PromotionController:
    def __init__(self, db_session):
        """
        Initializes the PromotionController with a database session.
        Args:
            db_session: The database session object (e.g., SQLAlchemy session).
        """
        self.db_session = db_session

    def create_promotion(self, name, description, discount_percentage,
                         start_date, end_date, active=True):
        """
        Creates a new promotion.
        Args:
            name (str): Name of the promotion.
            description (str): Description of the promotion.
            discount_percentage (float): Discount percentage (e.g., 10.0 for 10%).
            start_date (date): The date the promotion starts.
            end_date (date): The date the promotion ends.
            active (bool): Whether the promotion is currently active.
        Returns:
            Promotion: The newly created Promotion object, or None if creation fails.
        """
        try:
            new_promotion = Promotion(
                name=name,
                description=description,
                discount_percentage=discount_percentage,
                start_date=start_date,
                end_date=end_date,
                active=active
            )
            self.db_session.add(new_promotion)
            self.db_session.commit()
            return new_promotion
        except Exception as e:
            self.db_session.rollback()
            print(f"Error creating promotion: {e}")
            return None

    def get_promotion_by_id(self, promotion_id):
        """
        Retrieves a promotion by its ID.
        Args:
            promotion_id (int): The ID of the promotion.
        Returns:
            Promotion: The Promotion object, or None if not found.
        """
        return self.db_session.query(Promotion).get(promotion_id)

    def get_all_promotions(self):
        """
        Retrieves all promotions.
        Returns:
            list: A list of all Promotion objects.
        """
        return self.db_session.query(Promotion).all()

    def get_active_promotions(self):
        """
        Retrieves all currently active promotions.
        Returns:
            list: A list of active Promotion objects.
        """
        today = date.today()
        return self.db_session.query(Promotion).filter(
            Promotion.active == True,
            Promotion.start_date <= today,
            Promotion.end_date >= today
        ).all()

    def update_promotion(self, promotion_id, **kwargs):
        """
        Updates an existing promotion.
        Args:
            promotion_id (int): The ID of the promotion to update.
            **kwargs: Keyword arguments for the fields to update (e.g., name='New Name').
        Returns:
            Promotion: The updated Promotion object, or None if update fails or not found.
        """
        promotion = self.get_promotion_by_id(promotion_id)
        if promotion:
            try:
                for key, value in kwargs.items():
                    setattr(promotion, key, value)
                self.db_session.commit()
                return promotion
            except Exception as e:
                self.db_session.rollback()
                print(f"Error updating promotion {promotion_id}: {e}")
        return None

    def deactivate_promotion(self, promotion_id):
        """
        Deactivates a promotion.
        Args:
            promotion_id (int): The ID of the promotion to deactivate.
        Returns:
            bool: True if deactivated successfully, False otherwise.
        """
        promotion = self.get_promotion_by_id(promotion_id)
        if promotion:
            try:
                promotion.active = False
                self.db_session.commit()
                return True
            except Exception as e:
                self.db_session.rollback()
                print(f"Error deactivating promotion {promotion_id}: {e}")
        return False

    def delete_promotion(self, promotion_id):
        """
        Deletes a promotion from the database.
        Args:
            promotion_id (int): The ID of the promotion to delete.
        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        promotion = self.get_promotion_by_id(promotion_id)
        if promotion:
            try:
                self.db_session.delete(promotion)
                self.db_session.commit()
                return True
            except Exception as e:
                self.db_session.rollback()
                print(f"Error deleting promotion {promotion_id}: {e}")
        return False