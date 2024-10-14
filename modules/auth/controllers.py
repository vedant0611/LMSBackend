from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from modules.database import db
from modules.auth.jwt_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

<<<<<<< HEAD
# Password hashing setup
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# Hash a plain-text password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify the provided password against the stored hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def register_user(username: str, password: str, role: str, created_at: datetime):
    cur = db.cursor()
    hashed_password = get_password_hash(password)

    # Check if username already exists in the database
    select_query = "SELECT COUNT(*) FROM users WHERE username=%s"
    cur.execute(select_query, (username,))
    count = cur.fetchone()[0]

    if count > 0:
        return {"response": False, "msg": "Username already exists."}
    else:
        query = '''INSERT INTO users(username, password, role, created_at) VALUES(%s, %s, %s, %s)'''
        cur.execute(query, (username, hashed_password, role, created_at))
        db.commit()
        cur.close()
        return {"response": True, "msg": f"Successfully registered as {role}"}

def is_valid(username: str, password: str):
    cur = db.cursor()

    # Check if username exists in the database
    select_query = "SELECT * FROM users WHERE username=%s"
    cur.execute(select_query, (username,))
    user = cur.fetchone()

    if user:
        user_id = user[0]
        hashed_password = user[2]
        role = user[3]
        is_password_valid = verify_password(password, hashed_password)
        if is_password_valid:
            return {"response": True, "msg": "Successfully logged in.", "user_id": user_id, "role": role}
        else:
            return {"response": False, "msg": "Invalid password."}
    return {"response": False, "msg": "Invalid username or password."}

async def index():
    try:
        return {"message": "Welcome to the Library Management System"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def signup(username: str, password: str, role: str):
    try:
        current_timestamp = datetime.now()
        res = register_user(username=username, password=password, role=role, created_at=current_timestamp)

        if res['response']:
            return {"status": 200, "message": res['msg']}
        raise HTTPException(status_code=400, detail=res['msg'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def login(username: str, password: str):
    try:
        res = is_valid(username=username, password=password)

        if res['response']:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"user_id": res['user_id'], "role": res['role']}, expires_delta=access_token_expires
            )
            return {"status": 200, "message": res['msg'], "access_token": access_token}
        raise HTTPException(status_code=401, detail=res['msg'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
=======
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
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
