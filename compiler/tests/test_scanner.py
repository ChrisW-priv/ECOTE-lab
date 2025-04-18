import pytest
from compiler.scanner import scanner
from compiler.models import Symbol, Text, String


@pytest.mark.parametrize(
    'input_text, expected_tokens',
    [
        (
            """
    <root>
        <kitten Name="Whiskers">
            <parent>
                <cat Name="The Garfield"/>
            </parent>
        </kitten>
    </root>
    """,
            [
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
            ],
        ),
        (
            '<cat Name="Whiskers"/>',
            [
                Symbol('<'),
                Text('cat'),
                Text('Name'),
                Symbol('='),
                String('Whiskers'),
                Symbol('/>'),
            ],
        ),
        (
            ' arst< /> ',
            [
                Text('arst'),
                Symbol('<'),
                Symbol('/>'),
            ],
        ),
        (
            ' <arst /> ',
            [
                Symbol('<'),
                Text('arst'),
                Symbol('/>'),
            ],
        ),
    ],
)
def test_scanner(input_text, expected_tokens):
    tokens = list(scanner(input_text))
    assert tokens == expected_tokens


def test_scanner_invalid_close_tag():
    input_text = ' arst</> '
    with pytest.raises(Exception):
        list(scanner(input_text))
