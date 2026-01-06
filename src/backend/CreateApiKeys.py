from .models.Database import AsyncSessionLocal
from .repositories.ApiKeysRepository import ApiKeysRepository
from .specifications.ApiKeySpecifications import ApiKeySpecification
from .models.ApiKeyModel import ApiKey
from sqlalchemy.dialects.postgresql import insert
import secrets
import asyncio


def generate_api_key() -> str:
    return str(secrets.token_urlsafe(64))


async def create_api_key(key_name: str, key_value: str):
    """
    Создаёт API ключ атомарно.
    Если ключ с таким именем уже есть, вставка пропускается.
    """
    async with AsyncSessionLocal() as db:
        api_key = ApiKey(key=key_value, description=key_name)
        stmt = insert(ApiKey).values(
            key=api_key.key,
            description=api_key.description
        ).on_conflict_do_nothing(index_elements=["key"])

        await db.execute(stmt)
        await db.commit()


async def main():
    await create_api_key("backend", generate_api_key())
    await create_api_key("moderationWorker", generate_api_key())
    await create_api_key("previewWorker", generate_api_key())
    await create_api_key("publishWorker", generate_api_key())
    await create_api_key("usersApi", generate_api_key())
    await create_api_key("worker", generate_api_key())


if __name__ == "__main__":
    asyncio.run(main())
