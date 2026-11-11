import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

API_TITLE = "EasyQueue API"

# Used when a service type has no duration on record
DEFAULT_SERVICE_DURATION = 15

# Service types created on startup if the service_types table is empty.
# (name, estimated duration in minutes)
DEFAULT_SERVICE_TYPES = [
    ("License Renewal", 10),
    ("Real ID", 20),
    ("Vehicle Registration", 15),
    ("Driving Test", 30),
    ("State ID", 10),
    ("Title Transfer", 15),
]

FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
