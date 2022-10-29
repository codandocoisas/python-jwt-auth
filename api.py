from datetime import timedelta
from asyncpg import UniqueViolationError
from fastapi import Depends, FastAPI, HTTPException, status
from utils.auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash
from utils.schema import UserCreated, UserRegistration, UserLogin, Token, User as SchemaUser
from database.database_models import User as ModelUser
from utils.helper import generate_uuid
from dotenv import dotenv_values
from fastapi.security import HTTPBearer


config = dotenv_values(".env")
oauth2_scheme = HTTPBearer()

app = FastAPI()

@app.post("/register", response_model=UserCreated, status_code=201)
async def register_user(user_register: UserRegistration) -> UserCreated:
    """
    endpoint will receive an User based on UserRegistration Model via JSON post request
    and it will generated a hashed password and a new uuid for the user
    which will be inserted into the database. Only the id will be returned on the response.
    """
    try:
        hashed_password = get_password_hash(user_register.password)    
        id = await generate_uuid()    
            
        user = await ModelUser.create(**{
            'id': id,
            'username': user_register.username, 
            'email': user_register.email, 
            'full_name': user_register.full_name, 
            'hashed_password': hashed_password})
        
        if user:
            return user
        raise HTTPException(status_code=400, content={"error": "Not able to create user"})
    except UniqueViolationError as e:
        raise HTTPException(status_code=400, detail={ "error": e.as_dict()["message"], "field": e.as_dict()["constraint_name"]})

@app.post("/login", response_model=Token)
async def login_for_access_token(login: UserLogin) -> Token:
    """
    endpoint will receive User credentials from UserLogin model and will attempt to login
    using credentials provided through authenticate_user function.
    Bearer access token will return if authentication was successfull 
    """
    user = await authenticate_user(login.username, login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password")
        
    access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "full_name": user.full_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer" }


@app.get("/users/me/", response_model=SchemaUser)
async def read_users_me(current_user: SchemaUser = Depends(get_current_active_user)) -> SchemaUser:
    """
    endpoint will only return the current active user based on Authorization and if a valid JWT token is provided
    """
    return current_user