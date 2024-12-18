from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, Float, Boolean, Integer, ForeignKey, Text, func
from src.infrastructure.orm.config.base import Base
from typing import List, Optional


class Grupos(Base):
    """Tabela de grupos."""
    __tablename__ = "grupos"

    id:                 Mapped[int] = mapped_column(Integer, primary_key=True)
    nome:               Mapped[str] = mapped_column(String(100))
    valor_maximo:       Mapped[float] = mapped_column(Float)
    status_sorteio:     Mapped[bool] = mapped_column(Boolean, default=False)
    sorteio_id:         Mapped[int] = mapped_column(ForeignKey("sorteios.id", ondelete="CASCADE"), nullable=True)

    pessoas:            Mapped[List["Pessoa"]] = relationship(
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

    id:                 Mapped[int] = mapped_column(Integer, primary_key=True)
    nome:               Mapped[str] = mapped_column(String(100))
    email:              Mapped[str] = mapped_column(String(100))
    senha:              Mapped[str] = mapped_column(String(100))
    salt:               Mapped[str] = mapped_column(String(100))
    codigo:             Mapped[int] = mapped_column(Integer, unique=True)
    sugestao_presente:  Mapped[str] = mapped_column(Text, nullable=True)
    ativa:              Mapped[bool] = mapped_column(Boolean, default=True)
    sorteio_id:         Mapped[int] = mapped_column(ForeignKey("sorteios.id", ondelete="CASCADE"), nullable=True)
    grupo_id:           Mapped[int] = mapped_column(ForeignKey("grupos.id", ondelete="CASCADE"))
    
    grupo:              Mapped["Grupos"] = relationship("Grupos", back_populates="pessoas")
    sorteios_como_participante: Mapped[List["Sorteio"]] = relationship(
        "Sorteio", foreign_keys="[Sorteio.participante_id]", back_populates="participante"
    )
    sorteios_como_sorteado: Mapped[List["Sorteio"]] = relationship(
        "Sorteio", foreign_keys="[Sorteio.sorteado_id]", back_populates="sorteado"
    )
    user_keys: Mapped[List["UserKeys"]] = relationship(
        "UserKeys", back_populates="pessoa", cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"<Pessoa(id={self.id}, nome='{self.nome}', email='{self.email}', senha='{self.senha}', 'salt={self.salt}', codigo='{self.codigo}', sugestao_presente='{self.sugestao_presente}', grupo_id={self.grupo_id}, sorteio_id='{self.sorteio_id}', ativa'{self.ativa}')>"
    
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
    

class UserKeys(Base):
    """Tabela de chaves de usuário."""
    __tablename__ = "user_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    public_key: Mapped[str] = mapped_column(Text, nullable=False)
    private_key: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    pessoa_id: Mapped[int] = mapped_column(ForeignKey("pessoas.id", ondelete="CASCADE"), nullable=False)
    
    pessoa: Mapped["Pessoa"] = relationship("Pessoa", back_populates="user_keys")
    
    def __repr__(self):
        return f"<UserKeys(id={self.id}, public_key='{self.public_key}', private_key='{self.private_key}', created_at='{self.created_at}', pessoa_id={self.pessoa_id})>"