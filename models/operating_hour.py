# D:\PYTHON\Laserowo\P1_desktop_app\models\operating_hour.py

from sqlalchemy import Column, Integer, Time, Enum, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
import enum

# Make sure your Base is imported correctly from your database configuration
# Assuming your Base is defined in config/database.py like this:
# from sqlalchemy.orm import DeclarativeBase
# class Base(DeclarativeBase):
#    pass
from config.database import Base # Adjust if your Base is named differently or located elsewhere

# Define an Enum for days of the week for better data integrity
class DayOfWeek(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class OperatingHour(Base):
    """
    Represents the regular operating hours for the salon on a specific day of the week.
    """
    __tablename__ = 'operating_hours'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Using Enum for day of week ensures valid days
    day_of_week: Mapped[DayOfWeek] = mapped_column(
        Enum(DayOfWeek, name="day_of_week_enum"),
        nullable=False,
        unique=True # Assuming only one set of operating hours per day
    )
    
    open_time: Mapped[Optional[Time]] = mapped_column(Time, nullable=True)
    close_time: Mapped[Optional[Time]] = mapped_column(Time, nullable=True)
    
    # You might want a flag to indicate if the salon is closed on this day
    # rather than just having NULL times. For example, if open_time and close_time
    # are both NULL, it implies closed.
    is_closed: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self):
        if self.is_closed:
            return f"<OperatingHour(day_of_week='{self.day_of_week.value}', is_closed=True)>"
        return f"<OperatingHour(day_of_week='{self.day_of_week.value}', open_time='{self.open_time}', close_time='{self.close_time}')>"