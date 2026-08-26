from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
class SigninRequest(BaseModel):
    email: EmailStr
    password: str
class SubscriptionStatusUpdate(BaseModel):
    status: str
class PlanCreate(BaseModel):
    name: str
    price: float
    billing_interval: str
    trial_days: int
    features: dict | None = None
class PlanUpdate(BaseModel):
    name: str
    price: float
    billing_interval: str
    trial_days: int
    features: dict | None = None