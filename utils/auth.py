from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from .schema import TokenData
from database.database_models import User
from dotenv import dotenv_values
from fastapi.security import HTTPBearer


config = dotenv_values(".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()

def verify_password(plain_password, hashed_password):
    """
    function will verify whether login password matches with hashed password found in database
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    plain text password will be hashed in order to be saved in the database
    """
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str):
    """
    user will be pulled from database by matching username input
    and inserted password will be verified whether it matches with hashed password in database
    or not. if passwords matches, user will have login allowed.
    """
    user = await User.get_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    access token will be created once user is allowed to login
    jwt token is created and encoded based on a secret_key and algorithm provided in your .env file
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    function pulls the current user logged in using jwt token information
    user id, username and full name are decoded from the token.
    user is returned from user id in encoded token
    """
    try:
        payload = jwt.decode(token.credentials, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        full_name: str = payload.get("full_name")
                
        if user_id is None:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials" )
        token_data = TokenData(id=user_id, username=username, full_name=full_name)
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
        )
    user = await User.get_by_id(token_data.id)
    if user is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials" )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    if token is no longer valid, session will be expired and user will not be returned
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Session expired")
    return current_user