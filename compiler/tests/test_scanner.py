import pytest
from compiler.scanner import scanner
from compiler.models import Symbol, Text, String


@pytest.fixture
def xml_example():
    return '<cat Name="Whiskers"/>'


def test_scanner_xml_example(xml_example):
    tokens = list(scanner(xml_example))
    expected_tokens = [
        Symbol('<'),
        Text('cat'),
        Text('Name'),
        Symbol('='),
        String('Whiskers'),
        Symbol('/>'),
    ]
    assert tokens == expected_tokens


@pytest.fixture
def nested_xml_example():
    return """
    <root>
        <kitten Name="Whiskers">
            <parent>
                <cat Name="The Garfield"/>
            </parent>
        </kitten>
    </root>
    """


def test_scanner_nested_xml(nested_xml_example):
    tokens = list(scanner(nested_xml_example))
    expected_tokens = [
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
    assert tokens == expected_tokens
