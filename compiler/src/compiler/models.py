from abc import ABC
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
    Represents a class in the generated C# code
    """

    id: str
    instance_name: str
    class_name: str
    attributes: list[ElementAttribute]


@dataclass
class Class:
    """
    Represents an instance declaration in the generated C# code
    """

    name: str
    attributes: list[ClassAttribute]


@dataclass
class TypedTree:
    types: list[Class]
    declarations: list[Declaration]
