from random import randint
from typing import List, Optional
from sqlalchemy import func, select, delete, update as update_orm
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.log.audit_logger import AuditLogger
from app.domain.models.people import People

from .....domain.ports.people_repository import PeopleRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import NoResultFound
from ..config.db_config import get_async_session
from ..entities.group_orm_model import Grupos, Pessoa


class PeopleRepositoryORM(PeopleRepository):
    audit_logger = AuditLogger()
    
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session

    @classmethod
    async def create_instance(cls):
        async with get_async_session() as session:
            return cls(session)
            
    async def make_select(self, id: int) -> Pessoa:
        """
        Método genérico para realizar um SELECT por ID.
        """
        query = select(Pessoa).where(Pessoa.id == id)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()
        if not instance:
            return NoResultFound(f"{Pessoa.__name__} with id {id} does not exist.")
        return instance

    async def add_people_in_group(self, people: People, group_id: int) -> Pessoa:
        try:
            group = await self.session.get(Grupos, group_id)
            if not group:
                raise ValueError(f"Grupo com ID {group_id} não encontrado.")
            people.group_id = group_id

            people_orm = Pessoa(
                nome=people.name,
                sugestao_presente=people.sugestao_presente,
                grupo_id=people.group_id,
                codigo=randint(1000, 9999)
            )
            
            self.session.add(people_orm)
            await self.session.commit()
            await self.session.refresh(people_orm)
            
            self.audit_logger.log_info(
                "Pessoa adicionada com sucesso ao grupo.",
                "add_people_in_group",
                params={'people': people, 'group_id': group_id, "people_orm": people_orm}
            )
            
            return people_orm
        except Exception as error:
          self.audit_logger.log_error(
              "Erro ao adicionar pessoa ao grupo no banco de dados.",
              "add_people_in_group",
              str(error),
              params={'people': people, 'group_id': group_id}
          )
          await self.session.rollback()
          raise

    async def get_all_people_in_group(self, people_id: int) -> List[Pessoa]:
        query = select(Pessoa).where(Pessoa.people_id == people_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_people_by_id(self, people_id: int) -> Pessoa:
        try:
            return await self.make_select(people_id)
        except SQLAlchemyError as error:
            self.audit_logger.log_error(f"Erro ao resgatar pessoa de id {people_id} no banco de dados", "create", str(error), params={'people_id': people_id})
            raise

    async def update_people(self, people: People) -> Pessoa:
        people_instance = await self.make_select(people.id)
        await self.session.execute(
        update_orm(Pessoa)
            .where(Pessoa.id == people_instance.id)
            .values(
                nome=people.name,
                grupo_id=people.group_id,
                sugestao_presente=people.sugestao_presente,
            ))

        await self.session.commit()
        updated_group = await self.make_select(people_instance.id)
        return updated_group

    async def remove_people_from_group(self, people_id: int) -> None:
        try:
            instance = await self.make_select(people_id)
            query = delete(Pessoa).where(Pessoa.id == people_id)
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

