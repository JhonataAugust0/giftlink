from abc import ABC, abstractmethod
from typing import List
from src.domain.models.group import Group


class GroupRepository(ABC):
    @abstractmethod
    async def make_select(self, id: int) -> Group:
        pass

    @abstractmethod
    async def create_group(self, group: Group) -> Group:
        pass

    @abstractmethod
    async def get_all_groups(self) -> List[Group]:
        pass

    @abstractmethod
    async def get_group_by_id(self, group_id: int) -> Group:
        pass

    @abstractmethod
    async def delete_group(self, group_id: int) -> None:
        pass

    @abstractmethod
    async def update_group(self, group: Group) -> Group:
        pass
