from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from auth import model,schemas,utils
from auth.auth_database import get_db,engine
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import JWTError


model.Base.metadata.create_all(bind=engine)

SECRET_KEY="v-4EP_L84V6PFSTbMpEXmPpqS1upeRNaUIBUdvjopQU"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MIN=30

# Helper function
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({'exp':expire})
    encode_jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt_token


app=FastAPI()


@app.post('/signup')
def craete_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
     existing_user = db.query(model.User).filter(model.User.email == user.email).first()
     if existing_user:
         raise HTTPException(status_code=400,detail="Username or email already exist.")

     
     hashing_password = utils.hash_password(user.password)
     new_user = model.User(
         username=user.username,
         email=user.email,
         hashed_password=hashing_password,
         role=user.role
     )
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     # error may be occur
     user_data = user.model_dump(exclude={"password"})
     return user_data
 

@app.post('/login')
# 1. Added Depends() here
def vertiy_user(frorm_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # 2. Changed frorm_data.email to frorm_data.username
    user = db.query(model.User).filter(model.User.email == frorm_data.username).first()
    
    if not user:
        # Use 403 Forbidden or 401 Unauthorized for security
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify_password(frorm_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    token_data = {'sub': user.email, 'role': user.role}
    token = create_access_token(token_data)
    
    return {'access_token': token, 'token_type': "bearer"}

 


@app.get("/", response_class=HTMLResponse)
def welcome():
    return "<h1>Welcome to Auth API !</h1>"



oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(token:str = Depends(oauth2_scheme)):
    credential_excception = HTTPException(status_code=401,detail="Could not validate credentia!")
    header = {'WWW-Authenticate':"Bearer"}
    try:
        payload= jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username:str =  payload.get('sub')
        role:str = payload.get('role')
        if username is None or role is None:
            raise credential_excception
    except JWTError:
        raise credential_excception

    return {"username":username,"role":role}



@app.get('/protected')
def protected_route(current_user:dict=Depends(get_current_user)):
    return {"Messsage":f"Hello, My name is {current_user['username']} | Access Passed "}

def validate_roles(allowed_roles:list[str]):
    def role_checking(current_user:dict=Depends(get_current_user)):
        current_user_role = current_user.get('role')
        if current_user_role not in allowed_roles:
            raise HTTPException(status_code=403,detail="Not Allowed to Access")
        
        return current_user
    return role_checking

@app.get('/profile')
def profile_route(current_user:dict=Depends(validate_roles(['user','admin']))):
    return {"Message":f" role {current_user['role']}"}

@app.get('/user/dashboard')
def profile_route(current_user:dict=Depends(validate_roles(['user']))):
    return {"Message":f"Welcome to {current_user['role']} Dashboard"}

@app.get('/admin/dashboard')
def profile_route(current_user:dict=Depends(validate_roles(['admin']))):
    return {"Message":f"Welcome to {current_user['role']} Dashboard"}