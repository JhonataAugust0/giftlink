from pydantic import BaseModel, EmailStr, field_validator
import re

class UserRegistration(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        
        if not re.search(r'\d', password):
            raise ValueError('Senha deve conter pelo menos um número')
        
        if not re.search(r'[A-Z]', password):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        
        return password