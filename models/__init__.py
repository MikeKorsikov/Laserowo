# models/__init__.py (or similar file that collects your models)
from .base import Base # Assuming base.py defines your Base
from .client import Client
from .appointment import Appointment
from .service import Service # Add this line
from .treatment_area import TreatmentArea # Add this line
from .payment_method import PaymentMethod # Add this line
# from .promotion import Promotion # Add if you define it
# from .hardware import Hardware # Add if you define it

# If you have a separate file that defines Base and imports all models,
# ensure these new models are imported there too.
# updated 