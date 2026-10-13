from .token_type import TokenType


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int,
    col: int) -> None:
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.col = col

    def to_string(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"
