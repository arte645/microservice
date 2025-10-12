from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

T = TypeVar("T")

class ISpecification(ABC, Generic[T]):
    """
    Класс для фильтрации данных после запров в бд. Для конструирования сложных запросов понадобятся
    следующие логические операции: и(&), или (|), не(~)
    """
    @abstractmethod
    def is_satisfied_by(self, entity: T) -> bool: ...
     
    def __and__(self, other: 'ISpecification[T]') -> 'ISpecification[T]':
        return AndSpecification(self, other)

    def __or__(self, other: 'ISpecification[T]') -> 'ISpecification[T]':
        return OrSpec(self, other)

    def __invert__(self) -> 'ISpecification[T]':
        return NotSpec(self)
    
    
class DirectSpecification(ISpecification):
    def __init__(self, matchingCriteria: ISpecification):
        self._matchingCriteria = matchingCriteria
    
    def is_satisfied_by(self, entity: T) -> bool:
        return self._matchingCriteria(entity)
    
    
class AndSpecification(DirectSpecification):
    def __init__(self, *specs: ISpecification):
        self.specs = specs

    def is_satisfied_by(self, entity: T) -> bool:
        return all(spec.is_satisfied_by(entity) for spec in self.specs)
    
    
class OrSpec(DirectSpecification):
    def __init__(self, *specs: ISpecification[T]):
        self.specs = specs

    def is_satisfied_by(self, candidate: T) -> bool:
        return any(spec.is_satisfied_by(candidate) for spec in self.specs)


class NotSpec(DirectSpecification):
    def __init__(self, spec: ISpecification):
        self.spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self.spec.is_satisfied_by(candidate)
    