# ssrf_target.py
from fastapi import FastAPI, Query
from pathlib import Path
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/read")
def read_file(name: str = Query(..., description="Path to the file to read")):
    try:
        path = Path(name)

        if not path.exists():
            return JSONResponse(
                status_code=404,
                content={"error": "File not found", "path": str(path)}
            )

        if path.is_dir():
            return JSONResponse(
                status_code=400,
                content={"error": "Path is a directory, not a file", "path": str(path)}
            )

        content = path.read_text(errors="ignore")
        return JSONResponse(
            status_code=200,
            content={
                "message": "File read successfully",
                "file": str(path),
                "content": content
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "An unexpected error occurred while reading the file",
                "details": str(e),
                "path": name
            }
        )
