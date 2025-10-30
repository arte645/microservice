from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sqlalchemy_update
from src.interfaces.IRepository import IRepository
from src.interfaces.ISpecification import ISpecification
from src.models.UserModel import User

T = TypeVar("T")
ID = TypeVar("ID")


class UserRepository(IRepository[T, ID], Generic[T, ID]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id_: ID) -> Optional[T]:
        """Получить пользователя по ID"""
        return await self.session.get(User, id_)

    async def list(self, page: int = 0, per_page: int = None) -> List[T]:
        """Получить всех пользователей"""
        q = select(User).offset(page * (per_page or 0)).limit(per_page)
        result = await self.session.execute(q)
        return result.scalars().all()

    async def add(self, entity: User) -> None:
        """Добавить нового пользователя"""
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)

    async def update(self, data: dict):
        """Изменить поле пользователя"""
        await self.session.execute(
            sqlalchemy_update(User).where(User.user_id == data["user_id"]).values(**data)
        )
        await self.session.commit()

    async def remove(self, entity: User) -> None:
        """Удалить пользователя"""
        self.session.delete(entity)
        await self.session.commit()

    async def filter_by_spec(self, spec: ISpecification, page: int = 0, per_page: int = None) -> List[T]:
        """Фильтрация по спецификации"""
        q = select(User).where(spec.as_expression(User)).offset(page * (per_page or 0)).limit(per_page)
        result = await self.session.execute(q)
        return result.scalars().all()
    