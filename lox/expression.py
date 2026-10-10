from abc import ABC, abstractmethod
from typing import Protocol, TypeVar, override

from .token import Token

R_co = TypeVar("R_co", covariant=True)

class Visitor(Protocol[R_co]):
    def visit_binary_expression(self, expression: "Binary") -> R_co: ...

    def visit_grouping_expression(self, expression: "Grouping") -> R_co: ...

    def visit_literal_expression(self, expression: "Literal") -> R_co: ...

    def visit_unary_expression(self, expression: "Unary") -> R_co: ...

class Expression(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor[R_co]) -> R_co:
        raise NotImplementedError()
class Binary(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right
    @override
    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_binary_expression(self)

class Grouping(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression
    @override
    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_grouping_expression(self)

class Literal(Expression):
    def __init__(self, value: object):
        self.value = value
    @override
    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_literal_expression(self)

class Unary(Expression):
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right
    @override
    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_unary_expression(self)
