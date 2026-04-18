from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def welcome_root():
    return {"greeting":"good morning"}

@app.get('/about')
def read_root():
    return {"Message":"hello world"}

@app.get('/greet/')
def greet_name(name:str,age:Optional[int]=None):
    return {"message":f"Hello {name} you age is {age}"}


class Student(BaseModel):
    name: str
    age: Optional[int] = None
    grade: str

@app.post("/student/")
def create_student(student: Student):
    return {"name": student.name, "age": student.age, "grade": student.grade}
