from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .token import Token

R_co = TypeVar("R_co", covariant=True)

class Visitor(ABC, Generic[R_co]):
    @abstractmethod
    def visit_binary_expression(self, expression: "Binary") -> R_co: ...

    @abstractmethod
    def visit_grouping_expression(self, expression: "Grouping") -> R_co: ...

    @abstractmethod
    def visit_literal_expression(self, expression: "Literal") -> R_co: ...

    @abstractmethod
    def visit_unary_expression(self, expression: "Unary") -> R_co: ...

    @abstractmethod
    def visit_comma_expression(self, expression: "CommaExpr") -> R_co: ...

    @abstractmethod
    def visit_conditional_expression(self, expression: "Conditional") -> R_co: ...

class Expression(ABC):
    """
        Represents the grammar of the application. Each subclass represents one piece of grammar.
    """
    @abstractmethod
    def accept(self, visitor: Visitor[R_co]) -> R_co:
        raise NotImplementedError()

class Binary(Expression):
    """
        Represents an expression that runs an operator on two sub expressions
    """
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_binary_expression(self)

class Grouping(Expression):
    """
        Represents an expression surrounded by brackets. This gives it precedence
        over other possible expressions.
    """
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_grouping_expression(self)

class Literal(Expression):
    """
        Represents a literal as in a String, number, Boolean value or Nil
    """
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_literal_expression(self)

class Unary(Expression):
    """
        Represents an expression that is prepended by a unary operator (!,-) and all the
        other ones that can change the expression to a different value.
    """
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_unary_expression(self)

class CommaExpr(Expression):
    """
        Represents multiple expressions separated by a comma. Similar to C comma expression.
    """

    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_comma_expression(self)

class Conditional(Expression):

    def __init__(self, condition: Expression, left: Expression, right: Expression) -> None:
        self.condition = condition
        self.left = left
        self.right = right

    def accept(self, visitor: Visitor[R_co]):
        return visitor.visit_conditional_expression(self)