from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from .models import User
from .dependencies import get_current_user
from fastapi import Depends

router = APIRouter(prefix="/api/redirect", tags=["redirect"])

@router.get("")
def redirect(target: str = Query(...),current_user: User = Depends(get_current_user)):
    return RedirectResponse(url=target)