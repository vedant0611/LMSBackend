from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

# Import necessary modules
import modules.database as database
from modules.auth.jwt_handler import get_current_user
import modules.auth.controllers as auth_controllers

router = APIRouter()

# Pydantic models for user registration and login
class UserRegistration(BaseModel):
    username: str
    password: str
    role: str  # Either 'LIBRARIAN' or 'MEMBER'

class UserLogin(BaseModel):
    username: str
    password: str

# Index route
@router.get("/")
async def index(current_user: dict = Depends(get_current_user)):
    try:
        return await auth_controllers.index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User signup route
@router.post("/signup")
async def signup(user_detail: UserRegistration):
    try:
        username = user_detail.username
        password = user_detail.password
        role = user_detail.role
        return await auth_controllers.signup(username=username, password=password, role=role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User login route
@router.post("/login")
async def login(user_detail: UserLogin):
    try:
        username = user_detail.username
        password = user_detail.password
        return await auth_controllers.login(username=username, password=password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
