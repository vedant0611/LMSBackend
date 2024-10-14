from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
<<<<<<< HEAD
from jose import JWTError, jwt
=======
import jwt  # Using PyJWT for JWT encoding and decoding
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
from datetime import datetime, timedelta
from typing import Optional
from decouple import config
from fastapi.exceptions import HTTPException
<<<<<<< HEAD
import os

# Load secret key and algorithm from environment variables
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 10

# OAuth2 password bearer for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT access token with an expiration time.
    
    Args:
        data (dict): Data to encode in the token.
        expires_delta (Optional[timedelta]): Optional expiration time.
        
    Returns:
        str: The encoded JWT token.
    """
=======
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

<<<<<<< HEAD
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user from the JWT token.
    
    Args:
        token (str): The JWT token.
        
    Returns:
        dict: A dictionary containing user_id and user_role.
        
    Raises:
        HTTPException: If token validation fails.
    """
=======
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
<<<<<<< HEAD
=======
    
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        user_role: str = payload.get("role")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    return {"user_id": user_id, "user_role": user_role}
