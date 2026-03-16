from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
import datetime

router = APIRouter()
SECRET_KEY = "icfa_secret_key"
ALGORITHM = "HS256"

# Simple in-memory user DB with plain text passwords (good enough for college project)
USERS_DB = {
    "admin": "admin123",
    "user1": "pass123",
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    stored_password = USERS_DB.get(data.username)
    if not stored_password or stored_password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode(
        {
            "sub": data.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": token, "username": data.username}

@router.get("/test")
def test():
    return {"message": "Auth route working!"}
