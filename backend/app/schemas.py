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
class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    company_name: str | None = None


class CustomerUpdate(BaseModel):
    name: str
    email: EmailStr
    company_name: str | None = None
class SubscriptionCreate(BaseModel):
    customer_id: int
    plan_id: int
class SubscriptionChangePlan(BaseModel):
    plan_id: int