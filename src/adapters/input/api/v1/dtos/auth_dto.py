from pydantic import BaseModel, Field

from src.adapters.input.api.v1.dtos.people_dto import PeopleResponseDTO
from src.domain.models.people import People

from src.adapters.output.data.orm.entities.orm_entities import Grupos
from src.domain.models.group import Group

class LoginRequestDTO(BaseModel):
    username: str = Field(..., example="joao.silva@gmail.com")
    password: str = Field(..., example="123456")
    grant_type: str = Field(..., example="password") 


class LoginResponseDTO(BaseModel):
    token: str = Field(..., example="")
    user: PeopleResponseDTO

    @classmethod
    def from_domain(cls, user: People, token: str):
        return cls(
            token=token,
            user=PeopleResponseDTO.from_domain(user)
        )


class RegisterRequestDTO(BaseModel):
    name: str = Field(..., example="")
    email: str = Field(..., example="")
    password: str = Field(..., example="")
    group: str = Field(..., example="")

    @classmethod
    def to_domain(cls, user: People):
        return People(
            name=user.name,
            email=user.email,
            password=user.password,
            group=Group(name=user.group)
        )
    
    def from_domain(cls, user: People):
        return cls(
            name=user.name,
            email=user.email,
            password=user.password,
            group=user.group.name
        )
    
class RegisterResponseDTO(BaseModel):
    user: PeopleResponseDTO

    @classmethod
    def from_domain(cls, user: People):
        return cls(
            user=PeopleResponseDTO.from_core(user)
        )