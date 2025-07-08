# app/admin.py

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
import pickle
from pydantic import BaseModel
from .dependencies import get_current_user

# Create an API router with the /admin prefix and tag it as "admin"
router = APIRouter(prefix="/api/admin", tags=["admin"])

# Accept a JSON body: { "payload": "<hex string>" }
class DeserializeRequest(BaseModel):
    payload: str

# Middleware-style dependency to validate admin access via X-API-KEY header
async def verify_admin(x_api_key: str = Header(None, alias="X-API-KEY")):
    if x_api_key != "admin123":  # Hardcoded admin key (intentionally insecure)
        raise HTTPException(status_code=403, detail="Forbidden")

# GET /admin/users - List all users with full info (including hashed passwords)
@router.get("/users")
async def list_users(current_user: User = Depends(get_current_user),admin=Depends(verify_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "is_admin": user.is_admin
        }
        for user in users
    ]

# POST /admin/deserialize - Insecure deserialization endpoint (vulnerable to RCE)
@router.post("/deserialize")
async def insecure_deserialize(
    data: DeserializeRequest,
    current_user: User = Depends(get_current_user),
    admin=Depends(verify_admin)
):
    try:
        obj = pickle.loads(bytes.fromhex(data.payload))

        # Decode bytes if the object is binary output (e.g., from subprocess.check_output)
        if isinstance(obj, bytes):
            return {"output": obj.decode("utf-8", errors="ignore")}
        return {"output": obj}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Deserialization failed: {str(e)}")
