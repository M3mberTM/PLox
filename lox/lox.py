import sys

from .errors import Reporter
from .scanner import Scanner


class Lox:

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
        Lox.run(content)
        if Reporter.had_error:
            sys.exit(65) # indicated error in the exit code

    @staticmethod
    def run_prompt():
        while True:
            line = input("> ")
            if not line:
                break
            Lox.run(line)
            # if the user made a mistake in the interactive session, it shouldn't kill their whole
            # session
            Reporter.had_error = False

    @staticmethod
    def run(source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token.to_string())

def main():
    Lox.main()

if __name__ == "__main__":
    Lox.main()
