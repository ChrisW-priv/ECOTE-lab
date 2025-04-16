from abc import ABC
from typing import Iterable
from dataclasses import dataclass


@dataclass
class ClassAttribute:
    """
    Represents an Attribute of a C# Class
    """

    name: str
    attribute_type: str


@dataclass
class ElementAttribute:
    """
    Represents an Attribute of an XML element
    """

    name: str
    value: str
    ref: str | None = None


@dataclass
class Element:
    """
    Represents an element in the Abstract Syntax Tree (AST).
    """

    element_name: str
    attributes: list[ElementAttribute] | None = None
    children: list["Element"] | None = None


class Token(ABC):
    """
    Represents a lexical token produced by the scanner.
    """


@dataclass(slots=True, frozen=True)
class Symbol(Token):
    value: str


@dataclass(slots=True, frozen=True)
class Text(Token):
    value: str


@dataclass(slots=True, frozen=True)
class String(Token):
    value: str


@dataclass
class Declaration:
    """
    Represents an instance declaration in the final code in the Main section
    """

    id: str
    instance_name: str
    class_name: str
    attributes: list[ElementAttribute]


@dataclass
class Class:
    """
    Represents an instance declaration in the final code in the Main section
    """

    name: str
    attributes: list[ClassAttribute]


@dataclass
class TypedTree:
    types: list[Class]
    declarations: list[Declaration]


def source_reader(filename: str) -> Iterable[str]:
    """
    Reads characters from the source XML file one by one.

    Args:
        filename (str): The path to the XML file.

    Yields:
        str: The next character in the file.
    """
    with open(filename, "r") as file:
        while char := file.read(1):
            yield char


def scanner(chars: Iterable[str]) -> Iterable[Token]:
    """
    Converts a stream of characters into tokens.

    Args:
        chars (Iterable[str]): An iterable stream of INDIVIDUAL characters.

    Yields:
        Token: The next token in the stream.
    """
    # Implementation of the scanner goes here
    for char in chars:
        yield Symbol(char)


def parser(tokens: Iterable[Token]) -> Element:
    """
    Parses a stream of tokens into an Abstract Syntax Tree (AST).

    Args:
        tokens (Iterable[Token]): An iterable stream of tokens.

    Returns:
        Element: The root of the AST.
    """
    # Implementation of the parser goes here
    return Element("root", [], [])


def semantic_analyser(ast: Element) -> TypedTree:
    """
    Analyzes the AST to enforce semantic rules. Generates new, tree that enables easy code generation in later stages.

    Args:
        ast (Element): The root of the AST.

    Returns:
        Element: The semantically analyzed AST.
    """
    # Implementation of the semantic analyzer goes here
    return TypedTree([], [])


def code_gen(typed_ast: TypedTree) -> dict[str, str]:
    """
    Generates C# code from the AST.

    Args:
        ast (Element): The semantically analyzed AST.

    Returns:
        Dict[str, str]: A mapping from filenames to their C# code content.
    """
    # Implementation of the code generator goes here
    return {
        "Main.cs": "",
    }


def writer(file_map: dict[str, str]) -> None:
    """
    Writes the generated C# code to disk.

    Args:
        file_map (Dict[str, str]): A mapping from filenames to their C# code content.
    """
    # Implementation of the writer goes here
    for filename in file_map:
        content = file_map[filename]
        with open(f"output/{filename}", "w") as file:
            file.write(content)


def compiler(filename):
    chars = source_reader(filename)
    tokens = scanner(chars)
    ast = parser(tokens)
    typed_ast = semantic_analyser(ast)
    generated_code = code_gen(typed_ast)
    writer(generated_code)


def main():
    compiler("foo.xml")


if __name__ == "__main__":
    main()
