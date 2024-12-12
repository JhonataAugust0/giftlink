from abc import ABC, abstractmethod
from typing import List
from ..models.people import People


class PeopleRepository(ABC):
    @abstractmethod
    async def make_select(self, id: int) -> People:
        pass

    @abstractmethod
    async def add_people_in_group(self, people: People, group_id: int) -> People:
        pass

    @abstractmethod
    async def get_all_people_in_group(self, group_id: int) -> List[People]:
        pass

    @abstractmethod
    async def get_people_by_id(self, group_id: int) -> People:
        pass

    @abstractmethod
    async def remove_people_from_group(self, people_id) -> None:
        pass
    
    @abstractmethod
    async def update_people(self, group: People) -> People:
        pass
