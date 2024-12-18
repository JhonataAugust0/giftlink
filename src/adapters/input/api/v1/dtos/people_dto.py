from pydantic import BaseModel, Field

from src.adapters.output.data.orm.entities.orm_entities import Pessoa
from src.domain.models.people import People

class PeopleResponseDTO(BaseModel):
    id:                 int = Field(..., ge=0, description="Id da pessoa")
    name:               str = Field(..., max_length=100, description="name da pessoa")
    group_id:           int = Field(..., ge=0, description="Id do grupo")
    sugestao_presente:  str = Field(..., max_length=100, description="Sugestão de presente")
    codigo:             int = Field(..., description="Código da pessoa")
    email:              str = Field(..., max_length=100, description="Email da pessoa")
    is_active:             bool = Field(..., description="Se a pessoa está ativa")
    sorteio_id:         int | None = Field(None, description="Id do sorteio")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 2,
                "name": "Leo",
                "group_id": 29,
                "sugestao_presente": "Um livro",
                "codigo": 1598,
                "email": "joao.silva@gmail.com",
                "ativa": True,
                "sorteio_id": 1,
            }
        }

    @staticmethod
    def from_core(people: Pessoa):
        return PeopleResponseDTO(
            id=people.id,
            name=people.nome,
            codigo=people.codigo,
            group_id=people.grupo_id,
            sugestao_presente=people.sugestao_presente,
            sorteio_id=people.sorteio_id,
            email=people.email,
            is_active=people.ativa
        )


class PeopleRequestDTO(BaseModel):
    group_id:           int = Field(..., ge=0, description="Id do grupo")
    name:               str = Field(..., max_length=100, description="name da pessoa")
    sugestao_presente:  str = Field(..., max_length=100, description="Sugestão de presente")
    email:              str = Field(..., max_length=100, description="Email da pessoa")
    password:           str = Field(..., max_length=100, description="Senha")


    class Config:
        json_schema_extra = {
            "example": {
                "name": "Leo",
                "group_id": 29,
                "sugestao_presente": "Um livro",
                "email": "joao.silva@gmail.com",
                "password": "123456",
            }
        }

    def to_core(self) -> People:
        return People(
            name=self.name,
            group_id=self.group_id,
            gift_suggestion=self.sugestao_presente,
            email=self.email,
            hashed_password=self.password
        )
