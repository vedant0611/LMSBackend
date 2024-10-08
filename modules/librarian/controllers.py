from fastapi import status, HTTPException
from modules.database import db
from modules.auth.controllers import register_user
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a hashed password against a plain password."""
    return pwd_context.verify(plain_password, hashed_password)

async def get_books():
    """Retrieve all books from the database."""
    try:
        cur = db.cursor()
        query = "SELECT * FROM books"
        cur.execute(query)
        all_books = cur.fetchall()
        cur.close()
        return all_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def add_book(title: str, author: str, status: str, user_role: str):
    """Add a new book to the database."""
    if user_role != "LIBRARIAN":
        raise HTTPException(status_code=401, detail="Only librarians can add books.")
    
    try:
        cur = db.cursor()
        current_timestamp = datetime.now()

        query = '''INSERT INTO books(title, author, status, created_at) VALUES(%s, %s, %s, %s)'''
        cur.execute(query, (title, author, status, current_timestamp))
        db.commit()
        cur.close()
        return {"detail": "Book successfully added."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_book(book_id: int, title: str, author: str, status: str, user_role: str):
    """Update an existing book's details."""
    if user_role != "LIBRARIAN":
        raise HTTPException(status_code=401, detail="Only librarians can update books.")
    
    try:
        cur = db.cursor()
        query = "UPDATE books SET title=%s, author=%s, status=%s WHERE id=%s"
        cur.execute(query, (title, author, status, book_id))
        db.commit()
        cur.close()
        return {"detail": "Book successfully updated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_book(book_id: int, user_role: str):
    """Delete a book from the database."""
    if user_role != "LIBRARIAN":
        raise HTTPException(status_code=401, detail="Only librarians can delete books.")
    
    try:
        cur = db.cursor()
        query = "DELETE FROM books WHERE id=%s"
        cur.execute(query, (book_id,))
        db.commit()
        cur.close()
        return {"detail": f"Book successfully deleted with ID: {book_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def add_member(username: str, password: str, user_role: str):
    """Add a new member to the library."""
    if user_role != "LIBRARIAN":
        raise HTTPException(status_code=401, detail="Only librarians can add members.")
    
    try:
        role = "MEMBER"
        hashed_password = get_password_hash(password)
        current_timestamp = datetime.now()

        await register_user(username=username, password=hashed_password, role=role, created_at=current_timestamp)
        return {"detail": "Member successfully added."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def view_members(user_role: str):
    """View all members of the library."""
    if user_role != "LIBRARIAN":
        raise HTTPException(status_code=401, detail="Only librarians can view members.")
    
    try:
        cur = db.cursor()
        query = "SELECT username, role, created_at FROM users WHERE role='MEMBER'"
        cur.execute(query)
        all_members = cur.fetchall()
        cur.close()
        return all_members
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_member(member_id: int, user_role: str):
    """Delete a member from the library."""
    if user_role != "LIBRARIAN":
        raise HTTPException(status_code=401, detail="Only librarians can delete members.")
    
    try:
        cur = db.cursor()
        query = "DELETE FROM users WHERE id=%s"
        cur.execute(query, (member_id,))
        db.commit()
        cur.close()
        return {"detail": f"Member successfully removed with ID: {member_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
