from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Any

T = TypeVar("T")
ID = TypeVar("ID")


class IRepository(ABC, Generic[T, ID]):
    """
    Интерфейс репозитория для взаимодействия с базой данных.
    Поддерживает пагинацию для list/filter_by_spec и принимает спецификацию для фильтрации.
    """
    @abstractmethod
    def get_by_id(self, id_: ID) -> Optional[T]: ...

    @abstractmethod
    def list(self, page: int = 0, per_page: Optional[int] = None) -> List[T]: ...

    @abstractmethod
    def add(self, entity: T) -> None: ...

    @abstractmethod
    def remove(self, entity: T) -> None: ...

    @abstractmethod
    def update(self, data: dict) -> None: ...

    @abstractmethod
    def filter_by_spec(self, spec: Any, page: int = 0, per_page: Optional[int] = None) -> List[T]: ...
    