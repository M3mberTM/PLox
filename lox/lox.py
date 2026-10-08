import sys


class Lox:

    def __init__(self) -> None:
        self.had_error = False

    def main(self):
        if len(sys.argv) > 2: # python gets this script path as the first argument by default
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            self.run_file(sys.argv[1])
        else:
            print("hahah")


    def run_file(self, path: str):
        """
        private static void runFile(String path) throws IOException {
            byte[] bytes = Files.readAllBytes(Paths.get(path));
            run(new String(bytes, Charset.defaultCharset()));
        }
        """
        file = open(path, "r", encoding="utf-8") # noqa
        content = file.read()
        self.run(content)
        if self.had_error:
            sys.exit(65) # indicated error in the exit code

    def run_prompt(self):
        """
            private static void runPrompt() throws IOException {
                InputStreamReader input = new InputStreamReader(System.in);
                BufferedReader reader = new BufferedReader(input);

                for (;;) { 
                System.out.print("> ");
                String line = reader.readLine();
                if (line == null) break;
                run(line);
                }
            }
        """
        while True:
            line = input("> ")
            if not line:
                break
            self.run(line)
            # if the user made a mistake in the interactive session, it shouldn't kill their whole
            # session
            self.had_error = False

    def run(self, source: str):
        """
        private static void run(String source) {
            Scanner scanner = new Scanner(source);
            List<Token> tokens = scanner.scanTokens();

            // For now, just print the tokens.
            for (Token token : tokens) {
            System.out.println(token);
            }
        }
        """
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    def error(self, line: int, message: str):
        """
        static void error(int line, String message) {
            report(line, "", message);
        }
        """
        self.report(line, "", message)

    def report(self, line: int, origin: str, message: str):
        """
            static void error(int line, String message) {
                report(line, "", message);
            }

            private static void report(int line, String where,
                                        String message) {
                System.err.println(
                    "[line " + line + "] Error" + where + ": " + message);
                hadError = true;
            }
        """
        # TODO implement a way to show where the error is in line like most errors in languages
        print(f"[line {line}] Error {origin}: {message}")
        self.had_error = True

if __name__ == "__main__":
    Lox()
