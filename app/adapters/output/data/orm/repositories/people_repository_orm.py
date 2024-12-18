from random import randint
from typing import List, Optional
from sqlalchemy import func, select, delete, update as update_orm
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.log.audit_logger import AuditLogger
from app.domain.models.people import People

from app.domain.ports.people_repository import PeopleRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import NoResultFound
from app.infrastructure.orm.config.db_config import get_async_session
from app.adapters.output.data.orm.entities.orm_entities import Grupos, Pessoa


class PeopleRepositoryORM(PeopleRepository):
    audit_logger = AuditLogger()
    
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session

    @classmethod
    async def create_instance(cls):
        async with get_async_session() as session:
            return cls(session)

    
    async def make_select(self, id: int) -> Pessoa:
        """Realiza um SELECT por ID."""
        result = await self.session.execute(select(Pessoa).where(Pessoa.id == id))
        pessoa = result.scalar_one_or_none()
        if not pessoa:
            raise NoResultFound(f"Pessoa com id {id} não encontrada.")
        return pessoa
        

    async def add_people_in_group(self, people: People, group_id: int) -> Pessoa:
        """
        Adiciona uma pessoa ao grupo.
        """    
        people_orm = Pessoa(
            nome=people.name,
            sugestao_presente=people.sugestao_presente,
            grupo_id=group_id,
            codigo=randint(1000, 9999)
        )
        
        self.session.add(people_orm)
        await self.session.commit()
        await self.session.refresh(people_orm)
        
        self.audit_logger.log_info(
            "Pessoa adicionada com sucesso ao grupo.",
            "add_people_in_group",
            params={"people": people, "group_id": group_id, "people_orm": people_orm}
        )
        
        return people_orm
    
    
    async def get_all_people_in_group(self, group_id: int) -> List[Pessoa]:
        """Retorna todas as pessoas de um grupo específico."""
        result = await self.session.execute(select(Pessoa).where(Pessoa.grupo_id == group_id))
        return result.scalars().all()

    
    async def get_people_by_id(self, people_id: int) -> Pessoa:
        """Busca uma pessoa pelo ID."""
        return await self.make_select(people_id)


    async def update_people(self, people: People) -> Pessoa:
        instance = await self.make_select(people.id)
        if not instance:
            return ValueError(f"Pessoa com ID {instance} não encontrado.")
        
        query = (
            update_orm(Pessoa)
            .where(Pessoa.id == people.id)
            .values(
                nome=people.name,
                grupo_id=people.group_id,
                sugestao_presente=people.sugestao_presente,
            )
        )
        await self.session.execute(query)
        await self.session.commit()
        return await self.make_select(people.id)
            

    async def remove_people_from_group(self, people_id: int) -> None:
        """Remove uma pessoa de um grupo específico."""
        instance = await self.make_select(people_id)
        if not instance:
            return ValueError(f"Pessoa com ID {instance} não encontrado.")
        
        await self.session.execute(delete(Pessoa).where(Pessoa.id == people_id))
        await self.session.commit()

        self.audit_logger.log_info(
            f"Pessoa com ID {people_id} removida com sucesso.",
            "remove_people_from_group",
            params={"people_id": people_id},
        )
        return instance

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

