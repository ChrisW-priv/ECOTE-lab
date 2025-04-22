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


@dataclass(slots=True, frozen=True)
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

    def __eq__(self, other):
        return (self.element_name == other.element_name) and set(self.attributes or []) == set(other.attributes or [])


@dataclass(slots=True, frozen=True)
class ClassAttribute:
    """
    Represents an Attribute of a C# Class
    """

    name: str
    attribute_type: str

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other) -> bool:
        return self.name == other.name


@dataclass
class InstanceAttribute:
    """
    Represents an Attribute of an instance in the C# code
    """

    name: str
    value: str | None = None
    ref: str | None = None
    is_list: bool = False


@dataclass
class Declaration:
    """
    Represents an instance declaration in the final code in the Main section
    """

    id: str
    instance_name: str
    class_name: str
    attributes: list[InstanceAttribute] | None = None
    is_list: bool = False


@dataclass
class Class:
    """
    Represents an instance declaration in the final code in the Main section
    """

    name: str
    attributes: list[ClassAttribute]

    def __eq__(self, other):
        return (self.name == other.name) and set(self.attributes) == set(other.attributes)


@dataclass
class IntermediateCode:
    types: list[Class]
    declarations: list[Declaration]


@dataclass
class TypedXmlElement:
    element_name: str
    identified_type: int
    identified_role: str | None
    children: list['TypedXmlElement'] | None = None
    attributes: list[ElementAttribute] | None = None
    identified_class: Class | None = None
    is_list: bool = False


@dataclass
class SemanticAnalyzerOutput:
    typed_ast: TypedXmlElement
    types: list[set[ClassAttribute]]
