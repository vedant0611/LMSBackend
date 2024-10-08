from fastapi import APIRouter, Depends, HTTPException
import modules.member.controllers as member_controller
from modules.auth.routes import get_current_user

router = APIRouter()

@router.post("/book/borrow/{book_id}")
async def borrow_book(book_id: int, current_user: dict = Depends(get_current_user)):
    current_user_id = current_user.get("user_id")
    try:
        result = await member_controller.borrow_book(current_user_id, book_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For Return the books
@router.post("/book/return/{book_id}")
async def return_book(book_id: int, current_user: dict = Depends(get_current_user)):
    try:
        result = await member_controller.return_book(book_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For Delete my own account
@router.delete("/delete-account")
async def delete_account(current_user: dict = Depends(get_current_user)):
    current_user_id = current_user.get("user_id")
    try:
        result = await member_controller.delete_account(current_user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
