from fastapi import status
from fastapi.exceptions import HTTPException
from modules.database import db
from modules.auth.controllers import register_user
from datetime import datetime
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_books():
    try:
        cur = db.cursor()
        query = "SELECT * FROM books"
        cur.execute(query)
        all_books = cur.fetchall()
        return all_books
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

async def add_book(title,author,status,user_role):
    try:
        if user_role != "LIBRARIAN":
            return HTTPException(status_code=401, detail="This feature allow only for the Librarian...!")
        cur = db.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        query = '''INSERT INTO books(title,author,status,created_at) VALUES(%s, %s, %s, %s)'''
        cur.execute(query,(title,author,status,current_timestamp))
        db.commit()
        cur.close()
        return HTTPException(status_code=200, detail="Book succesfully added...!")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

async def update_book(book_id,title,author,status,user_role):
    try:
        if user_role != "LIBRARIAN":
            return HTTPException(status_code=401, detail="This feature allow only for the Librarian...!")
        
        cur = db.cursor()
        query = "UPDATE books SET title=%s,author=%s,status=%s WHERE id=%s"
        cur.execute(query,(title,author,status,book_id))
        db.commit()
        cur.close()
        return HTTPException(status_code=200, detail="Book succesfully updated...!")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

async def delete_book(book_id,user_role):
    try:
        if user_role != "LIBRARIAN":
            return HTTPException(status_code=401, detail="This feature allow only for the Librarian...!")
        
        cur = db.cursor()
        query = "DELETE FROM books WHERE id=%s"
        cur.execute(query,(book_id,))
        db.commit()
        cur.close()
        return HTTPException(status_code=200, detail=f"Book succesfully deleted that has id: {book_id}")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

async def add_member(username, password, user_role):
    try:
        if user_role != "LIBRARIAN":
            return HTTPException(status_code=401, detail="This feature allow only for the Librarian...!")
        
        role = "MEMBER"
        hashed_password = get_password_hash(password)

        # Get the current timestamp
        current_timestamp = datetime.now()

        res = register_user(username=username,password=hashed_password,role=role, created_at=current_timestamp)
        return HTTPException(status_code=200, detail="Member succesfully added...!")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

async def view_members(user_role):
    try:
        if user_role != "LIBRARIAN":
            return HTTPException(status_code=401, detail="This feature allow only for the Librarian...!")
        
        cur = db.cursor()
        query = "SELECT username,role,created_at FROM users WHERE role='MEMBER'"
        cur.execute(query)
        all_members = cur.fetchall()
        return all_members
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

async def delete_member(member_id,user_role):
    try:
        if user_role != "LIBRARIAN":
            return HTTPException(status_code=401, detail="This feature allow only for the Librarian...!")
        
        cur = db.cursor()
        query = "DELETE FROM users WHERE id=%s"
        cur.execute(query,(member_id,))
        db.commit()
        cur.close()
        return HTTPException(status_code=200, detail=f"Member succesfully removed that has id: {member_id}")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))