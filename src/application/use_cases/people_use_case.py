from typing import List
from src.adapters.output.data.orm.entities.orm_entities import Pessoa
from src.domain.models.people import People
from src.domain.ports.people_repository import PeopleRepository


class PeopleUseCase:
    def __init__(self, repository: PeopleRepository):
        self.people_repository = repository

    async def add_people(self, name: str, group_id: int, gift_suggestion: str, email: str, password: str) -> People:
        new_people = People(name=name, group_id=group_id, gift_suggestion=gift_suggestion, email=email, hashed_password=password)
        return await self.people_repository.add_people_in_group(new_people, group_id)

    async def list_people(self) -> List[People]:
        return await self.people_repository.get_all_people_in_group()

    async def show_people(self, people_id: int) -> People:
        return await self.people_repository.get_people_by_id(people_id)

    async def show_people_by_email(self, email: str) -> Pessoa:
        return await self.people_repository.get_people_by_email(email)
    
    async def remove_people(self, people_id: int) -> None:
        return await self.people_repository.remove_people_from_group(people_id)

    async def edit_people(self, people_id: int, people_name: str, group_id: float, sugestao_presente: str) -> People:
        people = await self.people_repository.get_people_by_id(people_id)
        people.name = people_name
        people.group_id = group_id
        people.sugestao_presente = sugestao_presente
        return await self.people_repository.update_people(people)
