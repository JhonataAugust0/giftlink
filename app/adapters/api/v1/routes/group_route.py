import http
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from .....domain.use_cases.group_use_case import GroupUseCase
from ..dtos.group_dto import GroupRequestDTO, GroupResponseDTO, GroupWithParticipantsResponseDTO
from .....adapters.data.orm.repositories.group_repository_orm import GroupRepositoryORM


class groupRouter:
      router = APIRouter()

      async def get_group_repository() -> GroupUseCase:
            repository = await GroupRepositoryORM().create_instance()
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
            print(groups)
            return [GroupResponseDTO.from_core(group) for group in groups]
      
      @router.get("/group/show", response_model=GroupWithParticipantsResponseDTO, responses={
            404: {"description": "Group not found"},
            401: {"description": "Unauthorized"},
      })
      async def show_group(id: int, use_case: GroupUseCase = Depends(get_group_repository)):
            group = await use_case.show_group(id)
            if group is None:
                  raise HTTPException(status_code=404, detail="Group not found")
            return GroupWithParticipantsResponseDTO.from_core(group)

      
      @router.put("/group/update", response_model=GroupResponseDTO)
      async def edit_group(
            group_id: int,
            params: GroupRequestDTO, 
            use_case: GroupUseCase = Depends(get_group_repository)
            ):
            group = await use_case.edit_group(group_id, params.name, params.max_value)
            return GroupResponseDTO.from_core(group)

      @router.delete("/group/remove", responses={
            404: {"description": "Group with id {id} does not exist"},
            401: {"description": "Unauthorized"},
      })
      async def remove_group(id: int, use_case: GroupUseCase = Depends(get_group_repository)):
            response = await use_case.remove_group(id)
            if response is None:
                  raise HTTPException(status_code=404, detail=f"with id {id} does not exist")
            return http.HTTPStatus.NO_CONTENT
