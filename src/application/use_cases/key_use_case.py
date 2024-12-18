from typing import List
from src.domain.models.keys import Keys
from src.domain.ports.key_user_repository import KeyUserRepository


class KeyUseCase:
    def __init__(self, repository: KeyUserRepository):
        self.group_repository = repository

    async def create(self, public_key: str, private_key: str, user_id: int) -> Keys:
        new_group = Keys(public_key=public_key, private_key=private_key, user_id=user_id)
        return await self.group_repository.insert_key(new_group)

    async def list_user_keys(self) -> List[Keys]:
        return await self.group_repository.get_keys_by_user_id()

    async def get_key(self, user_id: int) -> Keys:
        return await self.group_repository.get_by_key_id(user_id)

    async def remove_key(self, id: int) -> None:
        return await self.group_repository.delete_key_by_id(id)

    async def edit_key(self, key_id: int, public_key: str, private_key: str) -> Keys:
        key = await self.group_repository.get_by_key_id(key_id)
        key.public_key = public_key
        key.private_key = private_key
        return await self.group_repository.update_key(key)
