from pydantic import BaseModel, EmailStr
from typing import Dict

class SignUpSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

