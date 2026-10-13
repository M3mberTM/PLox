from .errors import Reporter
from .token import Token
from .token_type import TokenType


class Scanner:
    """
        Main class for parsing small lexemes and forming tokens
    """

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.col = 0
        self.current = 0
        self.line = 1
        self.keywords: dict[str, TokenType] = {
            "and": TokenType.AND,
            "or": TokenType.OR,
            "else": TokenType.ELSE,
            "class": TokenType.CLASS,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.col))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        char = self.advance()
        match char:
            # single character lexemes
            case "(":
                self.create_token(TokenType.LEFT_PAREN)
            case ")":
                self.create_token(TokenType.RIGHT_PAREN)
            case "{":
                self.create_token(TokenType.LEFT_BRACE)
            case "}":
                self.create_token(TokenType.RIGHT_BRACE)
            case ",":
                self.create_token(TokenType.COMMA)
            case ".":
                self.create_token(TokenType.DOT)
            case "-":
                self.create_token(TokenType.MINUS)
            case "+":
                self.create_token(TokenType.PLUS)
            case "*":
                self.create_token(TokenType.STAR)
            case ";":
                self.create_token(TokenType.SEMICOLON)
            case "?":
                self.create_token(TokenType.QUESTION)
            case ":":
                self.create_token(TokenType.COLON)
            # single character lexemes that can connect to other ones
            case "!":
                token = TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                self.create_token(token)
            case "=":
                token = TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                self.create_token(token)
            case "<":
                token = TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                self.create_token(token)
            case ">":
                token = TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                self.create_token(token)
            case "/":
                if self.match("/"):
                    # this is a comment now. Consume characters until it's the end of the line
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                elif self.match("*"):
                    # multiline comments
                    self.mult_comment()
                else:
                    self.create_token(TokenType.SLASH)
            # whitespace
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.line += 1
                self.col = 0
            # longer literals
            case "\"":
                self.string()
            case _:
                if self.is_digit(char):
                    self.number()
                elif self.is_alpha(char):
                    self.identifier()
                else:
                    Reporter.error(self.line, self.col, "Unexpected character")

    def mult_comment(self):
        while not self.is_at_end():
            if self.peek() == "*" and self.peek_next() == "/":
                self.advance()
                self.advance()
                return
            if self.peek() == "\n":
                self.line += 1

            self.advance()

        Reporter.error(self.line, self.col, "Unterminated multine comment")

    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER
        self.create_token(token_type)

    def is_alphanumeric(self, char: str) -> bool:
        return self.is_alpha(char) or self.is_digit(char)

    def is_alpha(self, char: str)->bool:
        num = ord(char)
        if num >= ord("a") and num <= ord("z"):
            return True
        if num >= ord("A") and num <= ord("Z"):
            return True
        return ord("_") == num

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == ".":
            # to take into account the doubles properly
            # if there is just a dot, consume it
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()


        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def peek_next(self)-> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current+1]


    def is_digit(self, char: str)-> bool:
        num = ord(char)
        return num >= ord("0") and num <= ord("9")

    def string(self):
        while self.peek() != "\"" and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            Reporter.error(self.line, self.col, "Unterminated string")
            return

        # closing
        self.advance()
        # trimming the surrounding quotes
        value = self.source[self.start + 1: self.current-1]
        self.add_token(TokenType.STRING, value)

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def create_token(self, token_type: TokenType):
        self.add_token(token_type, None)

    def add_token(self, token_type: TokenType, literal: object):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line, self.col))
