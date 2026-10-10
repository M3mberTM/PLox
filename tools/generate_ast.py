import sys
from io import TextIOWrapper


class GenerateAst:

    def __init__(self) -> None:
        if len(sys.argv) < 2:
            print("Usage generate_ast <output dir>")
            sys.exit(64)
        output_dir = sys.argv[1]
        self.define_ast(output_dir, "Expression", [
            "Binary   ;  left: Expression, operator: Token, right: Expression",
            "Grouping ; expression: Expression",
            "Literal  ; value: object",
            "Unary    ; operator: Token, right: Expression"
            ])

    def define_ast(self, output_dir: str, base_name: str, types: list[str]):
        output_file = f"{output_dir}/{base_name.lower()}.py"
        with open(output_file, "w+", encoding="UTF-8") as file:
            file.write("from .token import Token\n")
            file.write("from typing import Protocol, TypeVar, override\n")
            file.write("from abc import ABC, abstractmethod\n")
            file.write("\n")
            self.define_visitor(file, base_name, types)
            file.write(f"class {base_name}(ABC):\n")
            file.write("    @abstractmethod\n")
            file.write("    def accept(self, visitor: Visitor[R_co]) -> R_co:\n")
            file.write("        raise NotImplementedError()\n")

            for val in types:
                split = val.split(";")
                class_name = split[0].strip()
                fields = split[1].strip()
                self.define_type(file, base_name, class_name, fields)

    def define_type(self, writer: TextIOWrapper, base_name: str, class_name: str, fields: str):
        writer.write(f"class {class_name}({base_name}):\n")
        writer.write(f"    def __init__(self, {fields}):\n")
        for field in fields.split(","):
            name = field.split(":")[0].strip()
            writer.write(f"        self.{name} = {name}\n")
        writer.write("    @override\n")
        writer.write("    def accept(self, visitor: Visitor[R_co]):\n")
        writer.write(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)")
        writer.write("\n\n")

    def define_visitor(self, writer: TextIOWrapper, base_name: str, fields: list[str]):
        writer.write("R_co = TypeVar(\"R_co\", covariant=True)\n\n")
        writer.write("class Visitor(Protocol[R_co]):\n")

        for field in fields:
            type_name = field.split(";")[0].strip()
            writer.write(f"    def visit_{type_name.lower()}_{base_name.lower()}")
            writer.write(f"(self, {base_name.lower()}: \"{type_name}\") -> R_co: ...\n\n")





if __name__ == "__main__":
    GenerateAst()
