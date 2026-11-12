from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.services.errors import ConflictError, NotFoundError


def register_error_handlers(app: FastAPI):
    """Turn service-layer errors into proper HTTP responses, so routes don't
    need try/except around every call."""

    @app.exception_handler(NotFoundError)
    async def not_found(_: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ConflictError)
    async def conflict(_: Request, exc: ConflictError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})
