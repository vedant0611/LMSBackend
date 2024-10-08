from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

import modules.database as database
from modules.auth.jwt_handler import get_current_user
import modules.auth.controllers as auth_controllers

router = APIRouter()

class UserRegistration(BaseModel):
    """Model for user registration details."""
    username: str
    password: str
    role: str   

class UserLogin(BaseModel):
    """Model for user login credentials."""
    username: str
    password: str

@router.get("/")
async def index(current_user: dict = Depends(get_current_user)):
    """Welcome message for the library management system."""
    try:
        return await auth_controllers.index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def signup(user_detail: UserRegistration):
    """Endpoint for user registration."""
    try:
        username = user_detail.username
        password = user_detail.password
        role = user_detail.role
        return await auth_controllers.signup(username, password, role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=dict)
async def login(user_detail: UserLogin):
    """Endpoint for user login."""
    try:
        username = user_detail.username
        password = user_detail.password
        return await auth_controllers.login(username, password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
