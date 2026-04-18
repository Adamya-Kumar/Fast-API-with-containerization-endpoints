from fastapi import FastAPI,Depends
from database import get_db,engine
from sqlalchemy.orm import Session
import model
from  pydantic import BaseModel
from sqlalchemy import delete

app=FastAPI()

class BookStore(BaseModel):
    id:int
    title:str
    author:str
    publish_date:str
    
@app.post('/book')
def add_book(book:BookStore,db:Session=Depends(get_db)):
    new_book = model.Book(title=book.title,author=book.author,publish_date=book.publish_date)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book



@app.get('/all/books')
def all_books(db:Session=Depends(get_db)):
    book = db.query(model.Book).all()
    return book



@app.put('/update/book/{book_id}')
def update_book_by_id(book_id:int,updated_book:BookStore,db:Session=Depends(get_db)):
    book=db.query(model.Book).get(book_id)
    if book:
        # Update existing
        book.title = updated_book.title
    else:
        # Create new if it doesn't exist
        book = model.Book(book)
        db.add(book)
    db.commit()
    return {"Message":f"update book {book_id}"}

@app.delete('/delete/{book_id}')
def delete_book_by_id(book_id:int,db:Session=Depends(get_db)):
    db.execute(delete(model.Book).where(model.Book.id == book_id))
    db.commit()
    return {"Message":f"Delete {book_id}"}