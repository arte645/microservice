from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sqlalchemy_update
from src.interfaces.IRepository import IRepository
from src.models.CommentModel import Comment
from src.interfaces.ISpecification import ISpecification

T = TypeVar("T")
ID = TypeVar("ID")


class CommentRepository(IRepository[T, ID], Generic[T, ID]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_: ID) -> Optional[T]:
        """Получить комментарий по ID"""
        return await self.session.get(Comment, id_)

    async def list(self, page: int = 0, per_page: int = None) -> List[T]:
        """Получить всех комментарии"""
        q = select(Comment)
        if per_page is not None:
            q = q.offset(page * (per_page or 0)).limit(per_page)
        result = await self.session.execute(q)
        return result.scalars().all()

    async def add(self, entity: Comment) -> None:
        """Добавить новый комментарий"""
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)

    async def update(self, data: dict):
        """Изменить текст комментария"""
        await self.session.execute(
            sqlalchemy_update(Comment).where(Comment.comment_id == data["comment_id"]).values(**data)
        )
        await self.session.commit()

    async def remove(self, entity: Comment) -> None:
        """Удалить комментарий"""
        self.session.delete(entity)
        await self.session.commit()

    async def filter_by_spec(self, spec: ISpecification, page: int = 0, per_page: int = None) -> List[T]:
        """Фильтрация по спецификации"""
        q = select(Comment).where(spec.as_expression(Comment)).offset(page * (per_page or 0)).limit(per_page)
        result = await self.session.execute(q)
        return result.scalars().all()
    