from datetime import datetime, timedelta, timezone


def utc_now() -> datetime:
    """Naive UTC time, matching what the models store in DateTime columns."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def minutes_since(start: datetime | None) -> int:
    if start is None:
        return 0

    return max(int((utc_now() - start).total_seconds() // 60), 0)


def estimated_service_time(wait_minutes: int) -> datetime:
    return utc_now() + timedelta(minutes=wait_minutes)
