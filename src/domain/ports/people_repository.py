from abc import ABC, abstractmethod
from typing import List
from src.domain.models.people import People


class PeopleRepository(ABC):
    """Classe abstrata que define as operações do repositório."""

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
    async def get_people_by_id(self, people_id: int) -> People:
        pass

    @abstractmethod
    async def get_people_by_email(self, email: str) -> People:
        pass
    
    @abstractmethod
    async def remove_people_from_group(self, people_id: int) -> None:
        pass

    @abstractmethod
    async def update_people(self, people: People) -> People:
        pass