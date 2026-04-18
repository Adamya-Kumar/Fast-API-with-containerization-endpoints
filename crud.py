from fastapi import FastAPI,status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

app=FastAPI()

book=[
  {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "publish_date": "1925-04-10"
  },
  {
    "id": 2,
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "publish_date": "1960-07-11"
  },
  {
    "id": 3,
    "title": "1984",
    "author": "George Orwell",
    "publish_date": "1949-06-08"
  },
  {
    "id": 4,
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "publish_date": "1937-09-21"
  }
]

@app.get('/all/')
def get_all_book():
    return book


@app.get('/get_by_books')
def get_by_books(id:int):
    print(len(book))
    if id >= 4:
        raise  HTTPException(status_code=404,detail=f"input failed {id}")
    return book
    


@app.get("/book/{id}")
def get_book_by_id(id:int):
    for value in book:
        print(value['id'])
        if value['id'] == id:
            return value
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="failed 404")


class Book(BaseModel):
    id:int
    title:str
    author:str
    publish_date:str
    

@app.post("/add/book")
def add_book(new_book:Book):
    book.append(new_book)
    return book



@app.delete("/delete/book/{id}")
def delete_book_by_id(id:int):
    for value in book:
        if value['id'] == id:
            book.pop(value  )
            return {'message':"delete 200ok"}
    raise HTTPException(status_code=404,detail="failed")

class Book_Update(BaseModel):
    title:str
    author:str
    publish_date:str


@app.put('/update/{id}')
def update_book(id:int,book_update:Book_Update):
    for value in book:
        if value['id'] == id:
            value['id']=id
            value['title']=book_update.title
            value['author']=book_update.author
            value['publish_date']=book_update.publish_date
            return book
    raise HTTPException(status_code=404,detail="failed")