import subprocess
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from .dependencies import get_current_user
from .models import User  # Assuming User model is defined in models.py

router = APIRouter()

@router.get("/api/cmd/exec")
def execute(cmd: str = Query(..., description="Command to execute"),current_user: User = Depends(get_current_user)):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5)
        return JSONResponse(content={"output": result.decode()}, status_code=200)
    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": e.output.decode()}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
