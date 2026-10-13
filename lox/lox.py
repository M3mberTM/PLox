import sys

from .errors import Reporter
from .interpreter import Interpreter
from .parser import Parser
from .scanner import Scanner


class Lox:

    interpreter = Interpreter()

    @staticmethod
    def main():
        if len(sys.argv) > 2: # python gets this script path as the first argument by default
            print("Usage: plox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            Lox.run_file(sys.argv[1])
        else:
            Lox.run_prompt()


    @staticmethod
    def run_file(path: str):
        file = open(path, "r", encoding="utf-8") # noqa
        content = file.read()
        Reporter.set_source(content)
        Lox.run(content)
        if Reporter.had_error:
            sys.exit(65) # indicated error in the exit code
        if Reporter.had_runtime_error:
            sys.exit(70)

    @staticmethod
    def run_prompt():
        while True:
            line = input("> ")
            if not line:
                break
            Reporter.set_source(line)
            Lox.run(line)
            # if the user made a mistake in the interactive session, it shouldn't kill their whole
            # session
            Reporter.had_error = False

    @staticmethod
    def run(source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()

        if Reporter.had_error:
            return
        if expression is None:
            return

        Lox.interpreter.interpret(expression)


def main():
    Lox.main()

if __name__ == "__main__":
    Lox.main()
