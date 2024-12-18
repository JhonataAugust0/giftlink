import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from unittest.mock import AsyncMock, MagicMock

from app.adapters.output.data.orm.repositories.group_repository_orm import GroupRepositoryORM
from app.domain.models.group import Group
from adapters.output.data.orm.entities.orm_entities import Grupos

@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def repository(mock_session):
    return GroupRepositoryORM(session=mock_session)

@pytest.mark.asyncio
async def test_create_group_success(repository, mock_session):
    group = Group(id=1, name="Test Group", max_value=100, draw_status=True)
    group_orm = Grupos(id=1, nome="Test Group", valor_maximo=100, status_sorteio=True)
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    result = await repository.create(group)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert result.nome == group_orm.nome
    assert result.valor_maximo == group_orm.valor_maximo
    assert result.status_sorteio == group_orm.status_sorteio

@pytest.mark.asyncio
async def test_create_group_failure(repository, mock_session):
    group = Group(id=1, name="Test Group", max_value=100, draw_status=True)
    mock_session.commit.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        await repository.create(group)

    mock_session.rollback.assert_called_once()

# @pytest.mark.asyncio
# async def test_get_all_groups(repository, mock_session):
#     # Criação dos dados simulados
#     groups = [
#         Grupos(id=1, nome="Group 1", valor_maximo=100, status_sorteio=True),
#         Grupos(id=2, nome="Group 2", valor_maximo=200, status_sorteio=False)
#     ]
    
#     # Configurando o comportamento do mock (execute -> scalars -> all)
#     mock_scalars = AsyncMock()
#     mock_scalars.all.return_value = groups

#     mock_result = AsyncMock()
#     mock_result.scalars.return_value = mock_scalars  # scalars() retorna um AsyncMock
    
#     mock_session.execute.return_value = mock_result  # execute() retorna um AsyncMock

#     # Chamada do método que está sendo testado
#     result = await repository.get_all()

#     # Verificações
#     mock_session.execute.assert_called_once_with(select(Grupos))  # Verifica a query executada
#     assert result == groups  # Verifica o retorno esperadodo

@pytest.mark.asyncio
async def test_get_group_by_id_success(repository, mock_session):
    group_id = 1
    group = Grupos(id=group_id, nome="Test Group", valor_maximo=100, status_sorteio=True)
    repository.make_select = AsyncMock(return_value=group)

    result = await repository.get_by_id(group_id)

    repository.make_select.assert_called_once_with(group_id)
    assert result == group

@pytest.mark.asyncio
async def test_get_group_by_id_failure(repository, mock_session):
    group_id = 1
    repository.make_select = AsyncMock(side_effect=SQLAlchemyError("Database error"))

    with pytest.raises(SQLAlchemyError, match="Database error"):
        await repository.get_by_id(group_id)

# @pytest.mark.asyncio
# async def test_make_select_success(repository, mock_session):
#     group_id = 1
#     group = Grupos(id=group_id, nome="Test Group", valor_maximo=100, status_sorteio=True)
#     mock_session.execute.return_value.scalar_one_or_none.return_value = group

#     result = await repository.make_select(group_id)

#     query = select(Grupos).where(Grupos.id == group_id)
#     mock_session.execute.assert_called_once_with(query)
#     assert result == group

# @pytest.mark.asyncio
# async def test_make_select_no_result(repository, mock_session):
#     group_id = 1
#     mock_session.execute.return_value.scalar_one_or_none.return_value = None

#     with pytest.raises(NoResultFound):
#         await repository.make_select(group_id)