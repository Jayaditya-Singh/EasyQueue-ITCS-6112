from fastapi import FastAPI

from app.api.customer_routes import router as customer_router
from app.api.queue_routes import router as queue_router
from app.api.staff_routes import router as staff_router

app = FastAPI(title="EasyQueue API")

app.include_router(customer_router)
app.include_router(queue_router)
app.include_router(staff_router)

@app.get("/")
def root():
    return {"message": "EasyQueue API Running"}