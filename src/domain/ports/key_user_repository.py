from abc import ABC, abstractmethod
from src.domain.models.keys import Keys


class KeyUserRepository(ABC):
    @abstractmethod
    async def insert_key(self, public_key: str, private_key: str, user_id: int) -> Keys:
        pass

    @abstractmethod
    async def get_by_key_id(self, key_id: int) -> Keys | None:
        pass

    @abstractmethod
    async def get_key_by_user_id(self, user_id: int) -> Keys | None:
        pass

    @abstractmethod
    async def get_keys_by_user_id(self, user_id: int) -> list[Keys]:
        pass
   
    @abstractmethod
    async def delete_key_by_id(self, key_id: int) -> None:
        pass

    @abstractmethod
    async def update_key(self, key_id: int, public_key: str, private_key: str) -> Keys:
        pass