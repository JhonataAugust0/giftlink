from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from src.adapters.input.api.v1.dtos.auth_dto import LoginRequestDTO
from src.application.services.password_service import PasswordService
from src.application.services.auth_service import JWTService
from src.application.use_cases.people_use_case import PeopleUseCase
from src.adapters.output.data.orm.repositories.people_repository_orm import PeopleRepositoryORM

class authRoutes:
    router = APIRouter()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
    
    async def get_people_repository() -> PeopleUseCase:
            repository = await PeopleRepositoryORM().create_instance()
            return PeopleUseCase(repository)
    
    def get_current_user(public_key, token: Annotated[str, Depends(oauth2_scheme)], jwt_service: JWTService = Depends(JWTService)):
        try:
            payload = jwt_service.validate_token(token, public_key)
            print(payload)
            user_email = payload.get('sub')
            
            if user_email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            return user_email
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    @router.post("/protected-route")
    async def protected_route(public_key: str, current_user: Annotated[str, Depends(get_current_user)]):
        return {
            "message": "Rota protegida acessada com sucesso",
            "user": current_user
        }

    @router.post("/token")
    async def login(
        params: OAuth2PasswordRequestForm = Depends(), 
        use_case: PeopleUseCase = Depends(get_people_repository), 
        jwt_service: JWTService = Depends(JWTService),
        password_service: PasswordService = Depends(PasswordService) 
    ):  
        user = await use_case.show_people_by_email(params.username)
        if not user or not password_service.verify_password(user.senha, params.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"}
            )
        keys = await jwt_service.get_or_create_keys(user.id)
        access_token = jwt_service.create_access_token(
            data={"sub": user.email}, 
            private_key=keys[0],
            expires_delta=timedelta(minutes=120)
        )
        
        return {
            "access_token": access_token, 
            "token_type": "bearer"
        }