from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
import jwt  # Use PyJWT instead of jose
from datetime import datetime, timedelta
from typing import Optional
from decouple import config
from fastapi.exceptions import HTTPException
from decouple import config
import decouple
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Secret key to encode the JWT
SECRET_KEY = config("ryUMU2GT693WmUTPvScN6EnTbkkGlW2lzEUEAPXpXVI")
ALGORITHM = config("HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("10"))

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(credentials_exception)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        user_role: str = payload.get("role")
        if user_id is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    return {"user_id": user_id, "user_role": user_role}
