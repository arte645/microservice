from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sqlalchemy_update
from ..interfaces.IRepository import IRepository
from ..models.ArticleModel import Article
from ..interfaces.ISpecification import ISpecification

T = TypeVar("T")
ID = TypeVar("ID")


class ArticleRepository(IRepository[T, ID], Generic[T, ID]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_: ID) -> Optional[T]:
        """Получить статью по ID"""
        return await self.session.get(Article, id_)

    async def list(self, page: int = 0, per_page: int = None) -> List[T]:
        """Получить все статьи"""
        q = select(Article).offset(page * (per_page or 0)).limit(per_page)
        result = await self.session.execute(q)
        return result.scalars().all()

    async def add(self, entity: Article) -> None:
        """Добавить новую статью"""
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)

    async def update(self, data: dict):
        """Изменить поле статьи"""
        await self.session.execute(
            sqlalchemy_update(Article).where(Article.article_id == data["article_id"]).values(data)
        )
        await self.session.commit()

    async def remove(self, entity: Article) -> None:
        """Удалить статью"""
        self.session.delete(entity)
        await self.session.commit()

    async def filter_by_spec(self, spec: ISpecification, page: int = 0, per_page: int = None) -> List[T]:
        """Фильтрация по спецификации"""
        q = select(Article).where(spec.as_expression(Article)).offset(page * (per_page or 0)).limit(per_page)
        result = await self.session.execute(q)
        return result.scalars().all()
