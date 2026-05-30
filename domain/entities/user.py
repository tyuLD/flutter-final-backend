from pydantic import BaseModel, EmailStr

class UserEntity(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True

    class Config:
        from_attributes = True

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True
