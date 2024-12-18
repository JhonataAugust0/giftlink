from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Boolean, Integer, ForeignKey, Text
from app.infrastructure.orm.config.base import Base
from typing import List, Optional


class Grupos(Base):
    """Tabela de grupos."""
    __tablename__ = "grupos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    valor_maximo: Mapped[float] = mapped_column(Float)
    status_sorteio: Mapped[bool] = mapped_column(Boolean, default=False)
    sorteio_id: Mapped[int] = mapped_column(ForeignKey("sorteios.id", ondelete="CASCADE"), nullable=True)

    pessoas: Mapped[List["Pessoa"]] = relationship(
        "Pessoa", back_populates="grupo", cascade="all, delete-orphan"
    )
    
    sorteios: Mapped[List["Sorteio"]] = relationship(
        "Sorteio",
        back_populates="grupo",
        cascade="all, delete-orphan",
        primaryjoin="Grupos.id == Sorteio.grupo_id"
    )

    def __repr__(self):
        return f"<Grupo(id={self.id}, nome='{self.nome}', valor_maximo='{self.valor_maximo}', status_sorteio='{self.status_sorteio}', sorteio_id='{self.sorteio_id}')>"

class Pessoa(Base):
    """Tabela de pessoas."""
    __tablename__ = "pessoas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    codigo: Mapped[int] = mapped_column(Integer, unique=True)
    sugestao_presente: Mapped[str] = mapped_column(Text, nullable=True)
    sorteio_id: Mapped[int] = mapped_column(ForeignKey("sorteios.id", ondelete="CASCADE"), nullable=True)

    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.id", ondelete="CASCADE"))
    grupo: Mapped["Grupos"] = relationship("Grupos", back_populates="pessoas")

    sorteios_como_participante: Mapped[List["Sorteio"]] = relationship(
        "Sorteio", foreign_keys="[Sorteio.participante_id]", back_populates="participante"
    )
    sorteios_como_sorteado: Mapped[List["Sorteio"]] = relationship(
        "Sorteio", foreign_keys="[Sorteio.sorteado_id]", back_populates="sorteado"
    )

    def __repr__(self):
        return f"<Pessoa(id={self.id}, nome='{self.nome}', codigo='{self.codigo}', sugestao_presente='{self.sugestao_presente}', grupo_id={self.grupo_id}, sorteio_id='{self.sorteio_id}')>"
    
class Sorteio(Base):
    """Tabela de sorteios."""
    __tablename__ = "sorteios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.id", ondelete="CASCADE"))
    grupo: Mapped["Grupos"] = relationship(
        "Grupos",
        back_populates="sorteios",
        foreign_keys=[grupo_id],
        primaryjoin="Sorteio.grupo_id == Grupos.id"
    )

    participante_id: Mapped[int] = mapped_column(ForeignKey("pessoas.id", ondelete="CASCADE"))
    participante: Mapped["Pessoa"] = relationship(
        "Pessoa", foreign_keys=[participante_id], back_populates="sorteios_como_participante"
    )

    sorteado_id: Mapped[int] = mapped_column(ForeignKey("pessoas.id", ondelete="CASCADE"))
    sorteado: Mapped["Pessoa"] = relationship(
        "Pessoa",
        foreign_keys=[sorteado_id],
        back_populates="sorteios_como_sorteado",
        primaryjoin="Sorteio.sorteado_id == Pessoa.id"  # Relacionamento com Pessoa
    )

    def __repr__(self):
        return f"<Sorteio(id={self.id}, grupo_id={self.grupo_id}, participante_id={self.participante_id}, sorteado_id={self.sorteado_id}')>"