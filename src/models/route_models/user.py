from dataclasses import field
import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, validator, EmailStr

from src.models.general.user_constants import UserRoles

ALPHANUMERIC = r'^[a-zA-ZñÑ\s]+$'
PHONE_PREFIX = r'^\+[\d]{1,3}$'
FORMAT_DATE = r'^\d{4}-\d{2}-\d{2}$'


class SecurityQuestion(BaseModel):
    question: str = Field(...)
    answer: str = Field(...)


class UpdateUser(BaseModel):
    name: str = Field(None)
    last_name: str = Field(None)
    phone: int = Field(None)
    phone_prefix: str = Field(None)
    institution: str = Field(None)
    institution_role: str = Field(None)
    profession: str = Field(None)
    gender: str = Field(None)
    birthday: datetime = Field(None)
    role: UserRoles = Field(None)
    notify_removal: bool = Field(...)
    notify_simulation_done: bool = Field(...)

    class Config:
        fields = {
            'name': {'max_length': 64, 'regex': ALPHANUMERIC},
            'last_name': {'max_length': 64, 'regex': ALPHANUMERIC},
            'phone_prefix': {'regex': PHONE_PREFIX},
            'institution': {'max_length': 64, 'regex': ALPHANUMERIC},
            'institution_role': {'max_length': 64, 'regex': ALPHANUMERIC},
            'profession': {'max_length': 64, 'regex': ALPHANUMERIC},
            'gender': {'max_length': 1}
        }

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
    name: str = Field(...)
    last_name: str = Field(...)
    phone: int = Field(...)
    phone_prefix: str = Field(...)
    institution: str = Field(...)
    institution_role: str = Field(...)
    birthday: datetime = Field(...)
    email: EmailStr = Field(...)
    role: UserRoles = Field(None)
    password: str = Field(...)
    otp_code: str = Field(...)
    security_questions: List[SecurityQuestion] = Field(None)
