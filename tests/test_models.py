import pytest
from compiler.models import (
    ClassAttribute,
    ElementAttribute,
    Element,
    Symbol,
    Text,
    String,
    Declaration,
    Class,
    TypedTree
)

def test_class_attribute():
    attr = ClassAttribute(name="id", attribute_type="int")
    assert attr.name == "id"
    assert attr.attribute_type == "int"

def test_element_attribute():
    attr = ElementAttribute(name="color", value="red", ref=None)
    assert attr.name == "color"
    assert attr.value == "red"
    assert attr.ref is None

def test_element():
    element = Element(element_name="Root", attributes=[], children=[])
    assert element.element_name == "Root"
    assert element.attributes == []
    assert element.children == []

def test_symbol_token():
    symbol = Symbol(value="a")
    assert symbol.value == "a"

def test_text_token():
    text = Text(value="Sample text")
    assert text.value == "Sample text"

def test_string_token():
    string = String(value="\"Hello World\"")
    assert string.value == "\"Hello World\""

def test_declaration():
    decl = Declaration(
        id="1",
        instance_name="instance1",
        class_name="ClassA",
        attributes=[]
    )
    assert decl.id == "1"
    assert decl.instance_name == "instance1"
    assert decl.class_name == "ClassA"
    assert decl.attributes == []

def test_class():
    cls = Class(name="MyClass", attributes=[])
    assert cls.name == "MyClass"
    assert cls.attributes == []

def test_typed_tree():
    tree = TypedTree(types=[], declarations=[])
    assert tree.types == []
    assert tree.declarations == []
