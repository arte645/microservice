from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sqlalchemy_update
from ..interfaces.IRepository import IRepository
from ..models.ApiKeyModel import ApiKey
from ..interfaces.ISpecification import ISpecification

T = TypeVar("T")
ID = TypeVar("ID")


class ApiKeysRepository(IRepository[T, ID], Generic[T, ID]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_: ID) -> Optional[T]:
        """Получить api key по ID"""
        return await self.session.get(ApiKey, id_)

    async def list(self, page: int = 0, per_page: int = None) -> List[T]:
        """Получить все api keys"""
        q = select(ApiKey).offset(page * (per_page or 0)).limit(per_page)
        result = await self.session.execute(q)
        return result.scalars().all()

    async def add(self, entity: ApiKey) -> None:
        """Добавить новый api key"""
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)

    async def update(self, data: dict):
        """Изменить поле api key"""
        await self.session.execute(
            sqlalchemy_update(ApiKey).where(ApiKey.api_key_id == data["api_key_id"]).values(data)
        )
        await self.session.commit()

    async def remove(self, entity: ApiKey) -> None:
        """Удалить api key"""
        self.session.delete(entity)
        await self.session.commit()

    async def filter_by_spec(self, spec: ISpecification, page: int = 0, per_page: int = None) -> List[T]:
        """Фильтрация по спецификации"""
        q = select(ApiKey).where(spec.as_expression(ApiKey)).offset(page * (per_page or 0)).limit(per_page)
        result = await self.session.execute(q)
        return result.scalars().all()
