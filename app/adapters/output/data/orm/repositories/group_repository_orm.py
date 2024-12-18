from typing import List, Optional
from sqlalchemy import select, delete, update as update_orm
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.log.audit_logger import AuditLogger

from app.domain.models.group import Group
from app.domain.ports.group_repository import GroupRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import NoResultFound
from app.infrastructure.orm.config.db_config import get_async_session
from app.adapters.output.data.orm.entities.orm_entities import Grupos, Pessoa


class GroupRepositoryORM(GroupRepository):
    audit_logger = AuditLogger()
    
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session

    @classmethod
    async def create_instance(cls):
        async with get_async_session() as session:
            return cls(session)
    
    async def make_select(self, id: int) -> Grupos:
        """Realiza um SELECT por ID."""
        query = select(Grupos).where(Grupos.id == id)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()
        if not instance:
            raise ValueError(f"Group with id {id} does not exist.")
        return instance
    

    async def create_group(self, group: Group) -> Grupos:
        group_orm = Grupos(
            nome=group.name, 
            valor_maximo=group.max_value, 
            status_sorteio=group.draw_status
        )
        self.session.add(group_orm)
        await self.session.commit()
        await self.session.refresh(group_orm)
        self.audit_logger.log_info("Grupo criado com sucesso", "create", params={'group': group})
        return group_orm

    async def get_all_groups(self) -> List[Grupos]:
        query = select(Grupos)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_group_by_id(self, group_id: int) -> Grupos:
        return await self.make_select(group_id)


    async def update_group(self, group: Group) -> Grupos:
        group = await self.make_select(group.id)
        if not group:
            return ValueError(f"Grupo com ID {group.id} não encontrado.")
        
        await self.session.execute(
            update_orm(Grupos)
                .where(Grupos.id == group.id)
                .values(nome=group.name, valor_maximo=group.max_value)
        )
        await self.session.commit()
        updated_group = await self.make_select(group.id)
        return updated_group

    async def delete_group(self, group_id: int) -> None:
        group = await self.make_select(group_id)
        if not group:
            return ValueError(f"Grupo com ID {group.id} não encontrado.")
        
        await self.session.execute(delete(Grupos).where(Grupos.id == group_id))
        await self.session.commit()
        return group
            

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

