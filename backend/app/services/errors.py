class QueueError(Exception):
    """Base class for errors the API turns into HTTP responses."""


class NotFoundError(QueueError):
    """Something the request refers to does not exist (HTTP 404)."""


class ConflictError(QueueError):
    """The request is valid but not allowed in the current state (HTTP 409)."""
