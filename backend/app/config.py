import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

DEFAULT_SERVICE_DURATION = 15

QUEUE_STATUSES = [
    "WAITING",
    "CALLED",
    "IN_SERVICE",
    "COMPLETED",
    "CANCELLED"
]

API_TITLE = "EasyQueue API"