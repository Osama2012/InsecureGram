from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from . import auth, users, upload, admin, ssrf, redirect,command,deprecated
import subprocess

subprocess.Popen(["uvicorn", "app.ssrf_server:app", "--port", "9000"])

app = FastAPI(title="InsecureGram")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(upload.router)
app.include_router(admin.router)
app.include_router(ssrf.router)
app.include_router(redirect.router)
app.include_router(command.router)
app.include_router(deprecated.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
