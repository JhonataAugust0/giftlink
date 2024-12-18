
from src.adapters.output.data.orm.entities.orm_entities import UserKeys
from src.domain.ports.key_user_repository import KeyUserRepository
from src.infrastructure.orm.config.db_config import get_async_session
from typing import List, Optional
from sqlalchemy import select, delete, update as update_orm
from src.domain.models.keys import Keys
from sqlalchemy.ext.asyncio import AsyncSession

class KeysRepositoryORM(KeyUserRepository):
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session

    @classmethod
    async def create_instance(cls):
        async with get_async_session() as session:
            return cls(session)

    async def insert_key(self, public_key: str, private_key: str, user_id: int) -> UserKeys:
        new_key = UserKeys(public_key=public_key, private_key=private_key, pessoa_id=user_id)
        self.session.add(new_key)
        await self.session.commit()
        await self.session.refresh(new_key)
        return new_key
        

    async def get_by_key_id(self, key_id: int) -> UserKeys | None:
        query = select(UserKeys).where(UserKeys.id == key_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_key_by_user_id(self, user_id: int) -> UserKeys | None:
        query = select(UserKeys).where(UserKeys.pessoa_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_keys_by_user_id(self, user_id: int) -> list[UserKeys]:
        query = select(UserKeys).where(UserKeys.pessoa_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def delete_key_by_id(self, key_id: int) -> bool:
        query = delete(UserKeys).where(UserKeys.id == key_id)
        result = await self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    async def update_key(self, key_id, public_key, private_key):
        await self.session.execute(
            update_orm(UserKeys)
                .where(UserKeys.id == key_id)
                .values(public_key=public_key, private_key=private_key)
        )
        await self.session.commit()
        return
        

    async def __aenter__(self):
            return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()