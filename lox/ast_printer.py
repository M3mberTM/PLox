from io import StringIO
from typing import override

from .expression import (
    Binary,
    CommaExpr,
    Conditional,
    Expression,
    Grouping,
    Literal,
    Unary,
    Visitor,
)


class AstPrinter(Visitor[str]):

    def print(self, expr: Expression) -> str:
        return expr.accept(self)

    @override
    def visit_binary_expression(self, expression: Binary) -> str:
        return self.parenthesize(expression.operator.lexeme, expression.left, expression.right)

    @override
    def visit_grouping_expression(self, expression: Grouping) -> str:
        return self.parenthesize("group", expression.expression)

    @override
    def visit_literal_expression(self, expression: Literal) -> str:
        if expression.value is None:
            return "nil"
        return str(expression.value)

    @override
    def visit_unary_expression(self, expression: Unary) -> str:
        return self.parenthesize(expression.operator.lexeme, expression.right)

    @override
    def visit_comma_expression(self, expression: CommaExpr) -> str:
        return self.parenthesize(",", expression.left, expression.right)

    @override
    def visit_conditional_expression(self, expression: Conditional) -> str:
        return self.parenthesize("?:", expression.condition, expression.left, expression.right)

    def parenthesize(self, name: str, *expressions: Expression)->str:
        builder = StringIO()
        builder.write(f"({name}")
        for expr in expressions:
            builder.write(" ")
            builder.write(expr.accept(self))
        builder.write(")")

        return builder.getvalue()
