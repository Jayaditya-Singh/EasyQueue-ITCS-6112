from enum import Enum


class QueueStatus(str, Enum):
    WAITING = "WAITING"
    CALLED = "CALLED"
    IN_SERVICE = "IN_SERVICE"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


# Entries with these statuses are still "in line" and count toward the queue
ACTIVE_STATUSES = (
    QueueStatus.WAITING.value,
    QueueStatus.CALLED.value,
    QueueStatus.IN_SERVICE.value,
)


class StaffActionType(str, Enum):
    CALLED = "CALLED"
    STARTED_SERVICE = "STARTED_SERVICE"
    COMPLETED_SERVICE = "COMPLETED_SERVICE"
    CUSTOMER_LEFT = "CUSTOMER_LEFT"
