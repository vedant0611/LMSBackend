from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from modules.database import db
from modules.auth.jwt_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def check_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def add_user(username: str, password: str, role: str) -> dict:
    with db.cursor() as cur:
        hashed_password = hash_password(password)

        cur.execute("SELECT COUNT(*) FROM users WHERE username=%s", (username,))
        exists = cur.fetchone()[0]

        if exists > 0:
            return {"response": False, "msg": "Username is already taken."}
        
        query = '''INSERT INTO users (username, password, role, created_at) VALUES (%s, %s, %s, %s)'''
        created_at = datetime.now()
        cur.execute(query, (username, hashed_password, role, created_at))
        db.commit()
        
        return {"response": True, "msg": f"Successfully registered as {role}."}

def validate_user(username: str, password: str) -> dict:
    """Check if the provided username and password are valid."""
    with db.cursor() as cur:
        cur.execute("SELECT id, password, role FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        if user:
            user_id, stored_password, role = user
            if check_password(password, stored_password):
                return {"response": True, "msg": "Login successful.", "user_id": user_id, "role": role}
            return {"response": False, "msg": "Invalid password."}

    return {"response": False, "msg": "Invalid username or password."}

async def home():
    """Welcome message for the library management system."""
    return {"Message": "Welcome to the Library Management System"}

async def register_user(username: str, password: str, role: str, created_at: datetime) -> None:

    try:
        result = add_user(username=username, password=password, role=role)

        if result['response']:
            raise HTTPException(status_code=200, detail=result['msg'])
        
        raise HTTPException(status_code=400, detail=result['msg'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def login_user(username: str, password: str):
    """Handle user login and token generation."""
    try:
        result = validate_user(username=username, password=password)
        
        if result['response']:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"user_id": result['user_id'], "role": result['role']}, expires_delta=expires_delta
            )
            raise HTTPException(status_code=200, detail=result['msg'], headers={"Authorization": access_token})
        
        raise HTTPException(status_code=401, detail=result['msg'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
