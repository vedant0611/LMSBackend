from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import modules.librarian.controllers as librarian_controller 
from modules.auth.jwt_handler import get_current_user

router = APIRouter()


class Book(BaseModel):
    title: str
    author: str

class UpdateBookDetail(BaseModel):
    title: str
    author: str
    status: str

@router.get("/books")
async def get_books():
    books = await librarian_controller.get_books()
    return books

    return await librarian_controller.get_books()


# For Add the Book
@router.post("/book")
async def add_book(book_detail: Book, current_user: dict = Depends(get_current_user)):
    title = book_detail.title
    author = book_detail.author
    status = "AVAILABLE"
    user_role = current_user.get("user_role")
    result = await librarian_controller.add_book(title, author, status, user_role)
    if isinstance(result, HTTPException):
        raise result
    return result
    return await librarian_controller.add_book(title, author, status, user_role)

@router.patch("/book/update/{book_id}")
async def update_book(book_id: int, updateBookDetail: UpdateBookDetail, current_user: dict = Depends(get_current_user)):
    title = updateBookDetail.title
    author = updateBookDetail.author
    status = updateBookDetail.status
    user_role = current_user.get("user_role")

    result = await librarian_controller.update_book(book_id, title, author, status, user_role)
    if isinstance(result, HTTPException):
        raise result
    return result
    return await librarian_controller.update_book(book_id, title, author, status, user_role)

@router.delete("/book/delete/{book_id}")
async def delete_book(book_id: int, current_user: dict = Depends(get_current_user)):
    user_role = current_user.get("user_role")
    result = await librarian_controller.delete_book(book_id, user_role)
    if isinstance(result, HTTPException):
        raise result
    return result

# ************************************** Manage of Members *****************************************

    return await librarian_controller.delete_book(book_id, user_role)

class MemberDetail(BaseModel):
    username: str
    password: str

@router.get("/view/members")
async def view_members(current_user: dict = Depends(get_current_user)):
    user_role = current_user.get("user_role")
    result = await librarian_controller.view_members(user_role)
    if isinstance(result, HTTPException):
        raise result
    return result
    return await librarian_controller.view_members(user_role)

@router.post("/add/member")
async def add_member(member_detail: MemberDetail, current_user: dict = Depends(get_current_user)):
    username = member_detail.username
    password = member_detail.password
    user_role = current_user.get("user_role")
    result = await librarian_controller.add_member(username, password, user_role)
    if isinstance(result, HTTPException):
        raise result
    return result
    return await librarian_controller.add_member(username, password, user_role)

@router.delete("/member/delete/{member_id}")
async def delete_member(member_id: int, current_user: dict = Depends(get_current_user)):
    user_role = current_user.get("user_role")
    result = await librarian_controller.delete_member(member_id, user_role)
    if isinstance(result, HTTPException):
        raise result
    return result
    return await librarian_controller.delete_member(member_id, user_role)
