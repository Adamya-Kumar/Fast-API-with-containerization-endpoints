from pydantic import BaseModel,EmailStr

# New User
class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    role:str

# Existing User
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
