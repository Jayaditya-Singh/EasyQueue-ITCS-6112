from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.customer_routes import router as customer_router
from app.api.errors import register_error_handlers
from app.api.queue_routes import router as queue_router
from app.api.service_routes import router as service_router
from app.api.staff_routes import router as staff_router
from app.config import API_TITLE, FRONTEND_ORIGINS
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Creates any missing tables and seeds service types, so a fresh database
    # works without running `python -m app.db.init_db` first.
    init_db()
    yield


app = FastAPI(title=API_TITLE, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

app.include_router(customer_router)
app.include_router(queue_router)
app.include_router(service_router)
app.include_router(staff_router)


@app.get("/")
def root():
    return {"message": "EasyQueue API Running"}
