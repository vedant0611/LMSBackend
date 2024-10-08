from fastapi.exceptions import HTTPException
from modules.database import db
from datetime import datetime


async def borrow_book(current_user_id,book_id):
    try:
        cur = db.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        insert_query = "INSERT INTO borrowed_books(book_id,user_id,borrowed_at) VALUES(%s,%s,%s)"
        cur.execute(insert_query,(book_id,current_user_id,current_timestamp))

        query = "UPDATE books SET status = 'BORROWED' WHERE id=%s"
        cur.execute(query,(book_id,))

        db.commit()
        cur.close()
        return HTTPException(status_code=200, detail=f"Book borrowed that has id: {book_id}")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

async def return_book(book_id):
    try:
        cur = db.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        update_query = "UPDATE books SET status = 'AVAILABLE' WHERE id=%s"
        cur.execute(update_query,(book_id,))

        query = "UPDATE borrowed_books SET returned_at=%s WHERE book_id=%s"
        cur.execute(query,(current_timestamp,book_id))

        db.commit()
        cur.close()
        return HTTPException(status_code=200, detail=f"Book returned that has id: {book_id}")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

async def delete_account(current_user_id):
    try:
        cur = db.cursor()
        query = "DELETE FROM users WHERE id=%s"
        cur.execute(query,(current_user_id,))
        db.commit()
        cur.close()
        return HTTPException(status_code=200, detail=f"You succesfully deleted your own account...!")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))