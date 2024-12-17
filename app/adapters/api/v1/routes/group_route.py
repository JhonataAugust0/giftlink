import http
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from .....domain.use_cases.group_use_case import GroupUseCase
from ..dtos.group_dto import GroupRequestDTO, GroupResponseDTO
from .....adapters.data.orm.repositories.group_repository_orm import GroupRepositoryORM


class groupRouter:
      router = APIRouter()

      async def get_group_repository() -> GroupUseCase:
            repository = await GroupRepositoryORM().create_instance()
            return GroupUseCase(repository)


      @router.post("/groups", response_model=GroupResponseDTO)
      async def create_group(
            params: GroupRequestDTO, use_case: GroupUseCase = Depends(get_group_repository)
            ):
            group = params.to_core()
            created_group = await use_case.create(group.name, group.max_value)
            return GroupResponseDTO.from_core(created_group)
      
      @router.post("/groups/{group_id}/draw", response_model=GroupResponseDTO)
      async def group_draw(
            group_id: int, use_case: GroupUseCase = Depends(get_group_repository)
            ):
            pass
      
      @router.get("/groups", response_model=List[GroupResponseDTO])
      async def get_all_groups(use_case: GroupUseCase = Depends(get_group_repository)):
            groups = await use_case.list_groups()
            return [GroupResponseDTO.from_core(group) for group in groups]
      
      @router.get("/groups/{group_id}", response_model=GroupResponseDTO, responses={
            404: {"description": "Group not found"},
            401: {"description": "Unauthorized"},
      })
      async def show_group(group_id: int, use_case: GroupUseCase = Depends(get_group_repository)):
            group = await use_case.show_group(group_id)
            if group is None:
                  raise HTTPException(status_code=404, detail="Group not found")
            return GroupResponseDTO.from_core(group)

      
      @router.put("/groups/{group_id}", response_model=GroupResponseDTO)
      async def edit_group(
            group_id: int,
            params: GroupRequestDTO, 
            use_case: GroupUseCase = Depends(get_group_repository)
            ):
            group = await use_case.edit_group(group_id, params.name, params.max_value)
            return GroupResponseDTO.from_core(group)

      @router.delete("/groups/{group_id}", responses={
            404: {"description": "Group with id {id} does not exist"},
            401: {"description": "Unauthorized"},
      })
      async def remove_group(group_id: int, use_case: GroupUseCase = Depends(get_group_repository)):
            response = await use_case.remove_group(group_id)
            if response is None:
                  raise HTTPException(status_code=404, detail=f"with group_id {group_id} does not exist")
            return http.HTTPStatus.NO_CONTENT
