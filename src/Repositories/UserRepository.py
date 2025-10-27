from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.interfaces.IRepository import IRepository
from src.interfaces.ISpecification import ISpecification
from src.models.UserModel import User

T = TypeVar("T")
ID = TypeVar("ID")

class UserRepository(IRepository[T, ID], Generic[T, ID]):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id_: ID) -> Optional[T]:
        """Получить пользователя по ID"""
        return self.session.query(User).filter(User.user_id == id_).first()

    def list(self, page: int = 0, per_page: int = None) -> List[T]:
        """Получить всех пользователей"""
        return self.session.query(User).offset(page*per_page).limit(per_page).all()

    def add(self, entity: User) -> None:
        """Добавить нового пользователя"""
        self.session.add(entity)
        self.session.commit()

    def update(self, id_: ID, data: dict):
        """Изменить поле пользователя"""
        self.session.query(User).filter(User.user_id == id_).update(data)
        self.session.commit()

    def remove(self, entity: User) -> None:
        """Удалить пользователя"""
        self.session.delete(entity)
        self.session.commit()

    def filter_by_spec(self, spec: ISpecification, page: int = 0, per_page: int = None) -> List[T]:
        """Фильтрация по спецификации"""
        return self.session.query(User).filter(spec.as_expression(User)).offset(page*(per_page or 0)).limit(per_page).all()
    