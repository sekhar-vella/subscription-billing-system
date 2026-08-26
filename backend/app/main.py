from fastapi import FastAPI

from app.database import Base, engine
from app import models


# Create all database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Subscription Billing Automation System",
    description="Backend API for subscription and billing management",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Subscription Billing API is running"}