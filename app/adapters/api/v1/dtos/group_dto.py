from typing import List
from pydantic import BaseModel, Field

from app.adapters.api.v1.dtos.people_dto import PeopleResponseDTO
from app.domain.models.people import People

from ....data.orm.entities.group_orm_model import Grupos
from .....domain.models.group import Group

class GroupResponseDTO(BaseModel):
    id:             int
    nome:           str
    valor_maximo:   float
    status_sorteio: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nome": "Amigos da Faculdade",
                "valor_maximo": 25.0,
                "status_sorteio": False,
            }
        }

    @staticmethod
    def from_core(group: Grupos):
        return GroupResponseDTO(
            id=group.id,
            nome=group.nome,
            valor_maximo=group.valor_maximo,
            status_sorteio=group.status_sorteio,
        )


class GroupRequestDTO(BaseModel):
    name: str = Field(..., max_length=100, description="Nome do grupo")
    max_value: float = Field(..., ge=0, description="Valor máximo do presente")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Amigos da Faculdade",
                "max_value": 25.0,
            }
        }

    def to_core(self) -> Group:
        return Group(
            name=self.name,
            max_value=self.max_value,
        )
