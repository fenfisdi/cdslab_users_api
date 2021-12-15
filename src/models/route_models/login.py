from pydantic import BaseModel, Field, EmailStr


class UserCredentials(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
