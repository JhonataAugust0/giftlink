import pytest
from unittest.mock import AsyncMock
from app.domain.models.group import Group
from app.domain.use_cases.group_use_case import GroupUseCase
from app.domain.ports.group_repository import GroupRepository

@pytest.fixture
def group_repository():
    return AsyncMock(spec=GroupRepository)

@pytest.fixture
def group_use_case(group_repository):
    return GroupUseCase(group_repository)

@pytest.mark.asyncio
async def test_create_group(group_use_case, group_repository):
    group_name = "Test Group"
    max_value = 100.0
    group = Group(name=group_name, max_value=max_value)
    group_repository.create.return_value = group

    result = await group_use_case.create(group_name, max_value)

    assert result == group
    group_repository.create.assert_called_once_with(group)

@pytest.mark.asyncio
async def test_list_groups(group_use_case, group_repository):
    groups = [Group(name="Group 1", max_value=100.0), Group(name="Group 2", max_value=200.0)]
    group_repository.get_all.return_value = groups

    result = await group_use_case.list_groups()

    assert result == groups
    group_repository.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_show_group(group_use_case, group_repository):
    group_id = 1
    group = Group(name="Test Group", max_value=100.0)
    group_repository.get_by_id.return_value = group

    result = await group_use_case.show_group(group_id)

    assert result == group
    group_repository.get_by_id.assert_called_once_with(group_id)

@pytest.mark.asyncio
async def test_remove_group(group_use_case, group_repository):
    group_id = 1

    await group_use_case.remove_group(group_id)

    group_repository.delete.assert_called_once_with(group_id)

@pytest.mark.asyncio
async def test_edit_group(group_use_case, group_repository):
    group_id = 1
    group_name = "Updated Group"
    max_value = 150.0
    group = Group(name="Test Group", max_value=100.0)
    updated_group = Group(name=group_name, max_value=max_value)
    group_repository.get_by_id.return_value = group
    group_repository.update.return_value = updated_group

    result = await group_use_case.edit_group(group_id, group_name, max_value)

    assert result == updated_group
    group_repository.get_by_id.assert_called_once_with(group_id)
    group_repository.update.assert_called_once_with(group)
