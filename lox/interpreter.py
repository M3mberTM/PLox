from typing import cast

from lox.expression import (
    Binary,
    CommaExpr,
    Conditional,
    Expression,
    Grouping,
    Literal,
    Unary,
)

from .errors import Reporter, RuntimedError
from .expression import Visitor
from .token import Token, TokenType


class Interpreter(Visitor[object]):

    def visit_literal_expression(self, expression: Literal) -> object:
        return expression.value

    def visit_grouping_expression(self, expression: Grouping) -> object:
        return self.evaluate(expression.expression)

    def visit_unary_expression(self, expression: Unary) -> object:
        right = self.evaluate(expression.right)

        match expression.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expression.operator, expression.right)
                return -float(cast(float, right))
            case TokenType.BANG:
                return not self.is_truthy(right)

    def visit_binary_expression(self, expression: Binary) -> object:
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)

        match expression.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(expression.operator, left, right)
                return float(cast(float, left)) - float(cast(float, right))
            case TokenType.SLASH:
                self.check_number_operands(expression.operator, left, right)
                if float(cast(float, right)) == 0:
                    raise RuntimedError(expression.operator,
                    "Zero Division error: cannot divide by zero")
                return float(cast(float, left)) / float(cast(float, right))
            case TokenType.STAR:
                self.check_number_operands(expression.operator, left, right)
                return float(cast(float, left)) * float(cast(float, right))
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right

                if isinstance(left, str) or isinstance(right, str):
                    return self.stringify(left) + self.stringify(right)

                raise RuntimedError(expression.operator,
                "Operands must be two numbers or two strings")
            case TokenType.GREATER:
                self.check_number_operands(expression.operator, left, right)
                return float(cast(float, left)) > float(cast(float, right))
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expression.operator, left, right)
                return float(cast(float, left)) >= float(cast(float, right))
            case TokenType.LESS:
                self.check_number_operands(expression.operator, left, right)
                return float(cast(float, left)) < float(cast(float, right))
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expression.operator, left, right)
                return float(cast(float, left)) <= float(cast(float, right))
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
        return None

    def visit_comma_expression(self, expression: CommaExpr) -> object:
        self.evaluate(expression.left)
        return self.evaluate(expression.right)

    def visit_conditional_expression(self, expression: Conditional) -> object:
        is_condition_true = self.is_truthy(self.evaluate(expression.condition))

        if is_condition_true:
            return self.evaluate(expression.left)
        else:
            return self.evaluate(expression.right)

    def is_equal(self, left: object, right: object) -> bool:
        return left == right

    def evaluate(self, expression: Expression) -> object:
        return expression.accept(self)

    def is_truthy(self, obj: object) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def check_number_operand(self, operator: Token, operand: object):
        if not isinstance(operand, float):
            raise RuntimedError(operator, "Operand must be a number")

    def check_number_operands(self, operator: Token, left: object, right: object):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimedError(operator, "Operand must be a number")

    def interpret(self, expression: Expression):
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except RuntimedError as err:
            Reporter.runtime_error(err)

    def stringify(self, value: object) -> str:
        if object is None:
            return "nil"

        if isinstance(value, float):
            text =  str(value)
            if text.endswith(".0"):
                text = text[:len(text) -2]
            return text

        return str(value)