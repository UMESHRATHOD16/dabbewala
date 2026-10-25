from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables

from routes.orders import router as orders_router
from routes.stats import router as stats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Databse tables created")
    yield
    print("Application shutdown.")

app = FastAPI(
    title="Dabbewala Delivery Management API",
    description="This is a project to manage the delivery of food and other items in a city",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(orders_router)
app.include_router(stats_router)

@app.get("/")
def root():
    return {
        "message" : "Project Dabbewala is serving.",
        "description" : "This is a project to manage the delivery of food and other items in a city using a network of delivery personnel called Dabbewalas."
    }

@app.get("/health", tags=["health"])
def health_check():
    return {
        "status" : "healthy",
        "message" : "The API is running and healthy."
    }