from abc import ABC, abstractmethod
from typing import List
from ..models.group import Group


class GroupRepository(ABC):
    @abstractmethod
    async def make_select(self, id: int) -> Group:
        pass

    @abstractmethod
    async def create(self, group: Group) -> Group:
        pass

    @abstractmethod
    async def get_all(self) -> List[Group]:
        pass

    @abstractmethod
    async def get_by_id(self, group_id: int) -> Group:
        pass

    @abstractmethod
    async def delete(self, group_id: int) -> None:
        pass

    @abstractmethod
    async def update(self, group: Group) -> Group:
        pass
