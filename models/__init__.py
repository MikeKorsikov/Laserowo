# P1_desktop_app/models/__init__.py

# Import all your model classes here so that Base.metadata.create_all()
# can discover them.
from . import client
from . import appointment
from . import service
from . import treatment_area
from . import payment_method
# Add any other model files you have:
# from . import another_model
# from . import yet_another_model

# Optionally, you can import the Base itself if other modules need it
# from .base import Base # If you define Base in a separate base.py