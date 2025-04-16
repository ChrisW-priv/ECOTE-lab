from abc import ABC
from dataclasses import dataclass
from typing import List, Optional


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
    ref: Optional[str] = None


@dataclass
class Element:
    """
    Represents an element in the Abstract Syntax Tree (AST).
    """

    element_name: str
    attributes: Optional[List[ElementAttribute]] = None
    children: Optional[List["Element"]] = None


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
    attributes: List[ElementAttribute]


@dataclass
class Class:
    """
    Represents an instance declaration in the final code in the Main section
    """

    name: str
    attributes: List[ClassAttribute]


@dataclass
class TypedTree:
    types: List[Class]
    declarations: List[Declaration]
