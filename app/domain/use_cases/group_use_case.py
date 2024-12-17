from typing import List
from ..models.group import Group
from ..ports.group_repository import GroupRepository


class GroupUseCase:
    def __init__(self, repository: GroupRepository):
        self.group_repository = repository

    async def create(self, group_name: str, max_value: float) -> Group:
        new_group = Group(name=group_name, max_value=max_value)
        return await self.group_repository.create_group(new_group)

    async def list_groups(self) -> List[Group]:
        return await self.group_repository.get_all_groups()

    async def show_group(self, group_id: int) -> Group:
        return await self.group_repository.get_group_by_id(group_id)

    async def remove_group(self, group_id: int) -> None:
        return await self.group_repository.delete_group(group_id)

    async def edit_group(self, group_id: int, group_name: str, max_value: float) -> Group:
        group = await self.group_repository.get_group_by_id(group_id)
        group.name = group_name
        group.max_value = max_value
        return await self.group_repository.update_group(group)
