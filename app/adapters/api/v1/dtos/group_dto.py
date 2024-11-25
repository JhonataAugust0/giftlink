from pydantic import BaseModel, Field
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
                "valor_maximo": 100.0,
                "status_sorteio": False,
            }
        }

    @classmethod
    def to_core(self) -> Group:
        return Group(
            id              = self.id | None,
            group_name      = self.name,
            max_value       = self.max_value,
            draw_status     = self.draw_status,
        )

    @classmethod
    def from_core(cls, group: Group):
        return cls(
            id              = group.id,
            nome            = group.nome,
            valor_maximo    = group.valor_maximo,
            status_sorteio  = group.status_sorteio,
        )
    

class GroupRequestDTO(BaseModel):
    name:        str    = Field(..., max_length=100, description="Nome do grupo")
    max_value:   float  = Field(..., ge=0, description="Valor máximo do presente")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Amigos da Faculdade",
                "max_value": 70.0,
            }
        }

    def to_core(self) -> Group:
        print(self.name)
        return Group(
            name            = self.name,
            max_value       = self.max_value,
        )

    @classmethod
    def from_core(cls, group: Group):
        return cls(
            id              = group.id,
            nome            = group.name,
            valor_maximo    = group.max_value,
            status_sorteio  = group.draw_status,
        )

    # @staticmethod
    # def to_orm(grupo: Group) -> GrupoORM:
    #     return GrupoORM(
    #         id              = grupo.id,
    #         nome            = grupo.nome,
    #         valor_maximo    = grupo.valor_maximo,
    #         status_sorteio  = grupo.status_sorteio,
    #     )

    # @staticmethod
    # def from_orm(orm_obj: GrupoORM) -> Grupo:
    #     return Group(
    #         id              = orm_obj.id,
    #         group_name      = orm_obj.nome,
    #         max_value       = orm_obj.valor_maximo,
    #         draw_status     = orm_obj.status_sorteio,
    #     )