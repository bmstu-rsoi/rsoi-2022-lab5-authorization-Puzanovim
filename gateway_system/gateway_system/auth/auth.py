from datetime import datetime, timedelta
from typing import Dict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from gateway_system.auth.schemas import TokenData, UserInDB
from jose import JWTError
from passlib.context import CryptContext

SECRET_KEY = 'h7VxtcEoiJCxNDs9jRSDRlwGLjLpbpaw'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


authenticated_users_db = {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Dict, username: str, password: str):
    user_dict = {'username': username, 'hashed_password': get_password_hash(password)}
    db[username] = user_dict
    return UserInDB(**user_dict)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        user = create_user(db, username, password)
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
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
    user = get_user(authenticated_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
