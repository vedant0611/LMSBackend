from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

<<<<<<< HEAD
# Import necessary modules
=======
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
import modules.database as database
from modules.auth.jwt_handler import get_current_user
import modules.auth.controllers as auth_controllers

router = APIRouter()

<<<<<<< HEAD
# Pydantic models for user registration and login
=======
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
class UserRegistration(BaseModel):
    """Model for user registration details."""
    username: str
    password: str
<<<<<<< HEAD
    role: str  # Either 'LIBRARIAN' or 'MEMBER'
=======
    role: str   
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e

class UserLogin(BaseModel):
    """Model for user login credentials."""
    username: str
    password: str

<<<<<<< HEAD
# Index route
=======
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
@router.get("/")
async def index(current_user: dict = Depends(get_current_user)):
    """Welcome message for the library management system."""
    try:
        return await auth_controllers.index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

<<<<<<< HEAD
# User signup route
@router.post("/signup")
=======
@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
async def signup(user_detail: UserRegistration):
    """Endpoint for user registration."""
    try:
        username = user_detail.username
        password = user_detail.password
        role = user_detail.role
<<<<<<< HEAD
        return await auth_controllers.signup(username=username, password=password, role=role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User login route
@router.post("/login")
=======
        return await auth_controllers.signup(username, password, role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=dict)
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
async def login(user_detail: UserLogin):
    """Endpoint for user login."""
    try:
        username = user_detail.username
        password = user_detail.password
<<<<<<< HEAD
        return await auth_controllers.login(username=username, password=password)
=======
        return await auth_controllers.login(username, password)
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
