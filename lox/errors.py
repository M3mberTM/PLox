from .token import Token, TokenType


class ParseError(Exception):
    pass

class RuntimedError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token

class Reporter:

    had_error = False
    had_runtime_error = False
    source_lines: list[str] = []

    @staticmethod
    def set_source(source: str):
        Reporter.source_lines = source.splitlines()

    @staticmethod
    def error(line: int, col: int, message: str):
        Reporter.report(line, col, "", message)

    @staticmethod
    def token_error(token: Token, message: str):
        if token.type == TokenType.EOF:
            Reporter.report(token.line, token.col, "at the end", message)
        else:
            Reporter.report(token.line, token.col, f"at '{token.lexeme}'", message)

    @staticmethod
    def runtime_error(error: RuntimedError):
        print(f"{error!s}\n[line {error.token.line}]")
        print(Reporter.source_lines[error.token.line - 1])
        print(f"{' '*(error.token.col - 1)}^")
        Reporter.had_runtime_error = True

    @staticmethod
    def report(line: int, col: int, origin: str, message: str):
        # TODO implement a way to show where the error is in line like most errors in languages
        print(f"[line {line}] Error {origin}: {message}")
        print(Reporter.source_lines[line - 1])
        print(f"{' '*(col -1)}^")
        Reporter.had_error = True
