from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from src.interfaces.IRepository import IRepository
from src.models.CommentModel import Comment

T = TypeVar("T")
ID = TypeVar("ID")

class CommentRepository(IRepository[T, ID], Generic[T, ID]):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id_: ID) -> Optional[T]:
        """Получить пользователя по ID"""
        return self.session.query(Comment).filter(Comment.comment_id == id_).first()

    def list(self, page: int = 0, per_page: int = None) -> List[T]:
        """Получить всех пользователей"""
        return self.session.query(Comment).offset(page*per_page).limit(per_page).all()

    def add(self, entity: Comment) -> None:
        """Добавить нового пользователя"""
        self.session.add(entity)
        self.session.commit()
    
    def update(self, id_: ID, data: dict):
        """Изменить текст комментария"""
        self.session.query(Comment).filter(Comment.comment_id == id_).update(data)
        self.session.commit()

    def remove(self, entity: Comment) -> None:
        """Удалить коммент"""
        self.session.delete(entity)
        self.session.commit()

    def filter_by_spec(self, spec: bool, page: int = None, per_page: int = None) -> List[T]:
        """Фильтрация по спецификации"""
        return self.session.query(Comment).filter(spec).offset(page*per_page).limit(per_page).all()
    