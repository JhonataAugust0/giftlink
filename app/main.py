import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Log tool
from app.adapters.log.audit_logger import AuditLogger

# SQLAlchemy imports
from app.adapters.data.orm.config.db_config import engine

# routes
from app.adapters.api.v1.routes.group_route import groupRouter
from app.adapters.api.v1.routes.people_route import peopleRouter

# config imports database
from app.adapters.data.orm.config.base import Base
from app.adapters.data.orm.config.db_config import POSTGRES_URL


load_dotenv()
audit_logger = AuditLogger()


# app lifecycle 
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        audit_logger.log_info("Iniciando conexão com o banco de dados...", "lifespan")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            audit_logger.log_info("Tabelas criadas com sucesso!", "lifespan")
        yield
    
    except Exception as error:
        audit_logger.log_error(f"Erro na inicialização do banco de dados", "lifespan", {str(error)})
        raise
    
    finally:
        audit_logger.log_info("Finalizando conexão com o banco de dados...", "lifespan")
        await engine.dispose()
    

app = FastAPI()
app = FastAPI(
    title="GiftLinkApi",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    lifespan=lifespan  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(groupRouter.router, tags=["Groups"])
app.include_router(peopleRouter.router, tags=["People"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
