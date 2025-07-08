from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
import os
from uuid import uuid4
from .models import User
from .dependencies import get_current_user
from fastapi import Depends

router = APIRouter(prefix="/api/upload", tags=["uploads"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("")
def upload(file: UploadFile = File(...),current_user: User = Depends(get_current_user), unsafe: bool = Query(False)):
    try:
        # Check allowed content types
        allowed_types = ["image/jpeg", "image/png", "application/octet-stream"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"File type '{file.content_type}' is not allowed.")

        # Extract extension and validate
        ext = os.path.splitext(file.filename)[1]
        if not ext:
            raise HTTPException(status_code=400, detail="Uploaded file has no extension.")

        # Determine filename and path
        filename = f"{uuid4().hex}{ext}"
        if unsafe:
            # ⚠️ For testing only: this allows path manipulation
            filepath = os.path.join(UPLOAD_DIR, file.filename)
        else:
            filepath = os.path.join(UPLOAD_DIR, filename)

        # Write file to disk
        with open(filepath, "wb") as f:
            f.write(file.file.read())

        return {
            "message": "File uploaded successfully",
            "url": f"{filepath}"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "An unexpected error occurred during upload.",
                "details": str(e)
            }
        )
