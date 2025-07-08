from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .dependencies import get_current_user
from .models import User

router = APIRouter(prefix="/api/v1")

@router.get("/users/info")
def legacy_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch fresh user data from DB
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "version": "v1",
        "user": {
            "id": user.id,
            "username": user.username,
            "password": user.hashed_password, 
            "is_admin": user.is_admin
        },
        "info": "Legacy endpoint still running"
    }
