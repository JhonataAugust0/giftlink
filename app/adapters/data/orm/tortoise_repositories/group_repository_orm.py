from types import coroutine
from .....domain.models.group import Group
from .....domain.ports.group_repository import GroupRepository
from ..config.db_config import init_db
from ..entities.tortoise_models import Grupo, Pessoa


class GrupoRepositoryORM(GroupRepository):
    
    @classmethod
    async def create_instance(cls):
        await init_db()
        return cls()

    async def create(self, group: Group) -> Grupo:
        group = await Grupo.create(nome=group.name, valor_maximo=group.max_value, status_sorteio=group.draw_status)
        return group

    async def get_all(self):
        # await self.ensure_db_initialized()
        return await Grupo.all()

    async def get_by_id(self, group_id: int) -> Grupo:
        return await Grupo.get(id=group_id)

    async def update(self, group: Grupo) -> Grupo:
        await group.save()
        return group

    async def delete(self, group_id: int):
        await Grupo.filter(id=group_id).delete()

# class PessoaRepository:
#     """Repositório para manipular pessoas."""
#     async def criar_pessoa(self, nome: str, codigo: str, group_id: int, sugestao_presente: str = None) -> Pessoa:
#         pessoa = await Pessoa.create(
#             nome=nome,
#             codigo=codigo,
#             group_id=group_id,
#             sugestao_presente=sugestao_presente,
#         )
#         return pessoa

#     async def obter_pessoa_por_codigo(self, codigo: str) -> Pessoa:
#         return await Pessoa.get_or_none(codigo=codigo)

#     async def listar_pessoas(self):
#         return await Pessoa.all()