import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, validator, EmailStr

ALPHANUMERIC = r'^[a-zA-ZñÑ\s]+$'
PHONE_PREFIX = r'^\+[\d]{1,3}$'
FORMAT_DATE = r'^\d{4}-\d{2}-\d{2}$'


class SecurityQuestion(BaseModel):
    question: str = Field(...)
    answer: str = Field(...)


class UpdateUser(BaseModel):
    name: str = Field(None, max_length=64, regex=ALPHANUMERIC)
    last_name: str = Field(None, max_length=64, regex=ALPHANUMERIC)
    phone: int = Field(None)
    phone_prefix: str = Field(None, regex=PHONE_PREFIX)
    institution: str = Field(None, max_length=64, regex=ALPHANUMERIC)
    institution_role: str = Field(None, min_length=3, regex=ALPHANUMERIC)
    profession: str = Field(None, min_length=3, regex=ALPHANUMERIC)
    gender: str = Field(None, max_length=1)
    birthday: datetime = Field(None)

    @validator('gender')
    def validate_gender(cls, value: str):
        genders = ['F', 'M']
        if value.upper() in genders:
            return value.upper()
        raise ValueError('Invalid Type, gender must be F, M')

    @validator('birthday', pre=True)
    def validate_birthday(cls, value):
        if re.search(FORMAT_DATE, value):
            return value + 'T00:00'
        return value


class NewUser(UpdateUser):
    name: str = Field(..., max_length=64, regex=ALPHANUMERIC)
    last_name: str = Field(..., max_length=64, regex=ALPHANUMERIC)
    phone: int = Field(...)
    phone_prefix: str = Field(..., regex=PHONE_PREFIX)
    institution: str = Field(..., max_length=64, regex=ALPHANUMERIC)
    institution_role: str = Field(..., min_length=3, regex=ALPHANUMERIC)
    birthday: datetime = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    security_questions: List[SecurityQuestion] = Field(None)
