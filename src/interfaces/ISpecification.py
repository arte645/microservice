from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import and_, or_, not_


T = TypeVar("T")

class ISpecification(ABC, Generic[T]):
    """
    Базовый класс для построения спецификаций SQLAlchemy.
    Поддерживает логические операции: и(&), или(|), не(~)
    """
    @abstractmethod
    def as_expression(self, entity_class: T) -> BinaryExpression:
        """Возвращает SQLAlchemy выражение для фильтра"""
        ...

    def __and__(self, other: 'ISpecification[T]') -> 'ISpecification[T]':
        return AndSpecification(self, other)

    def __or__(self, other: 'ISpecification[T]') -> 'ISpecification[T]':
        return OrSpecification(self, other)

    def __invert__(self) -> 'ISpecification[T]':
        return NotSpecification(self)


class DirectSpecification(ISpecification):
    def __init__(self, expression_fn):
        self.expression_fn = expression_fn

    def as_expression(self, entity_class: T) -> BinaryExpression:
        return self.expression_fn(entity_class)


class AndSpecification(DirectSpecification):
    def __init__(self, *specs: ISpecification):
        self.specs = specs

    def as_expression(self, entity_class: T) -> BinaryExpression:
        return and_(*(spec.as_expression(entity_class) for spec in self.specs))


class OrSpecification(DirectSpecification):
    def __init__(self, *specs: ISpecification):
        self.specs = specs

    def as_expression(self, entity_class: T) -> BinaryExpression:
        return or_(*(spec.as_expression(entity_class) for spec in self.specs))
    

class NotSpecification(DirectSpecification):
    def __init__(self, spec: ISpecification):
        self.spec = spec

    def as_expression(self, entity_class: T) -> BinaryExpression:
        return not_(self.spec.as_expression(entity_class))
    