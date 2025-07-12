# --- controllers/client_controller.py ---
from config.database import SessionLocal
from models.client import Client

class ClientController:
    def __init__(self):
        self.db = SessionLocal()

    def add_client(self, name, phone, email):
        new_client = Client(name=name, phone=phone, email=email)
        self.db.add(new_client)
        self.db.commit()
        return new_client

    def get_all_clients(self):
        return self.db.query(Client).all()