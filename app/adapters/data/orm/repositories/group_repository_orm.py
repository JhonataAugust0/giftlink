from typing import List, Optional
from sqlalchemy import select, delete, update as update_orm
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.log.audit_logger import AuditLogger

from .....domain.models.group import Group
from .....domain.ports.group_repository import GroupRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import NoResultFound
from ..config.db_config import get_async_session
from ..entities.group_orm_model import Grupos, Pessoa


class GroupRepositoryORM(GroupRepository):
    audit_logger = AuditLogger()
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session

    @classmethod
    async def create_instance(cls):
        session = await get_async_session().__anext__()
        return cls(session)
    
    async def make_select(self, id: int) -> Grupos:
        """
        Método genérico para realizar um SELECT por ID.
        """
        query = select(Grupos).where(Grupos.id == id)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()
        if not instance:
            return NoResultFound(f"{Grupos.__name__} with id {id} does not exist.")
        return instance

    async def create(self, group: Group) -> Grupos:
        try:
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
        
        except Exception as error:
            self.audit_logger.log_error("Erro ao criar grupo no banco de dados", "create", str(error), params={'group': group})
            await self.session.rollback()
            raise

    async def get_all(self) -> List[Grupos]:
        query = select(Grupos)
        result = await self.session.execute(query)
        group_and_people = result.scalars().all()
        return group_and_people

    async def get_by_id(self, group_id: int) -> Grupos:
        try:
            query = select(Grupos, Pessoa).where(Grupos.id == group_id).join(Pessoa, Pessoa.grupo_id == group_id)
            result = await self.session.execute(query)
            group_and_people = result.all()
            return group_and_people
        except SQLAlchemyError as error:
            self.audit_logger.log_error(f"Erro ao resgatar grupo de id {group_id} no banco de dados", "create", str(error), params={'group_id': group_id})
            raise

    async def update(self, group: Group) -> Grupos:
        group = await self.make_select(group.id)

        await self.session.execute(
        update_orm(Grupos)
        .where(Grupos.id == group.id)
        .values(
            nome=group.name,
            valor_maximo=group.max_value,
        )
    )
        await self.session.commit()
        updated_group = await self.session.get(Grupos, group.id)
        return updated_group

    async def delete(self, group_id: int) -> None:
        try:
            instance = await self.make_select(group_id)
            query = delete(Grupos).where(Grupos.id == group_id)
            await self.session.execute(query)
            await self.session.commit()
            return instance     
        except SQLAlchemyError as error:
            await self.session.rollback()
            return instance
            

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

