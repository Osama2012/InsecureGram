from fastapi import APIRouter, Query
import requests
from .models import User
from .dependencies import get_current_user
from fastapi import Depends

router = APIRouter(prefix="/api/proxy", tags=["ssrf"])

@router.get("")
def proxy(url: str = Query(...),current_user: User = Depends(get_current_user)):
    try:
        r = requests.get(url, timeout=2)
        return {"status_code": r.status_code, "content": r.text[:200]}
    except Exception as e:
        return {"error": str(e)}