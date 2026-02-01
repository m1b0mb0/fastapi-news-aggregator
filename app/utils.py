import bcrypt
import os
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta, timezone

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def verify_pwd(plain_pwd: str, hashed_pwd: str):
    return bcrypt.checkpw(
        plain_pwd.encode("utf-8"),
        hashed_pwd.encode("utf-8"),
    ) 

def get_pwd_hash(pwd: str):
    return bcrypt.hashpw(
        pwd.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8") 

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

