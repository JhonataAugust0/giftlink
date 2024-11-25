from typing import Dict, List
from fastapi import APIRouter, Depends
from .....domain.use_cases.group_use_case import GroupUseCase
from ..dtos.group_dto import GroupRequestDTO, GroupResponseDTO
from .....adapters.data.orm.tortoise_repositories.group_repository_orm import GrupoRepositoryORM


class groupRouter:
      router = APIRouter()

      async def get_group_repository() -> GroupUseCase:
            repository = await GrupoRepositoryORM().create_instance()
            return GroupUseCase(repository)


      @router.post("/group/create", response_model=GroupResponseDTO)
      async def create_group(
            params: GroupRequestDTO, use_case: GroupUseCase = Depends(get_group_repository)
            ):
            group = params.to_core()
            created_group = await use_case.create(group.name, group.max_value)
            return GroupResponseDTO.from_core(created_group)
      
      @router.get("/groups/list", response_model=List[GroupResponseDTO])
      async def get_all_groups(use_case: GroupUseCase = Depends(get_group_repository)):
            groups = await use_case.list_groups()
            return [GroupResponseDTO.from_core(group) for group in groups]
      
      # @router.get("/group/show", response_model=GroupResponseDTO)
      # async def show_group(
      #       id: int, 
      #       use_case: GroupUseCase = Depends()
      #       ) -> Dict[str, str]:
      #       group = await use_case.show_group(id)
      #       return {"id": group.id, "nome": group.name, "valor_maximo": group.max_value, "status_sorteio": group.draw_status}

      # @router.patch("/group/edit", response_model=GroupResponseDTO)
      # async def edit_group(
      #       group_id: int,
      #       params: GroupRequestDTO, 
      #       use_case: GroupUseCase = Depends()
      #       ) -> Dict[str, str]:
      #       group = await use_case.edit_group(group_id, params.name, params.max_value)
      #       return {"id": group.id, "nome": group.name, "valor_maximo": group.max_value}

      # @router.delete("/group/remove")
      # async def remove_group(id: int, use_case: GroupUseCase = Depends()) -> Dict[str,str]:
      #       # use_case.remove_group(id)
      #       pass