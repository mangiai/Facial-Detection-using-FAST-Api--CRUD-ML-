from pydantic import BaseModel, validator

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    email: str

    @validator('email')
    def email_must_be_valid(cls, value):
        if "@" not in value:
            raise ValueError('Email must be valid')
        return value

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    name: str



class Token(BaseModel):
    access_token: str
    token_type: str
