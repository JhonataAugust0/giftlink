from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Boolean, Integer, ForeignKey, Text
from ..config.base import Base
from typing import List, Optional

class Grupos(Base):
    """Tabela de grupos."""
    __tablename__ = "grupos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    valor_maximo: Mapped[float] = mapped_column(Float)
    status_sorteio: Mapped[bool] = mapped_column(Boolean, default=False)

    pessoas: Mapped[List["Pessoa"]] = relationship(
        "Pessoa", back_populates="grupo", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Grupo(id={self.id}, nome='{self.nome}', valor_maximo='{self.valor_maximo}', status_sorteio='{self.status_sorteio}')>"


class Pessoa(Base):
    """Tabela de pessoas."""
    __tablename__ = "pessoas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    codigo: Mapped[int] = mapped_column(Integer, unique=True)
    sugestao_presente: Mapped[str] = mapped_column(Text, nullable=True)

    # Relacionamento com Grupo
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.id", ondelete="CASCADE"))
    grupo: Mapped["Grupos"] = relationship("Grupos", back_populates="pessoas")

    def __repr__(self):
        return f"<Pessoa(id={self.id}, nome='{self.nome}', codigo='{self.codigo}', sugestao_presente='{self.sugestao_presente}', grupo_id={self.grupo_id})>"