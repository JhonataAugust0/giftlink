from typing import List
from pydantic import BaseModel, Field

from src.adapters.output.data.orm.entities.orm_entities import Grupos
from src.domain.models.group import Group

class GroupResponseDTO(BaseModel):
    id:             int
    nome:           str
    valor_maximo:   float
    status_sorteio: bool
    sorteio_id:     int | None

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
            sorteio_id=group.sorteio_id
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

class GroupResponseDrawDTO(BaseModel):
    
    class DrawResultDTO(BaseModel):
        participante: str
        sorteado_para: str

    nome: str
    valor_maximo: float
    status_sorteio: bool
    status: str
    mensagem: str
    resultados: List[DrawResultDTO]

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Amigos do Trabalho",
                "valor_maximo": 50.0,
                "status_sorteio": True,
                "status": "success",
                "mensagem": "Sorteio realizado com sucesso.",
                "resultados": [
                    {"participante": "João", "sorteado_para": "Maria"},
                    {"participante": "Maria", "sorteado_para": "Carlos"},
                    {"participante": "Carlos", "sorteado_para": "Ana"},
                    {"participante": "Ana", "sorteado_para": "João"}
                ]
            }
        }
    
    @staticmethod
    def from_core(group, resultados):
        """Método para criar o DTO a partir do modelo do banco de dados (core) e resultados."""
        return GroupResponseDrawDTO(
            id=group.id,
            nome=group.nome,
            valor_maximo=group.valor_maximo,
            status_sorteio=group.status_sorteio,
            status="success",
            mensagem="Sorteio realizado com sucesso.",
            resultados=[{"participante": r['participante'], "sorteado_para": r['sorteado_para']} for r in resultados]
        )