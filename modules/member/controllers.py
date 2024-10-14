from fastapi import HTTPException
from modules.database import db
from datetime import datetime

async def borrow_book(current_user_id: int, book_id: int):
    cur = db.cursor()
    try:
        # Get the current timestamp
        current_timestamp = datetime.now()

        insert_query = "INSERT INTO borrowed_books (book_id, user_id, borrowed_at) VALUES (%s, %s, %s)"
        cur.execute(insert_query, (book_id, current_user_id, current_timestamp))

        query = "UPDATE books SET status = 'BORROWED' WHERE id = %s"
        cur.execute(query, (book_id,))

        db.commit()
        return {"detail": f"Book borrowed with id: {book_id}"}
    except Exception as e:
        db.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()  # Ensure the cursor is closed

async def return_book(book_id: int):
    cur = db.cursor()
    try:
        # Get the current timestamp
        current_timestamp = datetime.now()

        update_query = "UPDATE books SET status = 'AVAILABLE' WHERE id = %s"
        cur.execute(update_query, (book_id,))

        query = "UPDATE borrowed_books SET returned_at = %s WHERE book_id = %s"
        cur.execute(query, (current_timestamp, book_id))

        db.commit()
        return {"detail": f"Book returned with id: {book_id}"}
    except Exception as e:
        db.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()  # Ensure the cursor is closed

async def delete_account(current_user_id: int):
    cur = db.cursor()
    try:
        query = "DELETE FROM users WHERE id = %s"
        cur.execute(query, (current_user_id,))
        db.commit()
        return {"detail": "You successfully deleted your account!"}
    except Exception as e:
        db.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()  # Ensure the cursor is closed
