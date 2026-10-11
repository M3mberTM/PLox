from .token import Token, TokenType


class Reporter:

    had_error = False

    @staticmethod
    def error(line: int, message: str):
        Reporter.report(line, "", message)

    @staticmethod
    def token_error(token: Token, message: str):
        if token.type == TokenType.EOF:
            Reporter.report(token.line, "at the end", message)
        else:
            Reporter.report(token.line, f"at '{token.lexeme}'", message)


    @staticmethod
    def report(line: int, origin: str, message: str):
        # TODO implement a way to show where the error is in line like most errors in languages
        print(f"[line {line}] Error {origin}: {message}")
        Reporter.had_error = True
