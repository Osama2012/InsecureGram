from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import JWTError, jwt
from .database import get_db
from .models import User
from .config import settings
from .dependencies import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

# ✅ More realistic + obfuscated SQL Injection in /search
@router.get("/search")
def search_users(
    field: str = "username",
    keyword: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allowed_fields = ["username"]
    if field not in allowed_fields:
        raise HTTPException(400, "Invalid field")

    print(f"[*] Searching for '{keyword}' in field '{field}'")

    # 🧪 Try safe ORM query
    results = db.query(User).filter(text(f"LOWER({field}) LIKE :kw")).params(kw=f"%{keyword.lower()}%").all()
    if results:
        return [{"username": u.username, "is_admin": True if u.is_admin == 1 else False} for u in results]


    # ❌ Unsafe fallback with raw SQL
    try:
        print("[!] ORM search failed, falling back to raw SQL query")
        raw_sql = f"SELECT username, is_admin FROM users WHERE {field} = '{keyword}'"
        results = db.execute(text(raw_sql)).fetchall()
        return [{"username": u.username, "is_admin": True if u.is_admin == 1 else False} for u in results]
    except Exception as e:
        raise HTTPException(500, f"Raw query error: {e}")

# ✅ Protected profile endpoint
@router.get("/{user_id}")
def get_user_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(403, "Access denied")

    return {
        "id": user.id,
        "username": user.username,
        "is_admin": user.is_admin
    }
