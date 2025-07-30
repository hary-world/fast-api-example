import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")


class UserCreate(UserBase):
    password: str = Field(
        ..., min_length=8, max_length=100, description="User's password"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty or just whitespace")
        if not re.match(r"^[a-zA-Z\s]+$", v.strip()):
            raise ValueError("Name can only contain letters and spaces")
        return v.strip().title()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserResponse(UserBase):
    id: int = Field(..., description="User's unique identifier")

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=2, max_length=50, description="User's full name"
    )
    email: Optional[EmailStr] = Field(None, description="User's email address")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Name cannot be empty or just whitespace")
            if not re.match(r"^[a-zA-Z\s]+$", v.strip()):
                raise ValueError("Name can only contain letters and spaces")
            return v.strip().title()
        return v


class User(UserBase):
    id: int
    password: str

    class Config:
        from_attributes = True
