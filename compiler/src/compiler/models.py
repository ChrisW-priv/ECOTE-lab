from abc import ABC
from dataclasses import dataclass


class BaseToken(ABC):
    """
    Represents a lexical token produced by the scanner.
    """


@dataclass(slots=True, frozen=True)
class Symbol(BaseToken):
    value: str


@dataclass(slots=True, frozen=True)
class Text(BaseToken):
    value: str


@dataclass(slots=True, frozen=True)
class String(BaseToken):
    value: str


class XmlToken(ABC):
    """
    Represents an XML token produced by the parser.
    """


@dataclass
class ElementAttribute:
    """
    Represents an Attribute of an XML element
    """

    name: str
    value: str | None


@dataclass(slots=True, frozen=True)
class StartToken(XmlToken):
    name: str
    attributes: list[ElementAttribute] | None = None


@dataclass(slots=True, frozen=True)
class SelfClosingToken(XmlToken):
    name: str
    attributes: list[ElementAttribute] | None = None


@dataclass(slots=True, frozen=True)
class EndToken(XmlToken):
    name: str


@dataclass
class XmlElement:
    """
    Represents an element in the Abstract Syntax Tree (AST).
    """

    element_name: str
    attributes: list[ElementAttribute] | None = None
    children: list['XmlElement'] | None = None


@dataclass
class ClassAttribute:
    """
    Represents an Attribute of a C# Class
    """

    name: str
    attribute_type: str


@dataclass
class TypedXmlElement:
    element_name: str
    identified_type: str
    identified_role: str | None
    attributes: list[ElementAttribute] | None = None
    full_attributes: list[ClassAttribute] | None = None
    children: list['TypedXmlElement'] | None = None


@dataclass
class InstanceAttribute:
    """
    Represents an Attribute of an instance in the C# code
    """

    name: str
    value: str | None = None
    ref: str | None = None


@dataclass
class Declaration:
    """
    Represents an instance declaration in the final code in the Main section
    """

    id: str
    instance_name: str
    class_name: str
    attributes: list[InstanceAttribute] | None = None


@dataclass
class Class:
    """
    Represents an instance declaration in the final code in the Main section
    """

    name: str
    attributes: list[ClassAttribute]


@dataclass
class IntermediateCode:
    types: list[Class]
    declarations: list[Declaration]
