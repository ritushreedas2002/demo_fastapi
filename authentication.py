from fastapi import Depends, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "AUTHENTICATION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hash the password 'tim1234' and use it in the fake_db
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("tim1234")

fake_db = {
    "tim": {
        "username": "tim",
        "full_name": "Tim Russica",
        "email": "tim@gmail.com",
        "hashed_password": hashed_password,  # Use the hashed password here
        "disabled": False
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # OAuth2PasswordBearer(tokenUrl="token"): This creates an OAuth2PasswordBearer object that will be used to get the token from the request.

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy() # data.copy(): This creates a shallow copy of the data dict. This is done to prevent modifying the original data dict.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})    # to_encode.update({"exp": expire}): This adds an "exp" (expiration) claim to the data to encode.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # jwt.encode(): This function takes the data to encode and the secret key to encode it with. It also takes the algorithm to use for encoding.
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(fake_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)   #timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES): This creates a timedelta object that represents a duration of 30 minutes (since ACCESS_TOKEN_EXPIRE_MINUTES is set to 30).
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]