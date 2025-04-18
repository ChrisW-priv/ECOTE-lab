from compiler.models import Symbol, Text, String, Element, ElementAttribute
import pytest
from compiler.parser import parser


@pytest.fixture
def simple_tokens():
    return [
        Symbol('<'),
        Text('root'),
        Symbol('>'),
        Symbol('<'),
        Text('cat'),
        Text('Name'),
        Symbol('='),
        String('Whiskers'),
        Symbol('/>'),
        Symbol('</'),
        Text('root'),
        Symbol('>'),
    ]


@pytest.fixture
def nested_tokens():
    return [
        Symbol('<'),
        Text('root'),
        Symbol('>'),
        Symbol('<'),
        Text('kitten'),
        Text('Name'),
        Symbol('='),
        String('Whiskers'),
        Symbol('>'),
        Symbol('<'),
        Text('parent'),
        Symbol('>'),
        Symbol('<'),
        Text('cat'),
        Text('Name'),
        Symbol('='),
        String('The Garfield'),
        Symbol('/>'),
        Symbol('</'),
        Text('parent'),
        Symbol('>'),
        Symbol('</'),
        Text('kitten'),
        Symbol('>'),
        Symbol('</'),
        Text('root'),
        Symbol('>'),
    ]


@pytest.fixture
def simple_ast():
    return Element(
        element_name='root',
        attributes=[],
        children=[
            Element(
                element_name='cat',
                attributes=[ElementAttribute(name='Name', value='Whiskers')],
                children=[],
            )
        ],
    )


@pytest.fixture
def nested_ast():
    return Element(
        element_name='root',
        attributes=[],
        children=[
            Element(
                element_name='kitten',
                attributes=[ElementAttribute(name='Name', value='Whiskers')],
                children=[
                    Element(
                        element_name='parent',
                        attributes=[],
                        children=[
                            Element(
                                element_name='cat',
                                attributes=[ElementAttribute(name='Name', value='The Garfield')],
                                children=[],
                            )
                        ],
                    )
                ],
            )
        ],
    )


def test_parser_simple(simple_tokens, simple_ast):
    ast = parser(simple_tokens)
    assert ast == simple_ast


def test_parser_nested(nested_tokens, nested_ast):
    ast = parser(nested_tokens)
    assert ast == nested_ast
