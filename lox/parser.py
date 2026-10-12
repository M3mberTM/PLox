from .errors import Reporter
from .expression import (
    Binary,
    CommaExpr,
    Conditional,
    Expression,
    Grouping,
    Literal,
    Unary,
)
from .token import Token, TokenType


class ParseError(Exception):
    pass

class Parser:
    """
        Class for turning tokens into logical grammar with rules of precedence and associativity
    """

    def __init__(self, tokens: list[Token]) -> None:
        self.current = 0
        self.tokens = tokens

    def _expression(self) -> Expression:
        return self._comma()

    def _comma(self) -> Expression:
        expr = self._ternary()

        while self._match(TokenType.COMMA):
            right = self._ternary()
            expr = CommaExpr(expr, right)

        return expr

    def _ternary(self) -> Expression:
        expr = self._equality()

        if self._match(TokenType.QUESTION):
            left = self._expression()
            self._consume(TokenType.COLON, "Ternary operator requires a colon between statements")
            right = self._ternary()
            expr = Conditional(expr, left, right)

        return expr


    def _equality(self) -> Expression:
        expr = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expression:
        expr = self._term()

        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL,TokenType.LESS,
        TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)

        return expr

    def _term(self) -> Expression:
        expr = self._factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)

        return expr

    def _factor(self) -> Expression:
        expr = self._unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)

        return expr

    def _unary(self) -> Expression:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)

        return self._primary()

    def _primary(self) -> Expression:
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return Grouping(expr)

        raise self._error(self._peek(), "Invalid token")

    def _match(self, *tokens: TokenType) -> bool:
        for token_type in tokens:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _advance(self) -> Token:
        if not self._is_at_the_end():
            self.current += 1
        return self._previous()

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_the_end():
            return False
        return self._peek().type == token_type

    def _is_at_the_end(self):
        return self._peek().type == TokenType.EOF

    def _peek(self)->Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current-1]

    def _consume(self, token_type: TokenType, msg: str) -> Token:
        if self._check(token_type):
            return self._advance()

        raise self._error(self._peek(), msg)

    def _error(self, token: Token, msg: str):
        Reporter.token_error(token, msg)
        return ParseError(msg)

    def _synchronize(self):
        self._advance()

        while not self._is_at_the_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            match self._peek().type:
                case TokenType.CLASS:
                    pass
                case TokenType.FUN:
                    pass
                case TokenType.VAR:
                    pass
                case TokenType.FOR:
                    pass
                case TokenType.IF:
                    pass
                case TokenType.WHILE:
                    pass
                case TokenType.PRINT:
                    pass
                case TokenType.RETURN:
                    return

            self._advance()

    def parse(self) -> Expression | None:
        try:
            return self._expression()
        except ParseError:
            return None
