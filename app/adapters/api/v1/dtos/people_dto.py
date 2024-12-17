from pydantic import BaseModel, Field

from ....data.orm.entities.orm_entities import Pessoa
from .....domain.models.people import People

class PeopleResponseDTO(BaseModel):
    id:                 int 
    name:               str
    codigo:             int 
    group_id:           int 
    sugestao_presente:  str 

    class Config:
        json_schema_extra = {
            "example": {
                "id": 12,
                "name": "Leo",
                "codigo": 1598,
                "group_id": 29,
                "sugestao_presente": "Um livro"
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
        )


class PeopleRequestDTO(BaseModel):
    group_id:           int = Field(..., ge=0, description="Id do grupo")
    name:               str = Field(..., max_length=100, description="name da pessoa")
    sugestao_presente:   str = Field(..., max_length=100, description="Sugestão de presente")

    class Config:
        json_schema_extra = {
            "example": {
                "group_id": 13,
                "name": "Leo",
                "sugestao_presente": "Um livro"
            }
        }

    def to_core(self) -> People:
        return People(
            name=self.name,
            group_id=self.group_id,
            sugestao_presente=self.sugestao_presente,
        )
