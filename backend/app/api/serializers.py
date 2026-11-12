from datetime import timezone

from app.constants.enums import QueueStatus


def as_utc(value):
    """DB times are stored as naive UTC; mark them as UTC so browsers convert
    them to local time correctly."""
    if value is None:
        return None
    return value.replace(tzinfo=timezone.utc)


def queue_entry_to_dict(entry):
    """Flatten a QueueEntry plus its customer and service into API fields."""
    return {
        "queue_id": entry.queue_id,
        "customer_id": entry.customer_id,
        "customer_name": entry.customer.name if entry.customer else "",
        "service_type": entry.service.service_name if entry.service else "",
        "position": entry.position,
        "people_ahead": max(entry.position - 1, 0)
        if entry.status == QueueStatus.WAITING.value else 0,
        "status": entry.status,
        "estimated_wait_time": entry.estimated_wait_time or 0,
        "join_time": as_utc(entry.join_time),
    }
