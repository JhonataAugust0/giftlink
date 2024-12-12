import http
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException

from app.adapters.log.audit_logger import AuditLogger
from .....domain.use_cases.people_use_case import PeopleUseCase
from ..dtos.people_dto import PeopleRequestDTO, PeopleResponseDTO
from .....adapters.data.orm.repositories.people_repository import PeopleRepositoryORM


class peopleRouter:
      router = APIRouter()

      async def get_people_repository() -> PeopleUseCase:
            repository = await PeopleRepositoryORM().create_instance()
            return PeopleUseCase(repository)


      @router.post("/people/add", response_model=PeopleResponseDTO)
      async def add_people(
            params: PeopleRequestDTO, use_case: PeopleUseCase = Depends(get_people_repository)
            ):
            people = params.to_core()
            AuditLogger().log_info(f"{people}", "add_people")
            created_people = await use_case.add_people(people.name, people.group_id, people.sugestao_presente)
            return PeopleResponseDTO.from_core(created_people)
      
      @router.get("/people/show", response_model=PeopleResponseDTO, responses={
            404: {"description": "People not found"},
            401: {"description": "Unauthorized"},
      })
      async def show_people(id: int, use_case: PeopleUseCase = Depends(get_people_repository)):
            people = await use_case.show_people(id)
            if people is None:
                  raise HTTPException(status_code=404, detail="people not found")
            return PeopleResponseDTO.from_core(people)

      
      @router.put("/people/update", response_model=PeopleResponseDTO)
      async def edit_people(
            people_id: int,
            params: PeopleRequestDTO, 
            use_case: PeopleUseCase = Depends(get_people_repository)
            ):
            people_data = params.to_core()
            people = await use_case.edit_people(people_id, people_data.name, people_data.grupo_id, people_data.sugestao_presente)
            return PeopleResponseDTO.from_core(people)

      @router.delete("/people/remove", responses={
            404: {"description": "people with id {id} does not exist"},
            401: {"description": "Unauthorized"},
      })
      async def remove_people(id: int, use_case: PeopleUseCase = Depends(get_people_repository)):
            response = await use_case.remove_people(id)
            if response is None:
                  raise HTTPException(status_code=404, detail=f"with id {id} does not exist")
            return http.HTTPStatus.NO_CONTENT
