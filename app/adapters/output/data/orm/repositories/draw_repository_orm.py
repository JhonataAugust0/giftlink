from typing import Optional

from sqlalchemy import select
from app.domain.ports.draw_repository import DrawRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.output.log.audit_logger import AuditLogger
from app.infrastructure.orm.config.db_config import get_async_session
from app.adapters.output.data.orm.entities.orm_entities import Sorteio

class DrawRepositoryORM(DrawRepository):
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session

    @classmethod
    async def create_instance(cls):
        async with get_async_session() as session:
            return cls(session)

    async def create_draw(self, group_id: int, results: dict) -> Sorteio:
        try:
            draw = Sorteio(
              group_id=group_id,
              results=results
            )
            self.session.add(draw)
            await self.session.commit()
            await self.session.refresh(draw)
            return draw
        except Exception as error:
            await self.session.rollback()
            raise

    async def get_draw_by_group(self, group_id: int) -> Sorteio:
        query = select(Sorteio).where(Sorteio.grupo_id == group_id)
        result = await self.session.execute(query)
        draw = result.scalar_one_or_none()
        if not draw:
            raise ValueError(f"No draw found for group {group_id}.")
        return draw

    async def delete_draw(self, draw_id: int) -> None:
        draw = await self.session.get(Sorteio, draw_id)
        if not draw:
            raise ValueError(f"Draw with id {draw_id} does not exist.")
        await self.session.delete(draw)
        await self.session.commit()
        return draw
