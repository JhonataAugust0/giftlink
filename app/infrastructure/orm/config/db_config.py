from contextlib import asynccontextmanager
import os 
from dotenv import load_dotenv

from app.adapters.output.log.audit_logger import AuditLogger
from app.infrastructure.envs.config import Settings
from .base import Base
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
  AsyncSession, 
  async_sessionmaker, 
  create_async_engine
)


audit_logger = AuditLogger()
envs = Settings()

engine = create_async_engine(
    envs.POSTGRES_URL, 
    echo=True,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20
)

# Session factory
async_session = async_sessionmaker(
    engine, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession
)

@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception as error:
            await session.rollback()
            audit_logger.log_error("Erro ao realizar operação no banco de dados", "get_async_session", str(error))
            raise
        finally:
            await session.close()


async def create_database():
    """Criar todas as tabelas definidas nos modelos"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
