from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from src.interfaces.IRepository import IRepository
from src.interfaces.ISpecification import ISpecification
from src.models.ArticleModel import Article

T = TypeVar("T")
ID = TypeVar("ID")

class ArticleRepository(IRepository[T, ID], Generic[T, ID]):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id_: ID) -> Optional[T]:
        """Получить статью по ID"""
        return self.session.query(Article).filter(Article.article_id == id_).first()

    def list(self) -> List[T]:
        """Получить все статьи"""
        return self.session.query(Article).all()

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

    def filter_by_spec(self, spec: ISpecification[T]) -> List[T]:
        """Фильтрация по спецификации"""
        all_users = self.list()
        return [user for user in all_users if spec.is_satisfied_by(user)]
