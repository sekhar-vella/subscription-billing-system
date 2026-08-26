from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.database import Base, engine, SessionLocal
from app import models
from app.schemas import SignupRequest, SigninRequest
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