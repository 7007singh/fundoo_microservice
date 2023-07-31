import re
from pydantic import BaseModel, EmailStr, field_validator, constr, Field


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    email: EmailStr

    @field_validator('password')
    def validate_password(cls, value):
        if not re.match('^[a-zA-Z0-9]+$', value):
            raise ValueError
        return value

    @field_validator('password')
    def validate_username(cls, value):
        if not re.match('^[a-zA-Z0-9]+$', value):
            raise ValueError
        return value

    @field_validator('password')
    def validate_first_name(cls, value):
        if not re.match("^[A-Z]{1,}[a-z]{2,}", value):
            raise ValueError
        return value

    @field_validator('password')
    def validate_last_name(cls, value):
        if not re.match("^[A-Z]{1,}[a-z]{2,}", value):
            raise ValueError
        return value


class Login(BaseModel):
    username: str = Field(..., min_length=1, description="Username must not be empty")
    password: str = Field(..., min_length=1, description="Password must not be empty")
