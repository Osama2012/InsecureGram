from fastapi import APIRouter, HTTPException, status, Depends, Form
from jose import jwt
from passlib.hash import bcrypt
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

class UserIn(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register")
def register(user: UserIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(username=user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = bcrypt.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw, is_admin=user.is_admin)
    db.add(new_user)
    db.commit()
    return {"message": f"User {user.username} registered successfully."}

@router.post("/login", response_model=Token)
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not bcrypt.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = jwt.encode({"sub": username, "is_admin": user.is_admin, "exp": datetime.utcnow() + timedelta(hours=1)}, settings.SECRET_KEY)
    return {"access_token": token, "token_type": "bearer"}