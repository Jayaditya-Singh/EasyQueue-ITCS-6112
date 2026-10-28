from enum import Enum

class QueueStatus(str, Enum):
    WAITING = "WAITING"
    CALLED = "CALLED"
    IN_SERVICE = "IN_SERVICE"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"