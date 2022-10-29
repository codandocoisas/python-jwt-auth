import re
from uuid import UUID
from pydantic import BaseModel, validator, root_validator


class User(BaseModel):
    username: str
    email: str
    full_name: str
    
    @validator('username')
    def username_must_be_valid(cls, username: str) -> str:
        """
        method to validate username when creating an user.
        username must be between 4 and 16 characters, must not contain sequenced dashes nor underscores
        and will not allow characters different than a-z, A-Z, -, . or _
        """
        username = username.strip().lower()
        if not re.match("^[a-zA-Z0-9_.-]+$", username):
            raise ValueError('username is invalid')
        
        elif '--' in username or '__' in username:
            raise ValueError('username must not contain sequenced special characters')
        
        elif len(username) > 16 or len(username) < 4:
            raise ValueError('username length must be between 4 and 16 characters')
        
        return username
        
    @validator('full_name')
    def name_must_be_valid(cls, full_name: str) -> str:
        """
        full name must contain only a-z characters and a space
        """
        full_name = full_name.strip().title()
        if ' ' not in full_name or not re.match(r'^[a-zA-Z ]*$', full_name):
            raise ValueError('full name must have a space and only alpha characters')
        
        return full_name
    
    @validator('email')
    def email_must_be_valid(cls, email: str) -> str:
        """
        email may have alphanumeric, dot and underscore characters as well as at sign 
        """
        email = email.strip().lower()
        regex = r'^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
        
        if not (re.search(regex, email)):
            raise ValueError("Email is invalid")
        
        return email

        
    class Config:
        orm_mode = True
    

class UserRegistration(User):
    password: str 
    confirm_password: str
        
    @root_validator
    def check_passwords_match(cls, values):
        """
        whenever user is being registered both password and password confirmation must be the same.
        values are being directly passed through UserRegistration Model
        """
        password, confirm_password = values.get('password'), values.get('confirm_password')
        if password is not None and confirm_password is not None and password != confirm_password:
            raise ValueError('passwords do not match')
        
        return values
    
    @validator('password')
    def check_password_strenght(cls, password:str) -> str:
        """
        password has to meet the following requirements:
        at least 1 lowercase character, 1 uppercase character, 1 digit, 1 special character and be
        at least 8 characters long
        """
        regex = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})"
        if not (re.search(regex, password)):
            raise ValueError("password does not meet the criteria")
        
        return password
        

class UserCreated(BaseModel):
    id: UUID

class UserLogin(BaseModel):
    username: str
    password: str
    
class TokenData(BaseModel):
    id: str
    username: str
    full_name: str
    
class Token(BaseModel):
    access_token: str
    token_type: str