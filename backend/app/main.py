from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.database import Base, engine, SessionLocal
from app import models
from app.schemas import SignupRequest, SigninRequest
from datetime import datetime
from app.schemas import SubscriptionStatusUpdate
from app.schemas import PlanCreate
from app.schemas import PlanUpdate
from app.subscription_state import validate_status_transition
SECRET_KEY = "subscription-billing-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/signup")
def signup(
    user: SignupRequest,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
@app.post("/signin")
def signin(
    user: SigninRequest,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_correct = pwd_context.verify(
        user.password,
        existing_user.password_hash
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(existing_user.id)}
    )

    return {
        "message": "Signin successful",
        "access_token": access_token,
        "token_type": "bearer"
    }
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = (
        db.query(models.User)
        .filter(models.User.id == int(user_id))
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
@app.get("/home")
def home(current_user: models.User = Depends(get_current_user)):
    return {
        "message": f"Welcome {current_user.name}!",
        "user_id": current_user.id,
        "email": current_user.email
    }
@app.patch("/subscriptions/{subscription_id}/status")
def update_subscription_status(
    subscription_id: int,
    status_update: SubscriptionStatusUpdate,
    db: Session = Depends(get_db)
):
    subscription = (
        db.query(models.Subscription)
        .filter(models.Subscription.id == subscription_id)
        .first()
    )

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    old_status = subscription.status

    validate_status_transition(
        old_status,
        status_update.status
    )

    subscription.status = status_update.status
    subscription.status_changed_at = datetime.utcnow()

    db.commit()
    db.refresh(subscription)

    return {
        "message": "Subscription status updated successfully",
        "subscription_id": subscription.id,
        "old_status": old_status,
        "new_status": subscription.status,
        "status_changed_at": subscription.status_changed_at
    }
@app.post("/plans")
def create_plan(
    plan: PlanCreate,
    db: Session = Depends(get_db)
):
    new_plan = models.Plan(
        name=plan.name,
        price=plan.price,
        billing_interval=plan.billing_interval,
        trial_days=plan.trial_days,
        features=plan.features
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return {
        "message": "Plan created successfully",
        "plan_id": new_plan.id,
        "name": new_plan.name,
        "price": new_plan.price,
        "billing_interval": new_plan.billing_interval,
        "trial_days": new_plan.trial_days,
        "features": new_plan.features
    }
@app.get("/plans")
def list_plans(
    db: Session = Depends(get_db)
):
    plans = db.query(models.Plan).all()

    return plans
@app.put("/plans/{plan_id}")
def update_plan(
    plan_id: int,
    plan_data: PlanUpdate,
    db: Session = Depends(get_db)
):
    plan = (
        db.query(models.Plan)
        .filter(models.Plan.id == plan_id)
        .first()
    )

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    plan.name = plan_data.name
    plan.price = plan_data.price
    plan.billing_interval = plan_data.billing_interval
    plan.trial_days = plan_data.trial_days
    plan.features = plan_data.features

    db.commit()
    db.refresh(plan)

    return {
        "message": "Plan updated successfully",
        "plan_id": plan.id,
        "name": plan.name,
        "price": plan.price,
        "billing_interval": plan.billing_interval,
        "trial_days": plan.trial_days,
        "features": plan.features
    }
@app.patch("/plans/{plan_id}/archive")
def archive_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):
    plan = (
        db.query(models.Plan)
        .filter(models.Plan.id == plan_id)
        .first()
    )

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    plan.is_archived = True

    db.commit()
    db.refresh(plan)

    return {
        "message": "Plan archived successfully",
        "plan_id": plan.id,
        "is_archived": plan.is_archived
    }
@app.delete("/plans/{plan_id}")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):
    plan = (
        db.query(models.Plan)
        .filter(models.Plan.id == plan_id)
        .first()
    )

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    db.delete(plan)
    db.commit()

    return {
        "message": "Plan deleted successfully",
        "plan_id": plan_id
    }