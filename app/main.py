import uvicorn
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# SQLAlchemy imports
from app.adapters.data.orm.config.db_config import engine

# routes
from app.adapters.api.v1.routes.group_route import groupRouter

# config imports database
from app.adapters.data.orm.config.base import Base
from app.adapters.data.orm.config.db_config import POSTGRES_URL

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# app lifecycle 
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Iniciando conexão com o banco de dados...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tabelas criadas com sucesso!")
        yield
    except Exception as e:
        logger.error(f"Erro na inicialização do banco de dados: {e}")
        raise
    finally:
        logger.info("Finalizando conexão com o banco de dados...")
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

app.include_router(groupRouter.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
