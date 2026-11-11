from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.customer_routes import router as customer_router
from app.api.queue_routes import router as queue_router
from app.api.staff_routes import router as staff_router
from app.config import API_TITLE

app = FastAPI(title=API_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_router)
app.include_router(queue_router)
app.include_router(staff_router)

@app.get("/")
def root():
    return {"message": "EasyQueue API Running"}
