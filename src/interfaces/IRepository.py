from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from .ISpecification import ISpecification

T = TypeVar("T")
ID = TypeVar("ID")

class IRepository(ABC, Generic[T, ID]):
    """
    Класс для взаимодействия с бд, он нужен, чтоб абстрагироваться от конкретной базы данных.
    """
    @abstractmethod
    def get_by_id(self, id_: ID) -> T | None: ...

    @abstractmethod
    def list(self) -> List[T]: ...

    @abstractmethod
    def add(self, entity: T) -> None: ...

    @abstractmethod
    def remove(self, entity: T) -> None: ...

    @abstractmethod
    def update(self, id_: ID, data: dict) -> None: ...
    
    @abstractmethod
    def filter_by_spec(self, spec: ISpecification[T]) -> List[T]: ...
    