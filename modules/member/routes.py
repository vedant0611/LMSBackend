<<<<<<< HEAD
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
import modules.member.controllers as member_controller 
=======
from fastapi import APIRouter, Depends, HTTPException
import modules.member.controllers as member_controller
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
from modules.auth.routes import get_current_user

router = APIRouter()

@router.post("/book/borrow/{book_id}")
async def borrow_book(book_id: int, current_user: dict = Depends(get_current_user)):
<<<<<<< HEAD
    try:
        current_user_id = current_user.get("user_id")
        result = await member_controller.borrow_book(current_user_id, book_id)
        return result  # Assuming the controller returns a dict with success message
    except HTTPException as e:
        raise e  # Raise existing HTTPException
=======
    current_user_id = current_user.get("user_id")
    try:
        result = await member_controller.borrow_book(current_user_id, book_id)
        return result
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For Return the books
@router.post("/book/return/{book_id}")
async def return_book(book_id: int, current_user: dict = Depends(get_current_user)):
    try:
        result = await member_controller.return_book(book_id)
<<<<<<< HEAD
        return result  # Assuming the controller returns a dict with success message
    except HTTPException as e:
        raise e  # Raise existing HTTPException
=======
        return result
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For Delete my own account
@router.delete("/delete-account")
async def delete_account(current_user: dict = Depends(get_current_user)):
    current_user_id = current_user.get("user_id")
    try:
<<<<<<< HEAD
        current_user_id = current_user.get("user_id")
        result = await member_controller.delete_account(current_user_id)
        return result  # Assuming the controller returns a dict with success message
    except HTTPException as e:
        raise e  # Raise existing HTTPException
=======
        result = await member_controller.delete_account(current_user_id)
        return result
>>>>>>> fdec10d37796621e5322a61fa5a16b555aad2e2e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
