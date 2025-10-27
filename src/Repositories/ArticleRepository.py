from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from src.interfaces.IRepository import IRepository
from src.models.ArticleModel import Article

T = TypeVar("T")
ID = TypeVar("ID")

class ArticleRepository(IRepository[T, ID], Generic[T, ID]):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id_: ID) -> Optional[T]:
        """Получить статью по ID"""
        return self.session.query(Article).filter(Article.article_id == id_).first()

    def list(self, page: int = 0, per_page: int = None) -> List[T]:
        """Получить все статьи"""
        return self.session.query(Article).offset(page*per_page).limit(per_page).all()

    def add(self, entity: Article) -> None:
        """Добавить новую статью"""
        self.session.add(entity)
        self.session.commit()

    def update(self, id_: ID, data: dict):
        """Изменить поле статьи"""
        self.session.query(Article).filter(Article.article_id == id_).update(data)
        self.session.commit()

    def remove(self, entity: Article) -> None:
        """Удалить статью"""
        self.session.delete(entity)
        self.session.commit()

    def filter_by_spec(self, spec: bool, page: int = None, per_page: int = None) -> List[T]:
        """Фильтрация по спецификации"""
        return self.session.query(Article).filter(spec).offset(page*per_page).limit(per_page).all()
