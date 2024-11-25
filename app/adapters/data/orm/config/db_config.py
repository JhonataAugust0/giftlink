import os 
import asyncio
from tortoise import Tortoise
from dotenv import load_dotenv
from tortoise import Tortoise


load_dotenv()

POSTGRES_URL=os.environ.get('POSTGRES_URL')
TORTOISE_MODELS_PATH=os.environ.get('TORTOISE_MODELS_PATH')


DATABASE_CONFIG = {
    "connections": {
        "default": POSTGRES_URL
    },
    "apps": {
        "models": {
            "models": [TORTOISE_MODELS_PATH, "aerich.models"],
            "default_connection": "default",
        },
    },
}

async def init_db():
    await Tortoise.init(
        db_url=POSTGRES_URL,
        modules={
            "models": [
                TORTOISE_MODELS_PATH,
                "aerich.models"
            ]
        }
    )

async def migrate_db():
    await init_db()
    await Tortoise.generate_schemas(safe=True)


if __name__ == "__main__":
    import asyncio
    asyncio.run(migrate_db()) 